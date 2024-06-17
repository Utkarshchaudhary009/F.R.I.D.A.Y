import requests
import spacy
import wikipediaapi
import re
import sys
import os
# Get the directory of the current file (lang-detect.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (Brain)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Get the grandparent directory (Friday)
grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

# Add the necessary directories to the Python path
sys.path.append(parent_dir)
sys.path.append(grandparent_dir)
from Brain.services.webScrap import webSearch

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

class WikipediaSummaryError(Exception):
    pass

def preprocess_query(query):
    # Process the query using spaCy
    doc = nlp(query)
    # Extract relevant tokens (ignoring stopwords and punctuation)
    filtered_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    # Join tokens back into a string
    cleaned_query = ' '.join(filtered_tokens)
    return cleaned_query

def get_google_knowledge_graph(query):
    api_key = 'AIzaSyDqadZwa9HMk4PG0oZmrTiKhO975bY0kNo'
    try:
        query_key = preprocess_query(query)
        url = f"https://kgsearch.googleapis.com/v1/entities:search"
        params = {
            'query': query_key,
            'key': api_key,
            'limit': 1,
            'indent': True,
        }
        response_CODE = requests.get(url, params=params)
        if response_CODE.status_code == 200:
            data = response_CODE.json()
            if 'itemListElement' in data and data['itemListElement']:
                entity = data['itemListElement'][0]['result']
                detailed_description = entity.get('detailedDescription', {}).get('articleBody', 'No detailed description available')
                if 'No detailed description available' in detailed_description:
                    params['query'] = query  # Retry with the original query
                    response_CODE = requests.get(url, params=params)
                    if response_CODE.status_code == 200:
                        data = response_CODE.json()
                        if 'itemListElement' in data and data['itemListElement']:
                            entity = data['itemListElement'][0]['result']
                            detailed_description = entity.get('detailedDescription', {}).get('articleBody', 'No detailed description available')
                return {"response": detailed_description}
        return "Sorry, I couldn't find the information."
    except:
        return {"response": "Some error occurred, try again after some time"}

def get_wikipedia_summary(query):
    topic = extract_topic(query)

    if topic == None:
        return {"response":webSearch(query)}
    
    # Specify a user agent
    user_agent = 'YourAppName/1.0 (your_email@example.com)'
    
    # Create the Wikipedia object with the user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )
    
    # Fetch the page
    page = wiki_wiki.page(topic)
    
    if page.exists():
        summary = page.summary
        sentences = summary.split('. ')
        two_line_summary = '. '.join(sentences[:2]) + '.'
        return {"response": two_line_summary}
    else:
        raise WikipediaSummaryError(f"The page for '{topic}' does not exist on Wikipedia.")

def extract_topic(command):
    # Define the regex patterns
    pattern1 = re.compile(r'\b(what|when|where|who|how|how much|calculate)\b(.*)', re.IGNORECASE)
    pattern2 = re.compile(r'\b(find detailed information on|look up|search (?:Wikipedia )?for|get details about)\b(.*)', re.IGNORECASE)
    
    # Try to match the second pattern first (as it has longer keywords)
    match2 = pattern2.match(command)
    if match2:
        return match2.group(2).strip()
    
    # Try to match the first pattern
    match1 = pattern1.match(command)
    if match1:
        topic = match1.group(2).strip()
        # Remove auxiliary verbs like 'is', 'does', and 'wrote' at the beginning
        topic = re.sub(r'^(is|does|wrote)\b\s*', '', topic, flags=re.IGNORECASE)
        return topic.strip()
    
    # If no match is found, return None
    return None

def wiki(query):
    try:
        return get_wikipedia_summary(query)
    except :
        try:
            return {"response":webSearch(query)}
        except:
            return get_google_knowledge_graph(query)

# Example usage
commands = [
    "find detailed information on climate change",
    "get details about the solar system",
    "search Wikipedia for DNA structure",
    "look up the GDP of USA",
    "find detailed information on artificial intelligence",
    "get details about the Eiffel Tower",
    "search Wikipedia for renewable energy",
    "what is the boiling point of water",
    "when is the next solar eclipse",
    "where is the Amazon rainforest located",
    "who wrote 'To Kill a Mockingbird'",
    "how does gravity work",
    "how much is the population of China",
    "calculate 7 factorial",
    "what is the speed of light",
    "when was the Declaration of Independence signed",
    "where is Mount Everest"
]

if __name__ == "__main__":
    for command in commands:
        answer = wiki(command)
        print(f"Command: {command}\nSummary: {answer}\n")
