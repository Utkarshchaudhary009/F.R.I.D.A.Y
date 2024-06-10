import requests
import re
import sys
import os
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from Brain.utilities.readEnv import readEnv  # Absolute import
def extract_book_name(command):
    """Extracts the book name from a user command."""

    # Regex patterns for different ways users might phrase the command
    patterns = [
        r"tell me about book (.*)",
        r"tell me about (.*)",
        r"can you tell me about book (.*)",
        r"what is (.*) book about",
        r"give me information about book (.*)",
        r"i want to know about (.*)",
        # Add more patterns as needed
    ]

    for pattern in patterns:
        match = re.search(pattern, command, flags=re.IGNORECASE)
        if match:
            book_name = match.group(1).strip()  # Remove leading/trailing spaces
            return book_name

    # If no pattern matches, return None
    return 
def remove_unnecessary(text):
    # Remove excessive zeros after the decimal point
    text = re.sub(r'\.\d+', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text
def book(argument):
    try:
        book_title=argument.book
    except:
        book_title=extract_book_name(argument)
    if book_title:
        title="+".join(book_title.split())
        base_url = "https://www.googleapis.com/books/v1/volumes"
        api_key = readEnv("GOOGLEAPIES") # Replace 'YOUR_API_KEY' with your actual Google Books API key

        url=f"{base_url}?q={title}&key={api_key}"
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            print("got it")
            data = response.json()
            if data['totalItems'] > 0:
                # Assuming the first book in the list is the one you want
                book_info = data['items'][0]['volumeInfo']
                publish = book_info.get('publishedDate', 'publishedDate not available')
                authors = book_info.get('authors', ['author not available'])
                author= " and ".join(authors)
                title = book_info.get('title', 'Title not available')
                for item in data['items']:  # Iterate through all items
                    description = item['volumeInfo'].get('description', None)
                    if description==None:
                        if 'searchInfo' in item:
                           description = item['searchInfo'].get('textSnippet', None)  # If description found, prioritize it
                print(title) 
                return {"response":remove_unnecessary(f"The book {title} which is written by {author} published on {publish} is about {description}")}
            else:
                return "No book found with that title."
        else:
            return "Failed to fetch data. Check your connection or API key."

if __name__=="__main__":
    # Replace 'The Book Title' with the title you want
    while True:
        book_title = input("enter: ")
        description = book(book_title)
        print(description)
    