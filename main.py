import json
import argparse
import parsing_hitmo

with open("sources.json", "r", encoding="utf-8") as file:
    source = json.load(file)

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

args = parser.parse_args()
PATH = args.path
PLAYLIST = args.playlist


if PLAYLIST == "":
    search_input = input("Введи название исполнителя или трека:\n")
    parsing_hitmo.download(source["hitmo"], search_input, PATH, mode=0)
else:
    parsing_hitmo.download_playlist(source["hitmo"], PLAYLIST, PATH)