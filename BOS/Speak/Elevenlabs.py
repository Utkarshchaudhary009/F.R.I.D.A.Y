import os
import sys
import uuid
from rich.console import Console
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import pygame

console = Console()

# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Brain.utilities.readEnv import readEnv  # Absolute import

# Constants
ELEVENLABS_API_KEY = readEnv("ELEVENLABS_API_KEY")
OUTPUT_DIR = "F:/Friday/brain/data/cache/.speak/elevenlabs"  # Output directory for saving audio files
print(ELEVENLABS_API_KEY)

# Initialize Eleven Labs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def save_audio(audio_generator, output_path):
    with open(output_path, 'wb') as f:
        for chunk in audio_generator:
            f.write(chunk)

def play_audio(file_path):
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
    pygame.quit()  # Quit pygame to release resources

def elevenlabs_speak(text, lang='en'):
    try:
        # Ensure the output directory exists
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Generate a unique filename for the audio file
        output_file = f"{str(uuid.uuid4())[:8]}.mp3"
        output_path = os.path.join(OUTPUT_DIR, output_file)

        # Check if the file already exists
        if os.path.isfile(output_path):
            console.print(f"[bold blue]Playing existing file for text: [/bold blue][bold green]{text}[/bold green]")
            play_audio(output_path)
        else:
            console.print(f"[bold blue]Generating new file for text: [/bold blue][bold green]{text}[/bold green]")

            # Generate audio using Eleven Labs SDK
            audio_generator = client.generate(
                text=text,
                voice="Rachel",  # Replace with desired voice
                model="eleven_multilingual_v2"  # Replace with desired model
            )

            # Save audio to file
            save_audio(audio_generator, output_path)

            # Play the audio
            play_audio(output_path)

            # Also play audio directly using SDK's play function
            play(audio_generator)

    except Exception as e:
        console.print(f"Error with Eleven Labs TTS: [bold red]{e}[/bold red]")

if __name__ == "__main__":
    while True:
        text = console.input("[bold violet]Enter the text you want the computer to speak: [/bold violet]")
        elevenlabs_speak(text)
