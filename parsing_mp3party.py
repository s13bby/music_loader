import os
import time
import requests
import subprocess
from bs4 import BeautifulSoup

def download(what_, where_, mode=0):
    search_url_artist = "https://mp3party.net/" + "search?q=" + what_.replace(" ", "%20")
    page_searched_artist = requests.get(search_url_artist)
    soup = BeautifulSoup(page_searched_artist.text, 'html.parser')

    tracks = soup.find_all("div", class_="track__user-panel")

    if not tracks:
        print(f"Ничего не найдено по запросу: {what_}")
        return False

    track_artists = [track.get("data-js-artist-name") for track in tracks]
    track_titles = [track.get("data-js-song-title") for track in tracks]
    track_urls = [track.get("data-js-url") for track in tracks]

    id_ = {str(i): track_urls[i] for i in range(len(tracks))}

    if mode == 0:
        for i in range(len(tracks)):
            print(f"{i}. {track_artists[i]} - {track_titles[i]} | {track_urls[i]}")

        selected_index = int(input())
    else:
        selected_index = 0
        print(f"Найдено: {track_artists[0]} - {track_titles[0]}")

    download_url = id_.get(str(selected_index))

    if download_url:
        artist = track_artists[selected_index]
        title = track_titles[selected_index]
        filename = f"{artist} - {title}.mp3"
        os.makedirs(where_, exist_ok=True)
        save_path = os.path.join(where_, filename)
        time.sleep(2)
        result = subprocess.run(
            ["curl", "-L", "-A", "Mozilla/5.0", "-o", save_path, download_url],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"Ошибка загрузки: {result.stderr}")
            return False
        print(f"Скачано: {filename}")
        return True
    else:
        print("Ссылка для скачивания не найдена")
        return False

def download_playlist(playlist_path, where_, delay=5):
    if not os.path.exists(playlist_path):
        print(f"Файл плейлиста не найден: {playlist_path}")
        return

    with open(playlist_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        print(f"\n[{i}/{total}] Обработка: {line}")
        download(line, where_, mode=1)

        if i < total:
            print(f"Ожидание {delay} сек...")
            time.sleep(delay)
