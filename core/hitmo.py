import requests
import sys
import re
import os
import time
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

def ping():
    pages = ["https://rus.hitmotop.com/", "https://eu.hitmo-top.com/"]
    for page in pages:
        status = requests.get(page)
        if status.status_code == 200:
            return page
    print("Ресурсы не доступны")
    sys.exit()

def parse(request, page, settings):
    url = page + "search?q=" + request.replace(" ", "%20")
    time.sleep(settings["delay"]) 
    content = BeautifulSoup(requests.get(url).text, "html.parser")
    return content

def get_artists(content):
    return [artists.get_text(strip=True) for artists in content.find_all("div", class_="track__desc")]

def get_titles(content):
    return [titles.get_text(strip=True) for titles in content.find_all("div", class_="track__title")]

def get_links(content):
    return [links.get("href") for links in content.find_all("a", class_="track__download-btn")]

def get_data_dict(content):
    dictionary = {
        i: [artist, title, link]
        for i, (artist, title, link) in enumerate(zip(get_artists(content), get_titles(content), get_links(content)))
    }
    return dictionary

def get_url(index, dictionary):
    return dictionary[index][2]

def handle():
    selected_index = int(input("Скачать трек: "))
    return selected_index

def playlist():
    return 0

def get_filename(index, dictionary):
    filename = f"{dictionary[index][0]} - {dictionary[index][1]}.mp3"
    filename = re.sub(r'[*"?<>|:$&()\[\]!/]+', "", filename)
    return filename

def get_path_to_file(filename, settings):
    os.makedirs(settings["save to"], exist_ok=True)
    path_to_file = os.path.join(settings["save to"], filename)
    return path_to_file

def print_content(dictionary):
    for i in range(len(dictionary)):
        print(f"{i}. {dictionary[i][0]} - {dictionary[i][1]}")
    return None

def download(url, path_to_file, filename, settings):
    time.sleep(settings["delay"])
    with requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
        r.raise_for_status()
        size = int(r.headers.get('content-length', 0))

        with open(path_to_file, 'wb') as f, tqdm(total=size, unit='B', unit_scale=True) as pbar:
            for chunk in r.iter_content(8192):
                pbar.update(f.write(chunk))
    print(f"Скачано: {filename}")

def main(request, mode):
    try:
        with open("settings.json", "r", encoding="utf-8") as file:
            settings = json.load(file)
    except Exception as e:
        print(f"Ошибка открытия файла: {e}")
        sys.exit()
    page = ping()
    content = parse(request, page, settings)
    dictionary = get_data_dict(content)
    if not dictionary:
        print(f"По запросу {request} ничего не найдено.")
        return
    if mode == "handle":
        print_content(dictionary)
        index = handle()
    else:
        index = playlist()
    url = get_url(index, dictionary)
    filename = get_filename(index, dictionary)
    path_to_file = get_path_to_file(filename, settings)
    download(url, path_to_file, filename, settings)
    
    return path_to_file