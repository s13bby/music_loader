import sys
from yandex_music import Client

def get_tracks_from_playlist(owner, kind):
    
    client = Client().init()
    
    try:
        playlist = client.users_playlists(kind, owner)
        
        print(f"\nПлейлист: {playlist.title}")
        print(f"Всего треков: {playlist.track_count}")
        print("-" * 30)

        tracks_data = []

        file =  open(f"{playlist.title}.txt", "w", encoding="utf-8")

        for item in playlist.tracks:
            track = item.track
            artists = ", ".join([a.name for a in track.artists])
            title = track.title
            file.write(f"{artists} {title}\n")
            tracks_data.append({"artist": artists, "title": title})
            print(f"{artists} — {title}")

        print(f"\n{playlist.title}.txt плейлист сформирован")
        file.close()

        sys.exit()

    except Exception:
        print(f"Ошибка при чтении плейлиста: {Exception}")
        sys.exit()

import re

def extract_playlist_info(iframe_string):
    pattern = r"playlist/([\w\.-]+)/(\d+)"
    
    match = re.search(pattern, iframe_string)
    
    if match:
        owner = match.group(1)
        kind = match.group(2)
        return owner, kind
        
    return None, None