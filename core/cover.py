import io
import requests
import os
import time
import json
from yandex_music import Client
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

def get_yandex_cover(query, settings):
    try:
        client = Client().init()
        time.sleep(settings["delay"])
        search_result = client.search(query, type_='track')
        if search_result.tracks and search_result.tracks.results:
            track_obj = search_result.tracks.results[0]
            if track_obj.og_image:
                return "https://" + track_obj.og_image.replace('%%', '1000x1000')
        return None
    except:
        return None

def get_itunes_cover(query, settings):
    url = "https://itunes.apple.com/search"
    params = {"term": query, "entity": "song", "limit": 1}
    try:
        time.sleep(settings["delay"])
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("resultCount", 0) > 0:
            return data["results"][0]["artworkUrl100"].replace("100x100bb.jpg", "1000x1000bb.jpg")
        return None
    except:
        return None

def get_best_cover(query, settings):
    cover_url = get_itunes_cover(query, settings)
    if not cover_url:
        cover_url = get_yandex_cover(query, settings)
    return cover_url

def set_cover(track_path, request):
    with open("settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)
    cover_url = get_best_cover(request, settings)
    if not cover_url:
        return

    try:
        response = requests.get(cover_url, timeout=10)
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        img_data = buffer.getvalue()

        audio = MP3(track_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()

        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=img_data
            )
        )
        audio.save()
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False