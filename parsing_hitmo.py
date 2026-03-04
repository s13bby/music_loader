
import requests
import subprocess
from bs4 import BeautifulSoup

with open("sources.txt", "r") as file:
    source = file.read()

def download():
    search_input = input("Введи название исполнителя или трека:\n")

    search_url_artist = "https://rus.hitmotop.com/search?q=" + search_input.replace(" ", "%20")
    page_searched_artist = requests.get(search_url_artist)
    soup = BeautifulSoup(page_searched_artist.text, 'html.parser')

    track_titles_extracted = [track.get_text(strip=True) for track in soup.find_all("div", class_="track__title")]
    track_artist_extracted = [track.get_text(strip=True) for track in soup.find_all("div", class_="track__desc")]
    track_ids = [link.get("href").split("/")[-1] for link in soup.find_all("a", class_="track__info-l")]

    titles = {str(track_count): track_ids[track_count] for track_count in range(0, len(track_titles_extracted), 1)}

    for track_count in range(0, len(track_titles_extracted), 1):
        print(f"{track_count}. {track_artist_extracted[track_count]} - {track_titles_extracted[track_count]}")

    song_count_input = input()
    search_url_song = "https://rus.hitmotop.com/song/" + str(titles.get(str(song_count_input)))

    page_searched_song = requests.get(search_url_song)
    soup1 = BeautifulSoup(page_searched_song.text, 'html.parser')

    download_links = soup1.find_all("a", class_="track__download-btn")
    if download_links:
        download_url = download_links[0].get("href")
        subprocess.run(["curl", "-O", download_url])
