import argparse
import sys
import json
import time
from core import album, cover, hitmo, import_playlist, youtube

try:
    with open("settings.json", "r", encoding="utf-8") as data:
        settings = json.load(data)
except Exception:
    print("\nФайл с настройками settings.json не найден.\nВосстановите этот файл и перезапустите скрипт")
    sys.exit()

def arguments():
    parser = argparse.ArgumentParser(description="Загрузчик музыки из онлайн-источников с поддержкой интерактивного поиска, пакетной загрузки и импорта плейлистов.")
    parser.add_argument("-a", "--album", action="store_true", help="Импортировать альбом")
    parser.add_argument("-i", "--import_playlist", type=str, default="", help="Импортировать плейлист")
    parser.add_argument("-p", "--playlist", type=str, default="", help="Скачать список из txt")
    parser.add_argument("-s", "--source", type=str, default=f"{settings['source']}", help="Источник (hitmo/youtube)")

    args = parser.parse_args()
    return args.album, settings["cover"], args.import_playlist, args.playlist, args.source

def main():
    arg_album, cfg_cover, arg_import, arg_playlist, arg_source = arguments()

    if arg_album:
        request = input("Введите артиста и название альбома (синтаксис: артист название)\n")
        album.main(request)
        sys.exit()

    elif arg_import == "yandex":
        request = input("Введите HTML-код плейлиста\n")
        import_playlist.yandex(request)
        sys.exit()
    elif arg_import == "spotify":
        request = input("Введите путь до плейлиста в формате json\n")
        import_playlist.spotify(request)
        sys.exit()

    elif arg_playlist:
        try:
            with open(arg_playlist, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
        except Exception as e:
            print(f"Ошибка открытия файла: {e}")
            sys.exit()

        for i, line in enumerate(lines, 1):
            if arg_source == "hitmo":
                result = hitmo.main(line, "playlist")
            else:
                result = youtube.download_track(line)

            if result:
                cover.set_cover(result, line)
                print(f"[{i}/{len(lines)}] Обработан: {line}")
            else:
                print(f"Трек {line} не найден, пропускаем")
            
            if i < len(lines):
                time.sleep(settings["delay"])
        sys.exit()

    elif arg_source == "youtube":
        request = input("Введите артиста и название трека\n")
        result = youtube.download_track(request)
        if result:
            cover.set_cover(result, request)
        else:
            print(f"Трек {request} не найден")
        sys.exit()

    else:
        request = input("Введите артиста и название трека\n")
        result = hitmo.main(request, "handle")
        if result:
            cover.set_cover(result, request)
        sys.exit()

if __name__ == "__main__":
    main()