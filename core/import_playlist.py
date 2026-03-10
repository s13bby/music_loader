import json
import sys
import re
import random
from yandex_music import Client

def yandex(html_):
    pattern = r"playlist/([\w\.-]+)/(\d+)"
    
    match = re.search(pattern, html_)
    
    if match:
        owner = match.group(1)
        kind = match.group(2)
    else:
        sys.exit()
    
    client = Client().init()
    
    try:
        playlist = client.users_playlists(kind, owner)
        
        print(f"\nПлейлист: {playlist.title}")
        print(f"Всего треков: {playlist.track_count}")
        print("-" * 30)

        file =  open(f"{playlist.title}.txt", "w", encoding="utf-8")

        for item in playlist.tracks:
            track = item.track
            artists = ", ".join([a.name for a in track.artists])
            title = track.title
            file.write(f"{artists} {title}\n")
            print(f"{artists} — {title}")

        print(f"\n{playlist.title}.txt плейлист сформирован")
        file.close()

        sys.exit()

    except Exception:
        print(f"Ошибка при чтении плейлиста: {Exception}")
        sys.exit()

def spotify(playlist):
    try:
        with open(playlist, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Ошибка открытия файла: {e}")
        sys.exit()

    temp_name = str(random.randint(0, 2**32 -1))[:5]

    items = data["data"]["playlistV2"]["content"]["items"]

    file =  open(f"{temp_name}.txt", "w", encoding="utf-8")

    for item in items:
        track = item["itemV2"]["data"]

        title = track["name"]
        artist = track["artists"]["items"][0]["profile"]["name"]
        file.write(f"{artist} {title}\n")
        print(f"{artist} — {title}")


    file.close()
    print(f"\n{temp_name}.txt плейлист сформирован")

    sys.exit()