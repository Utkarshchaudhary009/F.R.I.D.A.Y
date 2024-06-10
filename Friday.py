import threading
from BOS.listen import listen
from BOS.process import process
from BOS.speak import speak
from BOS.Moniter_System import monitor_system
import subprocess
import json

# Load user configuration
with open('./Brain/data/userconfig.json') as file:
    data = json.load(file)

def monitor_system_thread():
    """Start a daemon thread to monitor the system."""
    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.daemon = True  # Daemonize the thread so it terminates with the main thread
    monitor_thread.start()

if __name__ == "__main__":
    # Start the monitor system thread
    monitor_system_thread()
    
    # Start the subprocess for the Flask application
    flask_app_process = subprocess.Popen(['python', '-u', "f:\\Friday\\Brain\\app.py"])
    
    try:
        # Main loop to listen and process commands
        while True:
            command = listen()
            print(command)
            if command not in ['friday stop','Friday stop','friday exit','Friday exit','friday close','friday disconnect','friday disconnect','Friday close','Friday kill your self','Friday formula 404',]:
                command=command.lower().replace("friday","").replace("Friday",'').strip()
                try:
                    response = process(command).get("response", "Sorry, I didn't catch that.")
                except Exception as e:
                    print(f"Error processing command: {e}")
                    response = "Sorry, some error occurred. Please try again."
                print(response)
                speak(response)
            else:
                exit_message = f"Ok Sir! Friday is disconnecting. See you later, {data.get('firstName', 'Mr.Unknown')}!"
                print(exit_message)
                speak(exit_message)
                break
    finally:
        # Ensure the Flask app subprocess is terminated
        flask_app_process.terminate()
        flask_app_process.wait()  # Wait for the subprocess to terminate
