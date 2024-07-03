import speech_recognition as sr
import sys
from rich.console import Console
from speak import speak

# Initialize Console
console = Console()

# Add the parent directory of the current file (Moniter_System.py)
sys.path.append(r'F:\Friday')  # Replace 'F:\Friday' with the actual path to the parent directory
# from Brain.services.Translator import translate_text

def listen(timeout=10, phrase_time_limit=30, energy_threshold=300, adjust_for_ambient_noise_duration=1):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Optionally adjust for ambient noise
        if adjust_for_ambient_noise_duration:
            r.adjust_for_ambient_noise(source, duration=adjust_for_ambient_noise_duration)
        
        # Set energy threshold for better accuracy
        r.energy_threshold = energy_threshold
        
        console.print("[bold white]Say something...[/bold white]")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            console.print("[bold red]Listening timed out while waiting for phrase to start.[/bold red]")
            return "unable to listen please try again sir..."
        
    try:
        text = r.recognize_google(audio)
        console.print(text)
        # return translate_to_english(text)
        return text
    except:
        console.print("[bold red]Google Speech Recognition could not understand audio. Trying offline...[/bold red]")
        try:
            text = r.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            console.print("[bold red]Offline recognition failed as well.[/bold red]")
            return "None"
        except sr.RequestError as e:
            console.print(f"[bold red]Sphinx error; {e}[/bold red]")
            return "None"

# def translate_to_english(text):
#     translated_text = translate_text(text, target_code="en")
#     if translated_text and translated_text.get("data"):
#         translated_text = translated_text["data"]["text"]
#         console.print(f"[bold green]Translation: {translated_text}[/bold green]")
#         return translated_text
#     else:
#         return text

if __name__ == "__main__":
    while True:
        text = listen()
        if text:
            speak(text)
        else:
            console.print("[bold red]Failed to recognize speech.[/bold red]")
