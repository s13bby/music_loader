import yt_dlp
import os
import json

def download_track(input_):
    with open ("settings.json", "r", encoding="utf-8") as data:
        settings = json.load(data)

    query = f"ytsearch1:{input_}"
    
    if not os.path.exists(settings["save to"]):
        os.makedirs(settings["save to"])

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],

        "proxy": settings["proxy"], 
    
        "extractor_args": {
            "youtube": {
                "player_client": ["android"],
                "skip": ["webpage"],
            }
        },

        "nocheckcertificate": True,
        "outtmpl": settings["save to"] + "%(title)s.%(ext)s",
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=True)
            
            if 'entries' in info_dict:
                video_info = info_dict['entries'][0]
            else:
                video_info = info_dict

            file_path = ydl.prepare_filename(video_info)
            final_path = os.path.splitext(file_path)[0] + ".mp3"
            
            print(f"Скачано: {final_path}")
            return final_path

    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        return False
