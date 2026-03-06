import json
import sys

def get_tracks_from_playlist(playlist_json):
    with open(playlist_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data["data"]["playlistV2"]["content"]["items"]

    file =  open("playlist_spotify.txt", "w", encoding="utf-8")

    for item in items:
        track = item["itemV2"]["data"]

        title = track["name"]
        artist = track["artists"]["items"][0]["profile"]["name"]
        file.write(f"{artist} {title}\n")
        print(f"{artist} — {title}")


    file.close()
    print(f"\nplaylist_spotify.txt плейлист сформирован")

    sys.exit()
    