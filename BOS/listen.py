import speech_recognition as sr
from speak import speak
import os
import sys
# Get the parent directory of the current file (Moniter_System.py)
sys.path.append(r'F:\Friday')  # Replace 'F:\Friday' with the actual path to the parent directory

from Brain.services.Translator import translate_text

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
        return translate_to_english(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio. Trying offline...")
        try:
            text = r.recognize_sphinx(audio)
            return translate_to_english(text)
        except sr.UnknownValueError:
            print("Offline recognition failed as well.")
            return None
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def translate_to_english(text):
    translated_text = translate_text(text, target_code="en")
    print(translated_text)
    return translated_text["data"]["text"]

if __name__ == "__main__":
    while True:
        text = listen()
        if text:
            speak(text)
        else:
            print("Failed to recognize speech.")
