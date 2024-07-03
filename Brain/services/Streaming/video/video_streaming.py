from flask import Flask, render_template, send_file, abort
import os

app = Flask(__name__)

# Paths to your video files
VIDEO_DIR1 = "X:/video/"
VIDEO_DIR2 = "F:/Friday/Downloads/Youtube"

@app.route('/')
def index():
    # List all video files in the VIDEO_DIR1 and VIDEO_DIR2
    videos = [os.path.join("VIDEO_DIR1", f) for f in os.listdir(VIDEO_DIR1) if f.endswith(('mp4', 'mkv', 'avi', 'mov'))]
    videos += [os.path.join("VIDEO_DIR2", f) for f in os.listdir(VIDEO_DIR2) if f.endswith(('mp4', 'mkv', 'avi', 'mov'))]
    return render_template('index.html', videos=videos)

@app.route('/video/<path:filename>')
def stream_video(filename):
    # Check if the file exists
    if filename.startswith("VIDEO_DIR1"):
        file_path = os.path.join(VIDEO_DIR1, filename[len("VIDEO_DIR1/"):])
    elif filename.startswith("VIDEO_DIR2"):
        file_path = os.path.join(VIDEO_DIR2, filename[len("VIDEO_DIR2/"):])
    else:
        abort(404)

    if not os.path.exists(file_path):
        abort(404)
    
    # Stream the video file
    return render_template('video.html', filename=filename)

@app.route('/video_file/<path:filename>')
def video_file(filename):
    # Serve the video file
    if filename.startswith("VIDEO_DIR1"):
        file_path = os.path.join(VIDEO_DIR1, filename[len("VIDEO_DIR1/"):])
    elif filename.startswith("VIDEO_DIR2"):
        file_path = os.path.join(VIDEO_DIR2, filename[len("VIDEO_DIR2/"):])
    else:
        abort(404)

    if not os.path.exists(file_path):
        abort(404)

    # Return the file directly to ensure original quality
    return send_file(file_path, as_attachment=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
