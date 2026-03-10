import requests
import os
from yandex_music import Client

def get_itunes_search_data(query):
    url = "https://itunes.apple.com/search"
    params = {"term": query, "entity": "album", "limit": 1}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"iTunes API Error: {e}")
        return None

def extract_itunes_album(data):
    if not data or data.get("resultCount") == 0:
        return None
    return data["results"][0]

def get_itunes_tracks(album_id):
    params = {"id": album_id, "entity": "song"}
    response = requests.get("https://itunes.apple.com/lookup", params=params)
    results = response.json().get("results", [])
    return results[1:] if len(results) > 1 else []

def format_itunes_track(item, artist_name):
    ms = item.get('trackTimeMillis', 0)
    duration = f"{ms // 60000}:{(ms // 1000) % 60:02d}"
    return {
        "no": item.get("trackNumber"),
        "artist": artist_name,
        "title": item.get("trackName"),
        "duration": duration
    }


def get_yandex_client():
    try:
        return Client().init()
    except:
        return None

def find_yandex_album(client, query):
    search = client.search(query, type_='album')
    if not search.albums or not search.albums.results:
        return None
    return search.albums.results[0]

def format_yandex_track(track):
    sec = track.duration_ms // 1000
    duration = f"{sec // 60}:{sec % 60:02d}"
    artists = ", ".join([a.name for a in track.artists])
    return {
        "no": getattr(track, 'number', 0),
        "artist": artists,
        "title": track.title,
        "duration": duration
    }


def process_itunes(query):
    data = get_itunes_search_data(query)
    album = extract_itunes_album(data)
    if not album:
        return None

    raw_tracks = get_itunes_tracks(album["collectionId"])
    artist = album.get("artistName", "Unknown")
    
    return {
        "title": album["collectionName"],
        "year": album["releaseDate"][:4],
        "tracks": [format_itunes_track(t, artist) for t in raw_tracks]
    }

def process_yandex(query):
    client = get_yandex_client()
    if not client: return None
    
    album_info = find_yandex_album(client, query)
    if not album_info: return None
    
    full_album = client.albums_with_tracks(album_info.id)
    tracks = []
    for vol in full_album.volumes:
        for t in vol:
            tracks.append(format_yandex_track(t))
            
    return {
        "title": album_info.title,
        "year": album_info.year or "Unknown",
        "tracks": tracks
    }

def save_to_file(album_data):
    filename = f"{album_data['title']}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for t in album_data['tracks']:
            line = f"{t['no']}. {t['artist']} - {t['title']} ({t['duration']})"
            print(line)
            f.write(f"{t['artist']} {t['title']}\n")
    print(f"\nГотово! Сохранено в {filename}")


def main(request):
    print(f"Поиск '{request}' в iTunes...")
    result = process_itunes(request)
    
    if not result:
        print("В iTunes не найдено. Ищем в Яндекс.Музыке...")
        result = process_yandex(request)
        
    if result:
        print(f"Найдено: {result['title']} ({result['year']})")
        save_to_file(result)
    else:
        print(f"Альбом '{request}' не найден ни в одном источнике.")