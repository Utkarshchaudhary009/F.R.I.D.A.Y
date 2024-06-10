from pytube import YouTube, Search
from mutagen.mp4 import MP4, MP4Cover
import os
import platform
import subprocess
import json
import win32gui
import win32api
import re



DOWNLOAD_DIR = 'F:\\Friday\\downloads'
METADATA_FILE = 'F:\\Friday\\brain\\data\\metadata.json'

def load_metadata():
    try:
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        return{"response":"Error loading metadata: {e}"}
    return {}

def save_metadata(metadata):
    try:
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=4)
    except Exception as e:
        return{"response":f"Error saving metadata: {e}"}

def search_and_download_song(query):
    metadata = load_metadata()

    try:
        search = Search(query)
        video = search.results[0]
        yt = YouTube(video.watch_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_name = f"{yt.title}.mp4"
        file_path = os.path.join(DOWNLOAD_DIR, file_name)

        if yt.title not in metadata:
            print(f"Downloading: {yt.title}")
            audio_stream.download(output_path=DOWNLOAD_DIR, filename=file_name)
            
            track_metadata = {
                'title': yt.title,
                'artists': ', '.join([yt.author]),
                'album': yt.title,  # YouTube doesn't provide album info
                'release_date': yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown'
            }

            # Add metadata to file
            audio = MP4(file_path)
            audio['\xa9nam'] = track_metadata['title']
            audio['\xa9ART'] = track_metadata['artists']
            audio['\xa9alb'] = track_metadata['album']
            audio['\xa9day'] = track_metadata['release_date']
            audio.save()

            metadata[yt.title] = track_metadata
            save_metadata(metadata)
        else:
            print(f"File already exists: {yt.title}")

        return file_path
    except Exception as e:
        return{"response":f"Error downloading song: {e}"}

def play_audio(file_path):
    try:
        system = platform.system()
        if system == 'Windows':
            os.startfile(file_path)
        elif system == 'Darwin':  # macOS
            subprocess.call(['open', file_path])
        else:  # Linux
            subprocess.call(['xdg-open', file_path])
        return{"response":f"Playing: {song_name}"}
    except Exception as e:
        return{"response":f"Error playing audio: {e}"}

WM_APPCOMMAND = 0x0319
APPCOMMAND_MEDIA_PLAY_PAUSE = 14
APPCOMMAND_MEDIA_PAUSE = 47

def pause_audio_windows():
    try:
        system = platform.system()
        if system != 'Windows':
            return{"response":"This function is only supported on Windows."}
        
        hWnd = win32gui.FindWindow(None, 'Media Player')
        if hWnd:
            # Use win32api to send the WM_APPCOMMAND message for pausing
            win32api.SendMessage(hWnd, WM_APPCOMMAND, 0, APPCOMMAND_MEDIA_PAUSE << 16)
        else:
            return{"response":"Default media player not found."}
    except Exception as e:
        return{"response":f"Error pausing audio: {e}"}

def resume_audio_windows():
    try:
        system = platform.system()
        if system != 'Windows':
            return{"response":"This function is only supported on Windows."}
            return
        
        hWnd = win32gui.FindWindow(None, 'Media Player')
        if hWnd:
            # Use win32api to send the WM_APPCOMMAND message for resuming
            win32api.SendMessage(hWnd, WM_APPCOMMAND, 0, APPCOMMAND_MEDIA_PLAY_PAUSE << 16)
            
        else:
            return{"response":"Default media player not found."}
    except Exception as e:
        return{"response":f"Error resuming audio: {e}"}

def extract_command_details(command):
    try:
        # Define regex patterns
        play_pattern = r'(?:play)\s+(.+?)$'
        pause_pattern = r'(?:pause)(?:\s+(.+?))?$'
        resume_pattern = r'(?:resume)(?:\s+(.+?))?$'
            
        if 'play' in command:
            return 'play', re.match(play_pattern, command).group(1)
        elif  'pause' in command:
            return 'pause', re.match(pause_pattern, command).group(1)
        elif  'resume' in command:
            return 'resume', re.match(resume_pattern, command).group(1)
        else:
            return None, None
    except Exception as e:
        return{"response":f"Error extracting command details: {e}"}
    
def play_song(cmd):
    try:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        cmd=cmd.lower().replace('song','').replace('the','').replace("music",'')
        action, song_name = extract_command_details(cmd)
        
        if action == 'play':
            file_path = search_and_download_song(song_name)
            if file_path:
                play_audio(file_path)
            return{"response":f"Playing the song {cmd.replace('song','').replace('the','').replace('play','')}."}
        elif action == 'pause':
            pause_audio_windows()
            return{"response":f"Pausing the song {cmd.replace('song','').replace('the','').replace('pause','')}."}
        elif action == 'resume':
            resume_audio_windows()
            return{"response":f"Resuming the song {cmd.replace('song','').replace('the','').replace('resume','')}."}
        else:
            return{"response":"Invalid command."}
    except Exception as e:
        return{"response":f"Error playing song: {e}"}

if __name__ == '__main__':
    try:
        song_name =input("Enter the song name: ")

        play_song(song_name)
    except Exception as e:
        print("Error: {e}")
