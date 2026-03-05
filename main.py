import argparse
from sources import spreader

parser = argparse.ArgumentParser(description="Загрузчик музыки из онлайн-источников с поддержкой интерактивного поиска и пакетной загрузки по плейлисту.")
parser.add_argument(
    "-p",
    "--path",
    type=str,
    default="downloads/",
    help="Путь для сохранения (по стандарту: downloads/)"
)

parser.add_argument(
    "-pl",
    "--playlist",
    type=str,
    default="",
    help="Путь к txt с плейлистом"
)

parser.add_argument(
    "-s",
    "--source",
    type=str,
    default="hitmo",
    help="Доступные сайты: hitmo, mp3party (по стандарту: hitmo)"
)

parser.add_argument(
    "--add_cover",
    action="store_true",
    help="Добавить обложку треку (по умолчанию выключено)"
)

parser.add_argument(
    "--import_playlist",
    type=str,
    default="",
    help="Импортировать плейлист из стриминг-сервиса (доступно: yandex)"
)

args = parser.parse_args()

PATH = args.path
PLAYLIST = args.playlist
SOURCE = args.source
COVER = args.add_cover
IMPORT = args.import_playlist

if IMPORT:
    spreader.import_playlist(IMPORT)
elif PLAYLIST == "" and COVER:
    search_input = input("Введи название исполнителя или трека:\n")
    spreader.spread(SOURCE, search_input, PATH, True)
elif PLAYLIST == "":
    search_input = input("Введи название исполнителя или трека:\n")
    spreader.spread(SOURCE, search_input, PATH, False)
elif PLAYLIST != "" and COVER:
    spreader.spread_playlist(SOURCE, PLAYLIST, PATH, True)
else:
    spreader.spread_playlist(SOURCE, PLAYLIST, PATH, False)