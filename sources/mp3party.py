import os
import time
import requests
import subprocess
from bs4 import BeautifulSoup
from tqdm import tqdm

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
        
        head = requests.head(download_url, headers={"User-Agent": "Mozilla/5.0"})
        total_size = int(head.headers.get('content-length', 0))

        with requests.get(download_url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
            r.raise_for_status()
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))

        print(f"\nСкачано: {filename}")
        return save_path, artist, title

    else:
        print("Ссылка для скачивания не найдена")
        return False, False, False

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
