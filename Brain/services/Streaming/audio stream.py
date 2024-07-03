import threading
from flask import Flask, Response, send_file
import subprocess
import os

app = Flask(__name__)

# Path to your video file
VIDEO_FILE_PATH = "X:/video/Harry_Potter_and_the_Deathly_Hallows_Part_2_2011_Hindi_Dubbed_Full_Movie_BDRip_(FilmyZilla.cc).mp4"

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
        command = [
            'ffmpeg',
            '-i', VIDEO_FILE_PATH,
            '-f', 'wav',
            '-ac', '2',  # 2 channels (stereo)
            '-ar', '44100',  # 44100 Hz sample rate
            '-'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            data = process.stdout.read(4096)
            # print(data)
            if not data:
                break
            yield data

    return Response(generate(), mimetype="audio/wav")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
