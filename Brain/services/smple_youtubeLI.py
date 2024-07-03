import re
import logging
import json
import os
import hashlib
import requests
from pytube import Search, YouTube
from pytube.exceptions import AgeRestrictedError
from mutagen.mp4 import MP4, MP4Cover
from tqdm import tqdm
from plyer import notification
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import tkinter as tk
from tkinter import Label
from PIL import ImageTk

# Constants
BASE_DIR = 'F:\\Friday\\'
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads\\Youtube')
METADATA_DIR = os.path.join(BASE_DIR, 'brain\\data\\Youtube')
CACHE_DIR = os.path.join(BASE_DIR, 'brain\\data\\cache\\Youtube')
IMG_DIR = os.path.join(CACHE_DIR, 'img')
SEARCH_DIR = os.path.join(CACHE_DIR, 'search')
LOG_DIR = os.path.join(BASE_DIR, 'brain\\data\\logs')

COLLAGE_SIZE = (600, 600)  # Size of the collage (width, height)
THUMBNAIL_SIZE = (300, 300)  # Size of each thumbnail in the collage

# Create the download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(SEARCH_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(LOG_DIR, 'youtube_cli.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to load and save metadata
def load_metadata():
    try:
        metadata_file = os.path.join(METADATA_DIR, 'metadata.json')
        if not os.path.exists(metadata_file):
            with open(metadata_file, 'w') as f:
                json.dump({}, f)
        
        with open(metadata_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return {}
    except IOError as e:
        logging.error(f"IO error: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {}

def save_metadata(metadata):
    try:
        metadata_file = os.path.join(METADATA_DIR, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving metadata: {e}")

# Function to sanitize query for filename
def sanitize_query(query):
    return re.sub(r'[^\w\s-]', '', query)

# Function to get cache filename using MD5 hash
def get_cache_filename(query):
    hashed_query = hashlib.md5(query.encode()).hexdigest()
    return f"{hashed_query}.json"

# Loading and saving search cache
def load_search_cache(query):
    cache_file = os.path.join(SEARCH_DIR, get_cache_filename(query))
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def save_search_cache(query, data):
    try:
        cache_file = os.path.join(SEARCH_DIR, get_cache_filename(query))
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving search cache for {query}: {e}")

def search_and_store_videos(query):
    try:
        cached_results = load_search_cache(query)
        if cached_results:
            return cached_results
        
        search = Search(query)
        logging.info(f"search is over with query: {query}")
        video_list = []
        for yt in search.results[:70]:  # Get the top 70 results
            try:      
                logging.info(f"on yt : {yt.title}")
                video_info = {
                    "title": yt.title,
                    "author": yt.author,
                    "publish_date": yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown',
                    "description": yt.description,
                    "length": yt.length,
                    "views": yt.views,
                    "url": yt.watch_url,
                    "thumbnail_url": yt.thumbnail_url,
                    "download_size": get_video_size(yt.streams.filter(progressive=True).first())
                }
                
                video_list.append(video_info)
            
            except Exception as e:
                if isinstance(e, AgeRestrictedError):
                    # Handle age-restricted video here
                    logging.warning(f"Skipping age-restricted video: '{yt.title}'")
                    continue
                else:
                    logging.error(f"Error processing video '{yt.title}': {e}")
        
        # Save search results to cache
        save_search_cache(query, video_list)
        
        return video_list
    
    except Exception as e:
        logging.error(f"Error during search and store: {e}")
        return []

# Function to download and convert thumbnail to low-size grayscale format
def download_thumbnail(url):
    try:
        thumbnail_path = os.path.join(IMG_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.png")
        if os.path.exists(thumbnail_path):
            logging.info(f"Using cached image; {thumbnail_path}")
            return thumbnail_path
        else:
            logging.info(f"Downloading image with URL: {url}")
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((320, 180))  # Resize to small dimensions
            img.save(thumbnail_path, "PNG")
            return thumbnail_path
    except Exception as e:
        logging.error(f"Error downloading or converting thumbnail: {e}")
        return "F:\Friday\Downloads\images.png"
    
def create_and_display_collage(video_list, start_index, root, img_label):
    images = []
    for idx in range(start_index, start_index + 4):
        if idx >= len(video_list):
            break
        video = video_list[idx]
        thumbnail_url = video['thumbnail_url']
        img = Image.open(download_thumbnail(thumbnail_url))
        images.append(img)
    
    collage = Image.new('RGB', COLLAGE_SIZE, color=(255, 255, 255))
    
    # Add images to the collage
    for i, img in enumerate(images):
        img = img.resize(THUMBNAIL_SIZE)
        x = (i % 2) * THUMBNAIL_SIZE[0]
        y = (i // 2) * THUMBNAIL_SIZE[1]
        collage.paste(img, (x, y))
        
        # Add index label with black circular background and white bold text
        draw = ImageDraw.Draw(collage)
        font = ImageFont.truetype("arialbd.ttf", 40)  # Use a bold font
        label = str(start_index + i + 1)
        
        # Calculate text size and position
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        circle_radius = max(text_width, text_height) // 2 + 10
        circle_center = (x + 30, y + 30)
        text_position = (circle_center[0] - text_width // 2, circle_center[1] - text_height // 2)

        # Draw black circle
        draw.ellipse(
            (circle_center[0] - circle_radius, circle_center[1] - circle_radius,
             circle_center[0] + circle_radius, circle_center[1] + circle_radius),
            fill=(0, 0, 0)
        )
        
        # Draw white text with offset to make it thicker
        for offset in [(0,0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((text_position[0] + offset[0], text_position[1] + offset[1]), label, font=font, fill=(255, 255, 255))

    collage_img = ImageTk.PhotoImage(collage)
    img_label.config(image=collage_img)
    img_label.image = collage_img
    root.update()



# Function to display videos
def display_videos(video_list, start_index, root, img_label):
    create_and_display_collage(video_list, start_index, root, img_label)
    
    end_index = min(start_index + 4, len(video_list))
    for idx in range(start_index, end_index):
        video = video_list[idx]
        print(f"{idx + 1}. Title: {video['title']}")
        print(f"   Author: {video['author']}")
        print(f"   Publish Date: {video['publish_date']}")
        print(f"   Description: {video['description']}")
        
        length_hours = int(video['length'] // 3600)
        length_minutes = int((video['length'] % 3600) // 60)
        print(f"   Length: {length_hours} hours {length_minutes} minutes")
        
        views_str = f"{video['views'] / 1_000_000:.1f}M" if video['views'] > 1_000_000 else f"{video['views'] / 1_000:.1f}K" if video['views'] > 1_000 else f"{video['views']}"
        print(f"   Views: {views_str}")
        
        print(f"   URL: {video['url']}")
        print(f"   Estimated Download Size: {video['download_size']:.2f} MB")
        print('-' * 40)

# Function to get video size
def get_video_size(video_stream):
    response = requests.head(video_stream.url)
    size_in_bytes = int(response.headers.get('Content-Length', 0))
    size_in_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes
    return size_in_mb

# Function to confirm download with size display
def confirm_download(video, size_in_mb):
    if 'thumbnail_path' not in video or not os.path.exists(video['thumbnail_path']):
        video['thumbnail_path'] = download_thumbnail(video['thumbnail_url'])
    if video['thumbnail_path']:
        Image.open(video['thumbnail_path'])
    else:
        video['thumbnail_path'] = "F:\Friday\Downloads\images.png"
        
    print(f"Title: {video['title']}")
    print(f"Author: {video['author']}")
    print(f"Publish Date: {video['publish_date']}")
    print(f"Description: {video['description']}")
    print(f"Length: {video['length'] // 60} minutes")
    print(f"Views: {video['views']}")
    print(f"URL: {video['url']}")
    print(f"Estimated Download Size: {size_in_mb:.2f} MB")
    confirmation = input("Do you want to download this video? (y/n): ")
    return confirmation.lower() == 'y'
# Function to print all available streams for a video

def print_available_streams(video, format_choice="none"):
    try:
        yt = YouTube(video['url'])
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
        
        for stream in streams:
            size_in_mb = get_video_size(stream)
            if format_choice == 'detailed':
                print(f"Resolution: {stream.resolution}, Frame Rate: {stream.fps}fps, Estimated Size: {size_in_mb:.2f} MB")
            else:
                print(f"Resolution: {stream.resolution}, Estimated Size: {size_in_mb:.2f} MB")
        
        return streams
    except Exception as e:
        logging.error(f"Error fetching available streams: {e}")
        return []

# Function to download video with metadata
def download_video(video):
    try:
        if 'thumbnail_path' not in video or not video['thumbnail_path']:
            video['thumbnail_path'] = os.path.join(IMG_DIR, f"{hashlib.md5(video['url'].encode()).hexdigest()}.png")

        # Check if thumbnail path exists or download it
        if not os.path.exists(video['thumbnail_path']):
            video['thumbnail_path'] = download_thumbnail(video['thumbnail_url'])

        # Check if thumbnail download failed
        if not video['thumbnail_path']:
            logging.error(f"Thumbnail download failed for video: {video['title']}")
            return
        
        yt = YouTube(video['url'])
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')

        print("Available streams:")
        for i, stream in enumerate(streams, 1):
            size_in_mb = get_video_size(stream)
            print(f"{i}. Resolution: {stream.resolution}, Estimated Size: {size_in_mb:.2f} MB")

        choice = int(input("Choose the stream to download (enter the number): "))
        selected_stream = streams[choice - 1]

        output_path = DOWNLOAD_DIR
        title = sanitize_query(video['title'])
        filename = f"{title}.mp4"

        output_filepath = os.path.join(output_path, filename)
        if os.path.exists(output_filepath):
            print(f"The file '{filename}' already exists. Skipping download.")
            return
        
        if confirm_download(video, size_in_mb):
            notification.notify(
                title='Download Started',
                message=f'Your download for "{video["title"]}" has started.',
                app_name='YouTube CLI'
            )
            print("Starting download...")

            # Download and show progress using tqdm
            with requests.get(selected_stream.url, stream=True) as r, open(output_filepath, 'wb') as f, tqdm(
                    total=size_in_mb, unit='B', unit_scale=True, unit_divisor=1024, desc=video['title']) as bar:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))
            print("Download completed.")

            # Display desktop notification
            notification.notify(
                title="Download Complete",
                message=f"'{video['title']}' has been downloaded and saved to '{output_path}'",
                timeout=10
            )
            # Adding metadata
            print("Adding metadata...")
            mp4_file = MP4(output_filepath)
            mp4_file["\xa9nam"] = video['title']
            mp4_file["\xa9ART"] = video['author']
            mp4_file["\xa9day"] = video['publish_date']
            mp4_file["desc"] = video['description']

            # Adding cover art
            with open(video['thumbnail_path'], "rb") as img_file:
                img_data = img_file.read()
            mp4_file["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_PNG)]

            mp4_file.save()
            print("Metadata added successfully.")

        else:
            print("Download cancelled.")
    except Exception as e:
        logging.error(f"Error during download or metadata addition: {e}")
        print(f"Error: {e}")



def cleanup():
    import os
    import time
    from datetime import datetime, timedelta

    # Specify the directory
    cutoff_time = datetime.now() - timedelta(days=6*30)

    # Iterate through all files in the directory
    for filename in os.listdir(IMG_DIR):
        file_path = os.path.join(IMG_DIR, filename)
        
        # Check if the file is an image
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Get the last modification time
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Check if the file is older than 6 months
            if file_mtime < cutoff_time:
                print(f"Deleting file: {file_path} (last modified: {file_mtime})")
                os.remove(file_path)
    print("System cleanup complete.")



def main():
    metadata = load_metadata()
    cleanup()

    # Initialize Tkinter GUI
    root = tk.Tk()
    root.title("YouTube CLI Collage Viewer")
    img_label = Label(root)
    img_label.pack()

    # Perform search and retrieve video list
    query = input("Enter your search query: ")
    video_list = search_and_store_videos(query)
    if not video_list:
        print("No videos found.")
        root.destroy()
        return

    start_index = 0

    # Function to display collage and video details
    def show_collage():
        display_videos(video_list, start_index, root, img_label)

    # Initial display of collage
    show_collage()

    # Main loop for user interaction
    while True:
        print("Options: [n]ext, [p]revious, [d]ownload <index>, [q]uit")
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == 'n':
            start_index += 4
            if start_index >= len(video_list):
                print("No more videos.")
                start_index -= 4
            else:
                show_collage()
        elif choice == 'p':
            start_index -= 4
            if start_index < 0:
                print("Already at the beginning of the list.")
                start_index = 0
            else:
                show_collage()
        elif choice.startswith('d'):
            try:
                video_index = int(choice[1:].strip()) - 1
                if 0 <= video_index < len(video_list):
                    video = video_list[video_index]
                    download_video(video)
                else:
                    print("Invalid video number.")
            except ValueError:
                print("Invalid choice. Please enter a valid index.")
        elif choice == 'q':
            save_metadata(metadata)
            print("Goodbye!")
            root.destroy()
            return
        else:
            print("Invalid choice. Please enter 'n', 'p', 'd <index>', or 'q'.")

if __name__ == "__main__":
    main()
