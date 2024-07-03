import threading
import subprocess
import json
import time
from pydub import AudioSegment
from pydub.playback import play
from colorama import init, Fore, Style
from BOS.listen import listen
from BOS.process import process
from BOS.speak import speak
from BOS.Moniter_System import monitor_system, check_plugin_status
from BOS.Greeting import advanced_greeting
import logging
from logging.handlers import RotatingFileHandler
from rich.console import Console
import os

# Initialize colorama for Windows support
init()

# Load user configuration
with open('F:/friday/Brain/data/userconfig.json') as file:
    data = json.load(file)

# Setup logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Set up logging
    log_file = r'f:\Friday\Brain\data\logs\Friday.log'
    log_level = logging.DEBUG  # Log everything
    # Create a RotatingFileHandler to log messages to a file
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
    # Console handler with colorful output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Use colorama styles for different log levels
    console_formatter = logging.Formatter(f'{Fore.GREEN}%(asctime)s {Style.RESET_ALL}- %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler for errors
    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.addHandler(error_handler)
    logger.setLevel(log_level)
    return logger

logger = setup_logging()

def monitor_system_thread():
    """Start a daemon thread to monitor the system."""
    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.daemon = True
    monitor_thread.start()

def play_startup_audio():
    """Play startup audio and synchronize actions with it."""
    sound = AudioSegment.from_mp3("F:/friday/Brain/data/startup.mp3")
    play(sound)

def play_shutdown_audio():
    """Play shutdown audio."""
    sound = AudioSegment.from_mp3("F:/friday/Brain/data/shutdown.mp3")
    play(sound)

try:
    audio_thread = threading.Thread(target=play_startup_audio)
    audio_thread.start()
    logger.info("Starting Friday...")
    
    # Start the monitor system thread
    monitor_system_thread()
    # Start the Flask server in a separate thread
    flask_app_process = subprocess.Popen(['python', '-u', "f:/Friday/Brain/app.py"])
    # Check plugin status in a separate thread
    plugin_thread = threading.Thread(target=check_plugin_status)
    plugin_thread.start()
    time.sleep(14.5)
    speak(advanced_greeting(data.get('firstName', 'Mr.Unknown')))
    while True:
        # command = listen()
        logger.info(f"Command received: {command}")
        if any(cmd.lower() in command.lower() for cmd in ['friday stop',"system close", 'shutdown', 'friday exit', 'exit', 'friday close', 'friday disconnect', 'friday kill yourself', 'kill yourself', 'Friday shutdown', 'Friday switchoff', 'Switchoff', 'Friday switch off', 'switch off', 'shutdown', 'Friday power off', 'friday power off', 'friday formula 404', 'pride stop']):
            exit_message = f"Ok Sir! Friday is disconnecting. See you later, {data.get('firstName', 'Mr.Unknown')}."
            logger.info(exit_message)
            speak(exit_message)
            # Ensure the Flask app subprocess is terminated
            shutdown_audio_thread = threading.Thread(target=play_shutdown_audio)
            shutdown_audio_thread.start()
            time.sleep(1.1)
            break
        elif command == '' or command == 'but' or command == "None":
            pass
        else:
            command = command.lower().replace("friday", "").strip()
            try:
                response = process(command).get("response", "Sorry, I didn't catch that.")
                if response:
                    logger.info(f"Response: {response}")
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                response = "Sorry, some error occurred. Please try again."
                logger.error(response)
            speak(response)
finally:
    flask_app_process.terminate()
    flask_app_process.wait()  # Wait for the subprocess to terminate
    console = Console()
    console.print("[bold green]Successfully Terminated, Sir[/bold green]")
    os._exit(0)  # Forcefully exit the program
