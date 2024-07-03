import requests
import hashlib
import os
import json
import uuid
from rich.console import Console
import pygame

console = Console()

# Constants
API_KEY = "2faadb74454d4d11a34823f0f8fe1e2a"
USER_ID = "5kupJPH9pRUzOPSA1f16pbpSZtI3"
BASE_URL = "https://api.play.ht"
CACHE_DIR = 'F:/Friday/brain/data/cache/.speak/playHT'

# Ensure the output directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def generate_cache_key(text, voice_id):
    """Generate a unique cache key based on the text and voice ID."""
    return "Summry of English Litrature."
    # return hashlib.sha256(f"{text}-{voice_id}".encode()).hexdigest()

def save_audio_file(audio_url, cache_key):
    """Download and save audio file from URL."""
    file_path = os.path.join(CACHE_DIR, f"{cache_key}.mp3")
    response = requests.get(audio_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    else:
        console.print(f"Failed to download audio file: {response.status_code} - {response.text}")
        return None

# def get_cloned_voice_id(voice_name):
#     """Get the ID of a cloned voice by its name."""
#     url = f"{BASE_URL}/api/v2/cloned-voices"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY}",
#         "X-USER-ID": USER_ID
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         cloned_voices = response.json()
#         for voice in cloned_voices:
#             if voice['name'].lower() == voice_name.lower():
#                 return voice['id']
#     else:
#         console.print(f"Failed to fetch cloned voices: {response.status_code} - {response.text}")
    return None

def playHT(text):
    """Perform Text-to-Speech using play.ht API with caching and fallback voice."""
    voice_id = r's3://voice-cloning-zero-shot/b3e1ea6f-8c75-4b63-a1dc-15818fea0541/original/manifest.json'
    # voice_id = get_cloned_voice_id("friday")
    # print(voice_id)
    if not voice_id:
        console.print(f"Voice with voice id '{voice_id}' not found. Using default voice.")
        voice_id = "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"  # Default voice if specified voice is not found

    cache_key = generate_cache_key(text, voice_id)
    audio_file_path = os.path.join(CACHE_DIR, f"{cache_key}.mp3")

    if not os.path.exists(audio_file_path):
        url = f"{BASE_URL}/api/v2/tts"
        payload = {
            "text": text,
            "voice": voice_id,
            "output_format": "mp3",
            "voice_engine": "PlayHT2.0",
            "speed": 1,
            "emotion": "female_happy"
        }
        headers = {
            "accept": "text/event-stream",
            "content-type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "X-USER-ID": USER_ID
        }
        response = requests.post(url, json=payload, headers=headers, stream=True)

        if response.status_code == 200:
            audio_url = None
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if "data:" in line:
                        event_data = line.split("data:")[1].strip()
                        try:
                            event_json = json.loads(event_data)
                            print(event_json.get("progress"))
                            if event_json.get("stage") == "complete":
                                audio_url = event_json.get("url")
                                break
                        except Exception as e:
                            console.print(f"Failed to parse event data: {e}")
            if audio_url:
                audio_file_path = save_audio_file(audio_url, cache_key)
            else:
                console.print("Audio URL not found in response.")
                return None
        else:
            console.print(f"Failed to convert text to speech: {response.status_code} - {response.text}")
            return None
    print("num : ",audio_file_path)
    play_audio(audio_file_path)
    return

def play_audio(file_path):
    """Play audio file."""
    if os.path.exists(file_path):
        pygame.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
        pygame.quit()  # Quit pygame to release resources
    else:
        console.print(f"File {file_path} does not exist.")

if __name__ == '__main__':
    # while True:
    #     text = console.input("[bold violet]Enter the text you want the computer to speak: [/bold violet]")
    #     # voice_name = "friday"  # Replace with the desired voice name
#    while True:
        # text = console.input("[bold voilet]Enter the text you want the computer to speak: [/bold voilet]")
        text = console.input("""[bold voilet]Enter: """)
        audio_file_path = playHT(text)
