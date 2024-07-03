from PIL import Image
import ascii_magic

def image_to_ascii(image_path, width=80):
    # Open image file
    image = Image.open(image_path)
    
    # Print the image size
    print(f"Image size: {image.size}")
    
    # Convert image to ASCII art with specified width
    ascii_art = ascii_magic.from_image(image_path)
    
    # Convert AsciiArt object to string formatted for terminal and return it
    ascii_art_str = ascii_art.to_terminal()
    return ascii_art_str

# Example usage
image_path = r"F:\code\project\Next.js\nature\public\bg\240_F_725928054_uzfzc8q1dzIrEm9f1YWhfESHJkbfD8NC.jpg"
ascii_art = image_to_ascii(image_path)
print(ascii_art)
import os
import json
import hashlib
import logging
import re
import aiohttp
import asyncio
import requests
from pytube import YouTube, Search
from mutagen.mp4 import MP4, MP4Cover
from threading import Thread, Event
from plyer import notification

# Constants
BASE_DIR = 'F:\\Friday\\'
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads\\Youtube')
METADATA_DIR = os.path.join(BASE_DIR, 'brain\\data\\Youtube')
CACHE_DIR = os.path.join(BASE_DIR, 'brain\\data\\cache\\Youtube')
LOG_DIR = os.path.join(BASE_DIR, 'brain\\data\\logs')

# Setup logging and directories
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(LOG_DIR, 'youtube_cli.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_metadata():
    try:
        metadata_file = os.path.join(METADATA_DIR, 'metadata.json')
        if not os.path.exists(metadata_file):
            with open(metadata_file, 'w') as f:
                json.dump({}, f)
        
        with open(metadata_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading metadata: {e}")
        return {}

def save_metadata(metadata):
    try:
        metadata_file = os.path.join(METADATA_DIR, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving metadata: {e}")

def sanitize_query(query):
    return re.sub(r'[^\w\s-]', '', query)

def get_cache_filename(query):
    hashed_query = hashlib.md5(query.encode()).hexdigest()
    return f"{hashed_query}.json"

def load_search_cache(query):
    cache_file = os.path.join(CACHE_DIR, get_cache_filename(query))
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def save_search_cache(query, data):
    try:
        cache_file = os.path.join(CACHE_DIR, get_cache_filename(query))
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving search cache for {query}: {e}")

async def fetch_video_info(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return await response.json()
                else:
                    html_content = await response.text()
                    # Process the HTML content if necessary
                    logging.warning(f"Received HTML content instead of JSON for URL: {url}")
                    return html_content
            else:
                logging.error(f"Error fetching video info: {response.status}")
                return None
    except aiohttp.ClientResponseError as e:
        logging.error(f"Client response error during fetch: {e}")
    except aiohttp.ClientConnectionError as e:
        logging.error(f"Client connection error during fetch: {e}")
    except aiohttp.ClientPayloadError as e:
        logging.error(f"Client payload error during fetch: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during fetch: {e}")


async def search_videos_async(query):
    cached_results = load_search_cache(query)
    if cached_results:
        logging.info(f"Using cached results for query: {query}")
        return cached_results
    
    try:
        search = Search(query)
        video_list = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for yt in search.results[:70]:  # Get the top 70 results
                tasks.append(fetch_video_info(session, yt.watch_url))

            video_results = await asyncio.gather(*tasks)
            
            for yt, result in zip(search.results[:70], video_results):
                if result:
                    video_info = {
                        "title": yt.title,
                        "author": yt.author,
                        "publish_date": yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown',
                        "description": yt.description,
                        "length": int(yt.length),  # Length in seconds
                        "views": f"{yt.views / 1000:.1f}k" if yt.views < 1_000_000 else f"{yt.views / 1_000_000:.1f}m",
                        "url": yt.watch_url,
                        "thumbnail": yt.thumbnail_url,
                        "download_size": get_video_size(yt.streams.first())  # Download size estimation
                    }
                    video_list.append(video_info)
        
        save_search_cache(query, video_list)
        return video_list
    except KeyError as e:
        logging.warning(f"Unexpected renderer encountered. Renderer name: {e}")
        return []
    except Exception as e:
        logging.error(f"Error during search: {e}")
        return []

def get_video_size(video_stream):
    try:
        response = requests.head(video_stream.url)
        size_in_bytes = int(response.headers.get('Content-Length', 0))
        size_in_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes
        return size_in_mb
    except Exception as e:
        logging.error(f"Error getting video size: {e}")
        return 0

def display_videos(video_list, start_index):
    end_index = min(start_index + 5, len(video_list))
    for idx in range(start_index, end_index):
        video = video_list[idx]
        print(f"{idx + 1}. Title: {video['title']}")
        print(f"   Author: {video['author']}")
        print(f"   Publish Date: {video['publish_date']}")
        print(f"   Description: {video['description']}")
        print(f"   Length: {video['length']} seconds")
        print(f"   Views: {video['views']}")
        print(f"   URL: {video['url']}")
        print(f"   Thumbnail: {video['thumbnail']}")
        print(f"   Estimated Download Size: {video['download_size']:.2f} MB")
        print('-' * 40)

class VideoDownloader(Thread):
    def __init__(self, video, format_choice):
        super().__init__()
        self.video = video
        self.format_choice = format_choice
        self.pause_event = Event()
        self.resume_event = Event()
        self.resume_event.set()

    def run(self):
        try:
            yt = YouTube(self.video['url'])
            video_stream = yt.streams.filter(file_extension='mp4', res=self.format_choice).first()
            
            if not video_stream:
                print(f"No stream found for the chosen format: {self.format_choice}")
                return None
            
            size_in_mb = get_video_size(video_stream)
            
            if not self.confirm_download(size_in_mb):
                print("Download cancelled.")
                return None
            
            sanitized_title = sanitize_query(yt.title)
            file_name = f"{sanitized_title}.mp4"
            file_path = os.path.join(DOWNLOAD_DIR, file_name)

            if not os.path.exists(file_path):
                self.download_with_resume(video_stream, file_path)
            else:
                print(f"File already exists: {yt.title}")
            
            notification.notify(
                title="Download Complete",
                message=f"Download complete: {yt.title}",
                timeout=5
            )
            
        except Exception as e:
            logging.error(f"Error downloading video: {e}")

    def confirm_download(self, size_in_mb):
        print(f"Title: {self.video['title']}")
        print(f"Author: {self.video['author']}")
        print(f"Publish Date: {self.video['publish_date']}")
        print(f"Description: {self.video['description']}")
        print(f"Length: {self.video['length']} seconds")
        print(f"Views: {self.video['views']}")
        print(f"URL: {self.video['url']}")
        print(f"Thumbnail: {self.video['thumbnail']}")
        print(f"Estimated Download Size: {size_in_mb:.2f} MB")
        
        confirm = input("Do you want to download this video? (yes/no): ").strip().lower()
        return confirm == 'yes'

    def sanitize_filename(self, filename):
        sanitized_filename = re.sub(r'[^\w\s-]', '', filename)
        sanitized_filename = re.sub(r'\s+', '_', sanitized_filename)
        return sanitized_filename

    def download_with_resume(self, stream, file_path):
        chunk_size = 1024 * 1024  # 1 MB
        downloaded = 0
        headers = {}

        if os.path.exists(file_path):
            downloaded = os.path.getsize(file_path)
            headers['Range'] = f'bytes={downloaded}-'

        response = requests.get(stream.url, headers=headers, stream=True)
        total_size = int(response.headers.get('Content-Length', 0)) + downloaded

        with open(file_path, 'ab') as f:
            for chunk in response.iter_content(chunk_size):
                self.pause_event.wait()
                self.resume_event.wait()

                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    print(f"Downloaded {downloaded / (1024 * 1024):.2f} MB of {total_size / (1024 * 1024):.2f} MB", end='\r')
        
        self.handle_metadata(self.video['title'], self.video, file_path)

    def handle_metadata(self, title, video_info, file_path):
        try:
            metadata = MP4(file_path)
            metadata['\xa9nam'] = video_info['title']
            metadata['\xa9ART'] = video_info['author']
            metadata['\xa9alb'] = video_info['title']
            metadata['\xa9day'] = video_info['publish_date']
            metadata['desc'] = video_info['description']
            metadata['\xa9gen'] = 'YouTube'
            
            # Download and embed thumbnail
            thumbnail_data = requests.get(video_info['thumbnail']).content
            cover = MP4Cover(thumbnail_data, imageformat=MP4Cover.FORMAT_JPEG)
            metadata['covr'] = [cover]
            
            metadata.save()
            
            # Save metadata to JSON
            metadata_dict = load_metadata()
            metadata_dict[title] = video_info
            save_metadata(metadata_dict)
            
        except Exception as e:
            logging.error(f"Error handling metadata: {e}")

    def pause(self):
        self.pause_event.set()
        self.resume_event.clear()
        print("Download paused.")

    def resume(self):
        self.pause_event.clear()
        self.resume_event.set()
        print("Download resumed.")

def main():
    metadata = load_metadata()
    
    while True:
        query = input("Enter search query: ").strip()
        if not query:
            break
        
        video_list = asyncio.run(search_videos_async(query))
        
        if not video_list:
            print("No results found.")
            continue
        
        start_index = 0
        while True:
            display_videos(video_list, start_index)
            
            print("Commands: next, prev, download [index], pause, resume, quit")
            command = input("Enter command: ").strip().lower()
            
            if command == 'next':
                if start_index + 5 < len(video_list):
                    start_index += 5
                else:
                    print("No more videos.")
            elif command == 'prev':
                if start_index - 5 >= 0:
                    start_index -= 5
                else:
                    print("Already at the first page.")
            elif command.startswith('download'):
                parts = command.split()
                if len(parts) == 2 and parts[1].isdigit():
                    index = int(parts[1]) - 1
                    if 0 <= index < len(video_list):
                        format_choice = input("Enter format (360p, 720p, 1080p): ").strip().lower()
                        downloader = VideoDownloader(video_list[index], format_choice)
                        downloader.start()
                    else:
                        print("Invalid index.")
                else:
                    print("Invalid download command. Use 'download [index]'.")
            elif command == 'pause':
                if 'downloader' in locals():
                    downloader.pause()
            elif command == 'resume':
                if 'downloader' in locals():
                    downloader.resume()
            elif command == 'quit':
                break
            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()
