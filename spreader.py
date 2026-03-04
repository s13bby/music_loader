import parsing_hitmo
import parsing_mp3party

def spread(from_, search_input, path):
    match from_:
        case "hitmo":
            parsing_hitmo.download(search_input, path, mode=0)
        case "mp3party":
            parsing_mp3party.download(search_input, path, mode=0)

def spread_playlist(from_, playlist_path, path):
    match from_:
        case "hitmo":
            parsing_hitmo.download_playlist(playlist_path, path)
        case "mp3party":
            parsing_mp3party.download_playlist(playlist_path, path)