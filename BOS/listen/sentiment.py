import assemblyai
import spacy

# # AssemblyAI API credentials
# API_KEY = '3e4dd5254c1044adaab5d704f1ccbf7c'

# # Initialize AssemblyAI client
# client = assemblyai.Client(API_KEY)

# def transcribe_audio(audio_url):
#     """Transcribes audio using AssemblyAI."""
#     response = client.transcript.create(audio_url=audio_url)
#     transcript_id = response['id']

#     # Polling for transcription completion
#     while True:
#         result = client.transcript.get(transcript_id)
#         if result['status'] == 'completed':
#             return result['text']
#         elif result['status'] == 'failed':
#             raise Exception("Transcription failed")
#         print("Waiting for transcription to complete...")
#         time.sleep(5)

def analyze_text(text):
    """Analyzes text for entities and sentiment using SpaCy."""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Determine sentiment
    sentiment = analyze_sentiment(text)

    return entities, sentiment

def analyze_sentiment(text):
    """Performs sentiment analysis using SpaCy."""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    sentiment = doc.sentiment
    return sentiment

if __name__ == '__main__':
    # Example usage: transcribe audio from a URL and analyze it
    # audio_url = 'https://your-audio-url-here.com/audio.mp3'
    # transcribed_text = transcribe_audio(audio_url)
    transcribed_text = "i am really sad. i lost my parents."
    print("Transcribed text:")
    print(transcribed_text)

    entities, sentiment = analyze_text(transcribed_text)

    print("\nEntities:")
    for entity, label in entities:
        print(f"{entity} - {label}")

    print("\nSentiment:")
    print(f"Polarity: {sentiment}")
    print(f"Subjectivity: {sentiment}")
