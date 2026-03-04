import argparse
import spreader

parser = argparse.ArgumentParser(description="Загрузчик музыки из онлайн-источников с поддержкой интерактивного поиска и пакетной загрузки по плейлисту.")
parser.add_argument(
    "-p",
    "--path",
    type=str,
    default="download/",
    help="путь для сохранения (по стандарту: download/)"
)

parser.add_argument(
    "-pl",
    "--playlist",
    type=str,
    default="",
    help="путь к txt с плейлистом"
)

parser.add_argument(
    "-s",
    "--source",
    type=str,
    default="hitmo",
    help="доступные сайты: hitmo, mp3party (по стандарту: hitmo)"
)

args = parser.parse_args()
PATH = args.path
PLAYLIST = args.playlist
SOURCE = args.source


if PLAYLIST == "":
    search_input = input("Введи название исполнителя или трека:\n")
    spreader.spread(SOURCE, search_input, PATH)
else:
    spreader.spread_playlist(SOURCE, PLAYLIST, PATH)