import speech_recognition as sr
from speak import speak
import os
import sys
from rich.console import Console
from rich.progress import Progress

# Initialize Console
console = Console()

# Get the parent directory of the current file (Moniter_System.py)
sys.path.append(r'F:\Friday')  # Replace 'F:\Friday' with the actual path to the parent directory

from Brain.services.Translator import translate_text

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        console.print("[bold white]Say something...[/bold white]")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        console.print(text)
        return translate_to_english(text)
    except sr.UnknownValueError:
        console.print("[bold red]Google Speech Recognition could not understand audio. Trying offline...[/bold red]")
        try:
            text = r.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            console.print("[bold red]Offline recognition failed as well.[/bold red]")
            return None
        except sr.RequestError as e:
            console.print(f"[bold red]Sphinx error; {e}[/bold red]")
            return None
    except sr.RequestError as e:
        console.print(f"[bold red]Could not request results from Google Speech Recognition service; {e}[/bold red]")
        return None

def translate_to_english(text):
    from Brain.services.Translator import translate_text
    translated_text = translate_text(text, target_code="en")["data"]
    if not translated_text:
        console.print("[bold green]Translation: {translated_text}[/bold green]")
        return translated_text["text"]
    else:
        return text

if __name__ == "__main__":
    while True:
        text = listen()
        if text:
            speak(text)
        else:
            console.print("[bold red]Failed to recognize speech.[/bold red]")
