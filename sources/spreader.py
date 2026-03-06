from sources import hitmo, mp3party, yandex_pl, spotify, cover

def spread(from_, search_input, path, cover_mode):
    match from_:
        case "hitmo":
            if cover_mode:
                track_path, artist, track = hitmo.download(search_input, path, mode=0)
                if track_path:
                    cover_path = cover.get_yandex_cover(artist, track)
                    if cover_path:
                        cover.set_cover(cover_path, track_path)
            else:
                hitmo.download(search_input, path, mode=0)

        case "mp3party":
            if cover_mode:
                track_path, artist, track = mp3party.download(search_input, path, mode=0)
                if track_path:
                    cover_path = cover.get_yandex_cover(artist, track)
                    if cover_path:
                        cover.set_cover(cover_path, track_path)
            else:
                mp3party.download(search_input, path, mode=0)

def spread_playlist(from_, playlist_path, path, cover_mode):
    match from_:
        case "hitmo":
            if cover_mode:
                lines = []
                with open(playlist_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    track_path, artist, track = hitmo.download(line, path, mode=1)
                    if track_path:
                        cover_path = cover.get_yandex_cover(artist, track)
                        if cover_path:
                            cover.set_cover(cover_path, track_path)
            else:
                hitmo.download_playlist(playlist_path, path)
        case "mp3party":
            if cover_mode:
                lines = []
                with open(playlist_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    track_path, artist, track = mp3party.download(line, path, mode=1)
                    if track_path:
                        cover_path = cover.get_yandex_cover(artist, track)
                        if cover_path:
                            cover.set_cover(cover_path, track_path)
            else:
                mp3party.download_playlist(playlist_path, path)

def import_playlist(streaming):
    if streaming == "yandex":
        link = input("Введи HTML-код на плейлист\n")
        owner, kind = yandex_pl.extract_playlist_info(link)
        yandex_pl.get_tracks_from_playlist(owner, kind)

    elif streaming == "spotify":
        playlist_path = input("Инструкция по получению плейлиста spotify в формате .json описана в README.md\nУкажи путь к плейлисту в формате .json\n")
        spotify.get_tracks_from_playlist(playlist_path)