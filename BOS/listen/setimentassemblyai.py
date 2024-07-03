import assemblyai as aai

# Set your AssemblyAI API key
aai.settings.api_key = "3e4dd5254c1044adaab5d704f1ccbf7c"

def transcribe_audio(audio_url):
    """Transcribe audio using AssemblyAI."""
    config = aai.TranscriptionConfig(iab_categories=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config)
    return transcript

if __name__ == '__main__':
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
    
    transcript = transcribe_audio(audio_url)
    
    # Get the parts of the transcript that were tagged with topics
    for result in transcript.iab_categories.results:
        print(result.text)
        print(f"Timestamp: {result.timestamp.start} - {result.timestamp.end}")
        for label in result.labels:
            print(f"{label.label} ({label.relevance})")
    
    # Get a summary of all topics in the transcript
    for topic, relevance in transcript.iab_categories.summary.items():
        print(f"Audio is {relevance * 100}% relevant to {topic}")
