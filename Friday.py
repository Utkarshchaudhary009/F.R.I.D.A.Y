import threading
import subprocess
import json
import time
from pydub import AudioSegment
from pydub.playback import play
from BOS.listen import listen
from BOS.process import process
from BOS.speak import speak
from BOS.Moniter_System import monitor_system
from BOS.Greeting import advanced_greeting
# Load user configuration
with open('F:/friday/Brain/data/userconfig.json') as file:
    data = json.load(file)

def monitor_system_thread():
    """Start a daemon thread to monitor the system."""
    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.daemon = True  # Daemonize the thread so it terminates with the main thread
    monitor_thread.start()

def play_startup_audio():
    """Play startup audio and synchronize actions with it."""
    sound = AudioSegment.from_mp3("F:/friday/Brain/data/startup.mp3")
    play(sound)
    speak(advanced_greeting(data.get('firstName', 'Mr.Unknown')))

def play_shutdown_audio():
    
    """Play startup audio and synchronize actions with it."""
    sound = AudioSegment.from_mp3("F:/friday/Brain/data/shutdown.mp3")
    play(sound)

# def synchronized_actions():
#     """Perform synchronized actions with the audio playback."""
#     # Assuming the audio file duration is 10 seconds
#     time.sleep(1)  # Assuming "Starting server" should happen at 1 second
#     print("Starting server...")
#     speak("Starting server...")

#     time.sleep(2)  # Assuming "Connecting to server" should happen at 3 seconds
#     print("Connecting to server...")
#     speak("Connecting to server...")

def main():
    # Start the monitor system thread
    monitor_system_thread()

    # Start the Flask server in a separate thread
    flask_app_process = subprocess.Popen(['python', '-u', "f:/Friday/Brain/app.py"])
    
    # Play the startup audio in a separate thread
    audio_thread = threading.Thread(target=play_startup_audio)
    audio_thread.start()

    # # Start synchronized actions in a separate thread
    # sync_thread = threading.Thread(target=synchronized_actions)
    # sync_thread.start()

    time.sleep(25)
    try:
        # Main loop to listen and process commands
        while True:
            command = listen()
            print(command)
            if command.lower() in ['friday stop', 'friday exit', 'friday close', 'friday disconnect', 'friday kill yourself', 'Friday shutdown', 'friday shutdown', 'friday formula 404', 'pride stop']:
                exit_message = f"Ok Sir! Friday is disconnecting. See you later, {data.get('firstName', 'Mr.Unknown')}!"
                print(exit_message)
                speak(exit_message)
                break
            else:
                command = command.lower().replace("friday", "").strip()
                try:
                    response = process(command).get("response", "Sorry, I didn't catch that.")
                except Exception as e:
                    print(f"Error processing command: {e}")
                    response = "Sorry, some error occurred. Please try again."
                print(response)
                speak(response)
    finally:
        # Ensure the Flask app subprocess is terminated
        audio_thread = threading.Thread(target=play_shutdown_audio)
        audio_thread.start()
        flask_app_process.terminate()
        flask_app_process.wait()  # Wait for the subprocess to terminate

if __name__ == "__main__":
    main()
