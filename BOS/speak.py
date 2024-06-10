import pyttsx3
from gtts import gTTS
import os
from time import sleep
import sounddevice
import sounddevice as sd
import pygame

def play_audio(file_path):
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
    pygame.quit()  # Quit pygame to release resources

def pyttsx(text):
            rate=160
            volume=1.0
            # Initialize pyttsx3 engine
            engine = pyttsx3.init(driverName='sapi5')
            engine.setProperty('voice', 'Microsoft David Desktop')
            # Set speech rate
            engine.setProperty('rate', rate)

            # Set volume (0.0 to 1.0)
            engine.setProperty('volume', volume)
            

            # Speak the text
            engine.say(text)
            engine.runAndWait()

def googlespeak(text, lang='en', output_dir="F:/Friday/brain/data/cache/.speak"):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a unique filename based on the text
    safe_text = "".join(x for x in text if x.isalnum())
    output_file = f"{safe_text}.mp3"
    output_path = os.path.join(output_dir, output_file)
    
    # Check if the file already exists
    if os.path.isfile(output_path):
        print(f"Playing existing file for text: {text}")
        play_audio(output_path)
    else:
        print(f"Generating new file for text: {text}")
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=lang, tld='com', lang_check=True)
        # Save the speech to a file
        tts.save(output_path)
        # Play the speech
        play_audio(output_path)


def speak(text):
    try:
            googlespeak(text)
    except:
        try:
         pyttsx(text)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    text = input("Enter the text you want the computer to speak: ")
    speak(text)