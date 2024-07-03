from rich.console import Console
from rich.progress import track
from textblob import TextBlob
from Speak.googlespeak import googlespeak
console = Console()
from NetHyTech_Pyttsx3_Speak import speak as NetHyTech_Speak
from Speak.playHT import playHT
# # Emotion detection based on keywords
# def detect_emotion(text):
#     emotion_keywords = {
#         "ecstatic": ['ecstatic'],
#         "overjoyed": ['overjoyed'],
#         "elated": ['elated'],
#         "joyful": ['joyful'],
#         "happy": ['happy'],
#         "cheerful": ['cheerful'],
#         "content": ['content'],
#         "pleased": ['pleased'],
#         "neutral": ['neutral'],
#         "indifferent": ['indifferent'],
#         "unhappy": ['unhappy'],
#         "sad": ['sad'],
#         "mournful": ['mournful'],
#         "despondent": ['despondent'],
#         "melancholy": ['melancholy'],
#         "depressed": ['depressed'],
#         "devastated": ['devastated'],
#         "hopeful": ['hopeful'],
#         "optimistic": ['optimistic'],
#         "grateful": ['grateful'],
#         "inspired": ['inspired'],
#         "amused": ['amused'],
#         "calm": ['calm'],
#         "confused": ['confused'],
#         "disappointed": ['disappointed'],
#         "frustrated": ['frustrated'],
#         "anxious": ['anxious'],
#         "overwhelmed": ['overwhelmed'],
#         "guilty": ['guilty'],
#         "disgusted": ['disgusted'],
#         "repulsed": ['repulsed'],
#         "detached": ['detached']
#     }
#     text_lower = text.lower()
#     for emotion, keywords in emotion_keywords.items():
#         if any(word in text_lower for word in keywords):
#             return emotion
#     return "unknown"

# # Mapping sentiment to emotions and speech characteristics
# def get_emotion(sentiment):
#     emotion_map = [
#         (0.7, "ecstatic", (220, 1.5)),
#         (0.6, "overjoyed", (180, 1.4)),
#         (0.5, "elated", (190, 1.3)),
#         (0.5, "angry", (290, 1.3)),
#         (0.4, "joyful", (180, 1.2)),
#         (0.3, "happy", (170, 1.1)),
#         (0.2, "cheerful", (160, 1.0)),
#         (0.1, "content", (150, 0.9)),
#         (0.05, "pleased", (140, 0.8)),
#         (-0.05, "neutral", (130, 1)),
#         (-0.1, "indifferent", (120, 1)),
#         (-0.2, "unhappy", (110, 1)),
#         (-0.3, "sad", (100, 1)),
#         (-0.4, "mournful", (100, 1)),
#         (-0.5, "despondent", (170, 1)),
#         (-0.6, "melancholy", (170, 0.1)),
#         (-0.7, "depressed", (60, 1)),
#         (-1, "devastated", (180, 1))
#     ]
#     for threshold, emotion, (rate, volume) in emotion_map:
#         if sentiment >= threshold:
#             return emotion, (rate, volume)
#     return "unknown", (130, 1)

# # Function to track specific emotion phrases
# def track_emotion_phrases(text):
#     tracked_emotions = {
#         "love": ['love', 'romance', 'affection', 'passion', 'adoration'],
#         "happy": ['happy', 'joyful', 'pleased', 'content', 'cheerful'],
#         "content": ['peaceful', 'serene', 'tranquil', 'calm', 'content'],
#         "neutral": ['neutral', 'indifferent', 'calm', 'composed', 'unaffected'],
#         "moody": ['moody', 'unsettled', 'irritable', 'restless', 'discontent'],
#         "sad": ['sad', 'unhappy', 'mournful', 'disheartened', 'dejected'],
#         "angry": ['angry', 'irate', 'furious', 'enraged', 'agitated']
#     }
#     text_lower = text.lower()
#     for emotion, phrases in tracked_emotions.items():
#         if any(phrase in text_lower for phrase in phrases):
#             return emotion
#     return None

# # Function for text-to-speech synthesis with advanced emotion handling
# def pyttsx(text):
#     try:
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
#         # Set English voice (attempt to find "Mark" or fallback to the first English voice)
#         mark_voice = next((voice for voice in voices if 'mark' in voice.id.lower()), None)
#         if mark_voice:
#             engine.setProperty('voice', mark_voice.id)
#         else:
#             engine.setProperty('voice', voices[0].id)  # Fallback to the first available voice

#         # Analyze sentiment and determine emotion
#         blob = TextBlob(text)
#         sentiment = blob.sentiment.polarity
#         emotion, (adjusted_rate, adjusted_volume) = get_emotion(sentiment)

#         # Track specific emotion phrases
#         tracked_emotion = track_emotion_phrases(text)
#         if tracked_emotion:
#             emotion = tracked_emotion

#         engine.setProperty('rate', adjusted_rate)
#         engine.setProperty('volume', adjusted_volume)
#         engine.say(text)
#         engine.runAndWait()
#         console.print(f"Text spoken using pyttsx3: [bold green]{text}[/bold green]")
#     except Exception as e:
#         console.print(f"Error with pyttsx3: [bold red]{e}[/bold red]")
def speak(text):
    try:
         playHT(text)
    except:
        try:
                # pyttsx(text)
                NetHyTech_Speak(text,1)
        except Exception as e:
            console.print(f"Google TTS failed, falling back to pyttsx3: [bold yellow]{e}[/bold yellow]")
            try:
                googlespeak(text)
            except Exception as e:
                console.print(f"An error occurred: [bold red]{e}[/bold red]")

if __name__ == "__main__":
    while True:
        # text = console.input("[bold voilet]Enter the text you want the computer to speak: [/bold voilet]")
        text = console.input("[bold voilet]Enter the text you want the computer to speak: [/bold voilet]")
        speak(text)
