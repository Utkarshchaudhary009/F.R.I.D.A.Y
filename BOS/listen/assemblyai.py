import assemblyai as aai
import time
import wave
import pyaudio

API_KEY = '3e4dd5254c1044adaab5d704f1ccbf7c'

# def record_audio(filename, duration=5):
#     """Records audio from the microphone and saves it to a file."""
#     chunk = 1024  # Record in chunks of 1024 samples
#     sample_format = pyaudio.paInt16  # 16 bits per sample
#     channels = 1
#     fs = 44100  # Record at 44100 samples per second
#     p = pyaudio.PyAudio()  # Create an interface to PortAudio

#     print('Recording...')

#     stream = p.open(format=sample_format,
#                     channels=channels,
#                     rate=fs,
#                     frames_per_buffer=chunk,
#                     input=True)
#     frames = []

#     for _ in range(0, int(fs / chunk * duration)):
#         data = stream.read(chunk)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     print('Finished recording.')

#     wf = wave.open(filename, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(p.get_sample_size(sample_format))
#     wf.setframerate(fs)
#     wf.writeframes(b''.join(frames))
#     wf.close()

def listen(duration=5):
    """Records audio, uploads it, and returns the transcription."""
    filename = 'audio.wav'
    # record_audio(filename, duration)

    # Initialize AssemblyAI client
    aai.settings.api_key = API_KEY
    transcriber = aai.Transcriber()

    # Upload the audio file
    upload = transcriber.upload(filename)

    # Request a transcription
    transcript = transcriber.transcribe(upload['upload_url'])

    # Polling for the transcription result
    while True:
        status = transcriber.poll(transcript['id'])
        if status['status'] == 'completed':
            return status['text']
        elif status['status'] == 'failed':
            raise Exception("Transcription failed")
        print("Waiting for transcription to complete...")
        time.sleep(5)


if __name__ == '__main__':
    print("Listening for 5 seconds...")
    print("Transcription:", listen(5))