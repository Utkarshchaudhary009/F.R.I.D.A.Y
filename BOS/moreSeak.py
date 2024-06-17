import threading
import os
import sys
import pygame
import pyttsx3
from textblob import TextBlob
from rich.console import Console
from rich.markdown import Markdown
from gtts import gTTS
from rich import print
import logging
from logging.handlers import RotatingFileHandler

# Initialize rich console
console = Console()

# Get the directory of the current file (lang-detect.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (Brain)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Get the grandparent directory (Friday)
grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

# Add the necessary directories to the Python path
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)

from Brain.services.langDetect import detect_language
# # Setup logging
# def setup_logging():
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     # Set up logging
#     log_file = r'f:\Friday\Brain\data\logs\Friday.log'
#     log_level = logging.DEBUG  # Log everything
#     handler.setLevel(log_level)
#     # Create a RotatingFileHandler to log messages to a file
#     handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
#     # Console handler with colorful output
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
#     # Use colorama styles for different log levels
#     console_formatter = logging.Formatter(f'{Fore.GREEN}%(asctime)s {Style.RESET_ALL}- %(levelname)s - %(message)s')
#     console_handler.setFormatter(console_formatter)
#     logger.addHandler(console_handler)

#     # File handler for errors
#     error_handler = logging.FileHandler('error.log')
#     error_handler.setLevel(logging.ERROR)
#     error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     logger.addHandler(error_handler)

#     return logger


# Setup logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler with rich colorful output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler for errors
    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)

    return logger
logger = setup_logging()
# Function to play audio using pygame
def play_audio(file_path):
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish playing
    pygame.quit()  # Quit pygame to release resources

# Function to generate speech using gTTS and play it
def googlespeak(text, lang='en', output_dir="F:/Friday/brain/data/cache/.speak"):
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
            logger.info(f"Playing existing file for text: {text}")
            play_audio(output_path)
        else:
            logger.info(f"Generating new file for text: {text}")
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=lang, tld='com', lang_check=True)
            # Save the speech to a file
            tts.save(output_path)
            # Play the speech
            play_audio(output_path)
    except Exception as e:
        logger.error(f"Error in googlespeak: {e}")
        raise

# Emotion detection based on keywords
def detect_emotion(text):
    emotion_keywords = {
        "ecstatic": ['ecstatic'],
        "overjoyed": ['overjoyed'],
        "elated": ['elated'],
        "joyful": ['joyful'],
        "happy": ['happy'],
        "cheerful": ['cheerful'],
        "content": ['content'],
        "pleased": ['pleased'],
        "neutral": ['neutral'],
        "indifferent": ['indifferent'],
        "unhappy": ['unhappy'],
        "sad": ['sad'],
        "mournful": ['mournful'],
        "despondent": ['despondent'],
        "melancholy": ['melancholy'],
        "depressed": ['depressed'],
        "devastated": ['devastated'],
        "hopeful": ['hopeful'],
        "optimistic": ['optimistic'],
        "grateful": ['grateful'],
        "inspired": ['inspired'],
        "amused": ['amused'],
        "calm": ['calm'],
        "confused": ['confused'],
        "disappointed": ['disappointed'],
        "frustrated": ['frustrated'],
        "anxious": ['anxious'],
        "overwhelmed": ['overwhelmed'],
        "guilty": ['guilty'],
        "disgusted": ['disgusted'],
        "repulsed": ['repulsed'],
        "detached": ['detached']
    }
    text_lower = text.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(word in text_lower for word in keywords):
            return emotion
    return "unknown"

# Mapping sentiment to emotions and speech characteristics
def get_emotion(sentiment):
    emotion_map = [
        (0.7, "ecstatic", (220, 1.5)),
        (0.6, "overjoyed", (180, 1.4)),
        (0.5, "elated", (190, 1.3)),
        (0.5, "angry", (290, 1.3)),
        (0.4, "joyful", (180, 1.2)),
        (0.3, "happy", (170, 1.1)),
        (0.2, "cheerful", (160, 1.0)),
        (0.1, "content", (150, 0.9)),
        (0.05, "pleased", (140, 0.8)),
        (-0.05, "neutral", (130, 1)),
        (-0.1, "indifferent", (120, 1)),
        (-0.2, "unhappy", (110, 1)),
        (-0.3, "sad", (100, 1)),
        (-0.4, "mournful", (100, 1)),
        (-0.5, "despondent", (170, 1)),
        (-0.6, "melancholy", (170, 0.1)),
        (-0.7, "depressed", (60, 1)),
        (-1, "devastated", (180, 1))
    ]
    for threshold, emotion, (rate, volume) in emotion_map:
        if sentiment >= threshold:
            return emotion, (rate, volume)
    return "unknown", (130, 1)

# Function to track specific emotion phrases
def track_emotion_phrases(text):
    tracked_emotions = {
        "love": ['love', 'romance', 'affection', 'passion', 'adoration'],
        "happy": ['happy', 'joyful', 'pleased', 'content', 'cheerful'],
        "content": ['peaceful', 'serene', 'tranquil', 'calm', 'content'],
        "neutral": ['neutral', 'indifferent', 'calm', 'composed', 'unaffected'],
        "moody": ['moody', 'unsettled', 'irritable', 'restless', 'discontent'],
        "sad": ['sad', 'unhappy', 'mournful', 'disheartened', 'dejected'],
        "angry": ['angry', 'irate', 'furious', 'enraged', 'agitated']
    }
    text_lower = text.lower()
    for emotion, phrases in tracked_emotions.items():
        if any(phrase in text_lower for phrase in phrases):
            return emotion
    return None

# Advanced animated message using rich
def print_animated_message(message):
    try:
        markdown_message = Markdown(message)
        console.print(markdown_message)
    except Exception as e:
        logger.error(f"Error in print_animated_message: {e}")

# Function for text-to-speech synthesis with advanced emotion handling
def speakbasic(text, language):
    try:
        engine = pyttsx3.init()
        
        # Set voice based on language
        voices = engine.getProperty('voices')
        if language == 'hi':
            # Set Hindi voice if available
            hindi_voice = next((voice for voice in voices if 'hindi' in voice.languages), None)
            if hindi_voice:
                engine.setProperty('voice', hindi_voice.id)
            else:
                logger.info("Hindi voice not available, using English voice.")
                googlespeak(text)
                return
        else:
            # Set English voice (attempt to find "Mark" or fallback to the first English voice)
            mark_voice = next((voice for voice in voices if 'mark' in voice.id.lower()), None)
            if mark_voice:
                engine.setProperty('voice', mark_voice.id)
            else:
                engine.setProperty('voice', voices[0].id)  # Fallback to the first available voice

        # Analyze sentiment and determine emotion
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        emotion, (adjusted_rate, adjusted_volume) = get_emotion(sentiment)

        # Track specific emotion phrases
        tracked_emotion = track_emotion_phrases(text)
        if tracked_emotion:
            emotion = tracked_emotion

        engine.setProperty('rate', adjusted_rate)
        engine.setProperty('volume', adjusted_volume)
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        logger.error(f"Error in speakbasic: {e}")
        raise

# Function to handle threading for speaking and animated printing
def speak(text):
    try:
        # Detect language of the text
        language = detect_language(text)
    except Exception as e:
        language = 'en'  # Default to English if detection fails
    print(language)
    speak_thread = threading.Thread(target=speakbasic, args=(text, language))
    speak_thread.start()

    print_thread = threading.Thread(target=print_animated_message, args=(text,))
    print_thread.start()

    speak_thread.join()
    print_thread.join()

# Example usage
if __name__ == "__main__":
    text = "नरक"
    speak(text)
