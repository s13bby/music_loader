import os
import time
import requests
import subprocess
from bs4 import BeautifulSoup

def download(from_, what_, where_, mode=0):
    search_url_artist = from_ + "search?q=" + what_.replace(" ", "%20")
    page_searched_artist = requests.get(search_url_artist)
    soup = BeautifulSoup(page_searched_artist.text, 'html.parser')

    track_titles_extracted = [track.get_text(strip=True) for track in soup.find_all("div", class_="track__title")]
    track_artist_extracted = [track.get_text(strip=True) for track in soup.find_all("div", class_="track__desc")]
    track_ids = [link.get("href").split("/")[-1] for link in soup.find_all("a", class_="track__info-l")]

    if not track_ids:
        print(f"Ничего не найдено по запросу: {what_}")
        return False

    id_ = {str(track_count): track_ids[track_count] for track_count in range(0, len(track_titles_extracted), 1)}

    if mode == 0:
        for track_count in range(0, len(track_titles_extracted), 1):
            print(f"{track_count}. {track_artist_extracted[track_count]} - {track_titles_extracted[track_count]}")

        song_count_input = input()
        selected_index = int(song_count_input)
    else:
        selected_index = 0
        print(f"Найдено: {track_artist_extracted[0]} - {track_titles_extracted[0]}")

    search_url_song = from_ + "song/" + str(id_.get(str(selected_index)))

    page_searched_song = requests.get(search_url_song)
    soup1 = BeautifulSoup(page_searched_song.text, 'html.parser')

    download_links = soup1.find_all("a", class_="track__download-btn")

    if download_links:
        download_url = download_links[0].get("href")

        if download_url.startswith("/"):
            download_url = from_.rstrip("/") + download_url

        artist = track_artist_extracted[selected_index]
        title = track_titles_extracted[selected_index]
        filename = f"{artist} - {title}.mp3"
        os.makedirs(where_, exist_ok=True)
        save_path = os.path.join(where_, filename)
        result = subprocess.run(["curl", "-L", "-o", save_path, download_url], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Ошибка загрузки: {result.stderr}")
            return False
        print(f"Скачано: {filename}")
        return True
    else:
        print("Ссылка для скачивания не найдена")
        return False


def download_playlist(from_, playlist_path, where_, delay=3):
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
        download(from_, line, where_, mode=1)

        if i < total:
            print(f"Ожидание {delay} сек...")
            time.sleep(delay)
