# # import sounddevice as sd
# # import wavio

# # def record_command(filename, duration=2, samplerate=44100):
# #     print(f"Recording {filename}...")
# #     myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2)
# #     sd.wait()  # Wait until recording is finished
# #     wavio.write(filename, myrecording, samplerate, sampwidth=2)
# #     print(f"Recording saved to {filename}")

# # # Example usage
# # for i in range(1, 21):  # Loop from 1 to 20
# #     filename = f"command_{i}.wav"  # Generate unique filename for each recording
# #     record_command(filename)

# import os
# from pydub import AudioSegment

# # Function to convert audio files to 120-second segments
# def convert_to_segments(input_file, output_directory, segment_length_ms=1200):
#     # Load the audio file
#     audio = AudioSegment.from_file(input_file)
    
#     # Get the duration of the audio in milliseconds
#     audio_length = len(audio)
    
#     # Calculate the number of segments
#     num_segments = audio_length // segment_length_ms
    
#     # Extract and save each segment
#     for i in range(num_segments):
#         start_time = i * segment_length_ms
#         end_time = (i + 1) * segment_length_ms
#         segment = audio[start_time:end_time]
#         segment.export(os.path.join(output_directory, f"segment_{i}.mp3"), format="mp3")

# # Directory containing audio files
# music_directory = "./music"

# # Output directory for segments
# output_directory = "./Sound/music"

# # Create output directory if it doesn't exist
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

# # Iterate over all files in the music directory
# for filename in os.listdir(music_directory):
#     if filename.endswith(".wav") or filename.endswith(".mp3"):
#         # Construct the full path of the input file
#         input_file = os.path.join(music_directory, filename)
        
#         # Convert the input file to segments
#         convert_to_segments(input_file, output_directory)
        
# print("Conversion complete!")
import pyaudio
import wave

def record_audio(filename, duration, sample_rate=44100, chunk_size=1024):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a new stream for recording
    stream = p.open(format=pyaudio.paInt16,  # 16-bit resolution
                    channels=1,              # mono channel
                    rate=sample_rate,        # sample rate
                    input=True,              # input stream
                    frames_per_buffer=chunk_size)  # chunk size

    print("Recording...")

    # Initialize an empty list to store the frames
    frames = []

    # Loop to read audio data from the stream
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded frames as a .wav file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)                     # mono channel
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  # 16-bit resolution
    wf.setframerate(sample_rate)           # sample rate
    wf.writeframes(b''.join(frames))       # write frames to file
    wf.close()

if __name__ == "__main__":
    filename = "output.wav"
    duration = 10  # duration of the recording in seconds
    record_audio(filename, duration)
