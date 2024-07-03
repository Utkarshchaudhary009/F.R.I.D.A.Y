from gtts import gTTS
import os
import pygame
from rich.console import Console
from textblob import TextBlob
console = Console()
def play_audio(file_path):
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
    pygame.quit()  # Quit pygame to release resources

def googlespeak(text, lang='en', output_dir="F:/Friday/brain/data/cache/.speak/google"):
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate a unique filename based on the text
        safe_text = "".join(x for x in text if x.isalnum())
        output_file = f"{safe_text}.mp3"
        output_path = os.path.join(output_dir, output_file)
        
        # Check if the file already exists
        if os.path.isfile(output_path):
            console.print(f"[bold blue]Playing existing file for text: [/bold blue][bold green]{text}[/bold green]")
            play_audio(output_path)
        else:
            console.print(f"[bold blue]Generating new file for text: [/bold blue][bold green]{text}[/bold green]")
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=lang, tld='com', lang_check=True)
            # Save the speech to a file
            tts.save(output_path)
            # Play the speech
            play_audio(output_path)
    except Exception as e:
        console.print(f"Error with Google TTS: [bold red]{e}[/bold red]")

if __name__ == "__main__":
    text = console.input("[bold voilet]Enter the text you want the computer to speak: [/bold voilet]")
    googlespeak(text)
