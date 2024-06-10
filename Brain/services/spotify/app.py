from flask import Flask, request, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
import sys
import time

# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utilities.readEnv import readEnv  # Absolute import

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Replace with your Spotify API credentials
CLIENT_ID = readEnv("CLIENT_ID")
CLIENT_SECRET = readEnv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI

scope = "user-library-read user-read-playback-state user-modify-playback-state user-top-read"

@app.route('/')
def index():
    sp_oauth = SpotifyOAuth(scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(scope=scope)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    session["token_info"] = token_info
    return redirect(url_for('welcome'))

def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return None

    now = int(time.time())
    is_token_expired = token_info['expires_at'] - now < 60

    if is_token_expired:
        sp_oauth = SpotifyOAuth(scope=scope)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session["token_info"] = token_info

    return token_info

@app.route('/welcome')
def welcome():
    token_info = get_token()
    if not token_info:
        return redirect('/')
    
    sp = Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    return f"Welcome, {user['display_name']}!"

@app.route('/play_track')
def play_track():
    token_info = get_token()
    if not token_info:
        return redirect('/')

    sp = Spotify(auth=token_info['access_token'])
    track_name = request.args.get('track')
    results = sp.search(q=track_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        try:
            sp.start_playback(uris=[f"spotify:track:{track['id']}"])
            return f"Playing song: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}"
        except SpotifyException as e:
            if e.http_status == 403 and 'PREMIUM_REQUIRED' in str(e):
                return "Playing tracks requires a Spotify Premium account."
            else:
                return f"An error occurred: {str(e)}"
    else:
        return "Track not found."

@app.route('/play_playlist')
def play_playlist():
    token_info = get_token()
    if not token_info:
        return redirect('/')

    sp = Spotify(auth=token_info['access_token'])
    playlist_id = request.args.get('playlist_id')
    try:
        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
        return "Playlist playback started successfully!"
    except SpotifyException as e:
        if e.http_status == 403 and 'PREMIUM_REQUIRED' in str(e):
            return "Playing playlists requires a Spotify Premium account."
        else:
            return f"An error occurred: {str(e)}"

@app.route('/top_searches')
def top_searches():
    token_info = get_token()
    if not token_info:
        return redirect('/')

    sp = Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=10)
    response = "Top Searches:<br>"
    for track in top_tracks['items']:
        response += f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}<br>"
    return response

@app.route('/most_played')
def most_played():
    token_info = get_token()
    if not token_info:
        return redirect('/')

    sp = Spotify(auth=token_info['access_token'])
    most_played = sp.current_user_top_tracks(limit=10, time_range='long_term')
    response = "Most Played Tracks:<br>"
    for track in most_played['items']:
        response += f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}<br>"
    return response

if __name__ == "__main__":
    app.run(debug=True)
