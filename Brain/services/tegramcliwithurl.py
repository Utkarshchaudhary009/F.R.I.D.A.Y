import os
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from plyer import notification

# Constants
BASE_DIR = 'f:\\Friday\\'
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

# Setup directories
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to sanitize query for filename
def sanitize_query(query):
    return re.sub(r'[^\w\s-]', '', query)

# Function to notify download start
def notify_download_start(media_title, media_type):
    notification_title = "Download Started"
    notification_message = f"Downloading {media_type}: {media_title}"
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name='Telegram CLI',
        timeout=5
    )

# Function to notify download end
def notify_download_end(media_title, media_type):
    notification_title = "Download Completed"
    notification_message = f"Downloaded {media_type}: {media_title}"
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name='Telegram CLI',
        timeout=5
    )

# Function to search Telegram channels
def search_channels(query):
    url = f'https://t.me/s/{query}'
    return url

# Function to list media in a Telegram channel
def list_media(query, media_type):
    channel_url=search_channels(query)
    response = requests.get(channel_url)
    # print(response)
    while True:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup)
            media_links = []
            if media_type.lower() == 'photo':
                for link in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                    media_links.append(link['href'])
            elif media_type.lower() == 'video':
                for link in soup.find_all('a', class_='tgme_widget_message_video_wrap'):
                    media_links.append(link['href'])
            return media_links
            
        else:
            print("Error: Unable to list media.")
            return []
# # Function to search Telegram channels
# def search_channels(query):
#     url = f'https://t.me/s/{query}'
#     print(url)
#     response = requests.get(url)
#     print(response)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print(soup)
#         channels = []
#         for link in soup.find_all('a', class_='tgme_channel_info_header_title'):
#             channel_name = link.get_text()
#             channel_url = link['href']
#             channels.append({'name': channel_name, 'url': channel_url})
#         return channels
#     else:
#         print("Error: Unable to search channels.")
#         return []

# # Function to list media in a Telegram channel
# def list_media(channel_url, media_type):
#     response = requests.get(channel_url)
#     print(response)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print(soup)
#         media_links = []
#         if media_type.lower() == 'photo':
#             for link in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
#                 media_links.append(link['href'])
#         elif media_type.lower() == 'video':
#             for link in soup.find_all('a', class_='tgme_widget_message_video_wrap'):
#                 media_links.append(link['href'])
#         return media_links
#     else:
#         print("Error: Unable to list media.")
#         return []

# Function to download media from a URL
def download_media(media_url, media_type):
    media_id = media_url.split('/')[-1]
    print(f"Media ID: {media_id}, Media URL: {media_url}")
    
    # First request to get the page content
    response = requests.get(media_url)
    print(f"Initial request status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(f"Parsed HTML: {soup.prettify()}")
        
        media_links = []
        for link in soup.find_all('meta', property='og:image'):
            media_links.append(link['content'])
        
        # print(f"Found media links: {media_links}")
        
        if media_links:
            # Update the media_url to the actual media link
            media_url = media_links[0]

    # Second request to download the media
    response = requests.get(media_url, stream=True)
    # print(f"Download request status: {response.status_code}")
    
    if response.status_code == 200:
        file_extension = 'jpg' if media_type.lower() == 'photo' else 'mp4'
        file_path = os.path.join(DOWNLOAD_DIR, f'{media_id}.{file_extension}')
        
        notify_download_start(media_id, media_type)
        
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, desc=f'Downloading {media_id}.{file_extension}')

        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        notify_download_end(media_id, media_type)
        print(f"Downloaded {media_type}: {media_id}")


def main():
    while True:
        print("\n1. Search channels")
        print("2. List media from a channel")
        print("3. Download media")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            query = input("Enter search query: ")
            channels = search_channels(query)
            for idx, channel in enumerate(channels, start=1):
                print(f"{idx}. Name: {channel['name']}, URL: {channel['url']}")

        elif choice == '2':
            channel_url = input("Enter channel URL: ")
            media_type = input("Enter media type (photo/video): ")
            media_links = list_media(channel_url, media_type)
            for idx, link in enumerate(media_links, start=1):
                print(f"{idx}. Media URL: {link}")

        elif choice == '3':
            media_url = input("Enter media URL: ")
            media_type = input("Enter media type (photo/video): ")
            download_media(media_url, media_type)

        elif choice == '4':
            print

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
