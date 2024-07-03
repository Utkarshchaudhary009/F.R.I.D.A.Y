from flask import Flask, Response
import subprocess
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the command to capture system audio using ffmpeg
FFMPEG_CMD = [
    'ffmpeg',
    '-f', 'dshow',  # Use DirectShow for audio capture (Windows-specific)
    '-i', 'audio=Digital Microphone (Cirrus Logic High Definition Audio)',  # Your audio input device
    '-f', 'wav',  # Output format
    '-ac', '2',  # Number of audio channels
    '-ar', '44100',  # Sample rate
    '-'
]

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Audio Stream</title>
    </head>
    <body>
        <audio controls autoplay>
            <source src="/audio" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </body>
    </html>
    """

@app.route('/audio')
def audio():
    def generate():
        process = None
        try:
            process = subprocess.Popen(FFMPEG_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("FFmpeg process started successfully.")
            while True:
                data = process.stdout.read(4096)
                if data:
                    print
                    yield data
                else:
                    ("....."*40)
        except Exception as e:
            logging.error(f"Error in FFmpeg process: {e}")
            if process:
                stderr = process.stderr.read().decode()
                logging.error(f"FFmpeg stderr: {stderr}")
        finally:
            if process:
                process.terminate()
                logging.info("FFmpeg process terminated.")

    return Response(generate(), mimetype="audio/wav")

if __name__ == '__main__':
    try:
        logging.info("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Error starting Flask server: {e}")
