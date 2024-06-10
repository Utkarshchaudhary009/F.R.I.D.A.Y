import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from Brain.utilities.readEnv import readEnv  # Absolute import

def get_spotify_client():
    # Replace with your Spotify API credentials
    client_id = readEnv("CLIENT_ID")
    client_secret =readEnv("CLIENT_SECRET")

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def get_music_details(args):
    try:
        track_name=args["song_title"]
    except:
        return {"response":f"Sorry, I didn't catch the song name."}
    sp = get_spotify_client()
    results = sp.search(q=track_name, limit=1, type='track')
    try:
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            music_details = {
                'name': track['name'],
                'album': track['album']['name'],
                'artists': ', '.join([artist['name'] for artist in track['artists']]),
                'release_date': track['album']['release_date'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url']
            }
            # f"The singer of the song '{song_name}' is {details['artists']}."
            artist_grammer=['singer','is'] if len(track['artists']) < 2 else ['singers','are'] 
            # print(music_details)
            return {"response":f"The {artist_grammer[0]} of the song {music_details['name']} {artist_grammer[1]} {music_details['artists']}. It was released on date {music_details['release_date']}."}
        else:
            return None
    except:
        return{"response":"there is some problem try again later."}



if __name__ == "__main__":
        while True:
            track_name = input("Enter the name of the track: ")
            details = get_music_details(track_name)
            if details:
                print("Music Details:")
                for key, value in details.items():
                    print(f"{key.capitalize()}: {value}")
            else:
                print("Track not found.")
