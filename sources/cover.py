import io
import requests
import os
import subprocess
import random
import time
from yandex_music import Client
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from tqdm import tqdm

def get_yandex_cover(artist, track):
    save_path = None
    temp_name = str(random.randint(0, 2**32 -1))[:5]+".png"

    try:
        time.sleep(0.5)
        client = Client().init()
        search_result = client.search(f"{artist} {track}")

        if search_result.tracks and search_result.tracks.results:
            track_obj = search_result.tracks.results[0]
            if track_obj.og_image:
                download_url =  "https://" + track_obj.og_image.replace('%%', '1000x1000')
                save_path = os.path.join("temp/", temp_name)
                time.sleep(0.5)
                result = subprocess.run(["curl", "-L", "-o", save_path, download_url])
    except Exception as e:
        print(f"Ошибка Яндекса: {e}")
    return save_path

def set_cover(cover_path, track_path):
    if not cover_path or not os.path.exists(cover_path):
        print(f"Обложка не найдена, пропускаем: {track_path}")
        return

    with Image.open(cover_path) as img:

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        image_data = buffer.getvalue()

    audio = MP3(track_path)
    if not audio.tags:
        audio.add_tags()

    audio.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=image_data
        )
    )

    audio.save()
    os.remove(cover_path)