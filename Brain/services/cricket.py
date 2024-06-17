import subprocess
import requests
import random
from bs4 import BeautifulSoup
import time  
import os
from selenium.webdriver.common.by import By
import re
import spacy
import joblib
from urllib.parse import quote_plus
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
  
# Import the setup_selenium function
try:
    from Brain.data.scripts.setup_selenium import setup_selenium
    from Brain.services.summry import summarize_text
except ImportError as e:
    print("Failed to import setup_selenium. Ensure the path is correct and the module exists.")
    raise e

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def clean_query(query):
    # Tokenize the query
    doc = nlp(query.lower())
    # Words to exclude
    exclude_words = {
        "tell", "information","all", "detail", "about", "summarize", "summary", "explain"
    }
    # Parts of speech to exclude
    exclude_pos = {"PRON", "DET", "CCONJ", "PUNCT", "ADP"}
    # Filter out words and parts of speech to exclude
    cleaned_words = [token.text for token in doc if token.text not in exclude_words and token.pos_ not in exclude_pos]
    # Join the remaining words
    cleaned_query = " ".join(cleaned_words)
    return cleaned_query

def extract_match_id(url):
    match = re.search(r'live-cricket-scores/(\d+)', url)
    if match:
        return match.group(1).replace("-"," ")
    return None

def google_search(url):
    # Path to your webdriver. Replace 'chromedriver' with the name of your WebDriver if using a different browser.
    driver = setup_selenium()
    driver.get(url)

    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    urls = [result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for result in search_results]
    print(urls[0])
    driver.quit()
    return urls[0]
    
def matchId(query):
    cquery=clean_query(query).replace(" "," vs ")
    # Example usage:
    site = "site:https://www.cricbuzz.com/live-cricket-scores/"
        # Format the Google search URL
    
    search_query = f"{cquery} {site}"
    encoded_query = quote_plus(search_query)
    google_url = f"https://www.google.com/search?q={encoded_query}"
    print(google_url)
    match_id=extract_match_id(google_search(google_url))
    print(match_id)
    return match_id

def classify_match(match):
    if (
        match.get('livescore') != 'Data Not Found' or
        match.get('runrate') != 'CRR: Data Not Found' or
        match.get('batterone') != 'Data Not Found' or
        match.get('batsmanonerun') != 'Data Not Found' or
        match.get('batsmanoneball') != '(Data Not Found)' or
        match.get('batsmanonesr') != 'Data Not Found' or
        match.get('battertwo') != 'Data Not Found' or
        match.get('batsmantworun') != 'Data Not Found' or
        match.get('batsmantwoball') != '(Data Not Found)' or
        match.get('batsmantwosr') != 'Data Not Found' or
        match.get('bowlerone') != 'Data Not Found' or
        match.get('bowleroneover') != 'Data Not Found' or
        match.get('bowleronerun') != 'Data Not Found' or
        match.get('bowleronewickers') != 'Data Not Found' or
        match.get('bowleroneeconomy') != 'Data Not Found' or
        match.get('bowlertwo') != 'Data Not Found' or
        match.get('bowlertwoover') != 'Data Not Found' or
        match.get('bowlertworun') != 'Data Not Found' or
        match.get('bowlertwowickers') != 'Data Not Found' or
        match.get('bowlertwoeconomy') != 'Data Not Found'
    ):
        return {"type":"live","response":f"In {match.get('title')} the live score is {match.get('livescore')}.{match.get('batterone')} has scored {match.get('batsmanonerun')} in {match.get('batsmanoneball')} balls. {match.get('battertwo')} has scored {match.get('batsmantworun')} in {match.get('batsmantwoball')} balls. currenlty {match.get('bowlerone')} is balling. he has given {match.get('bowleronerun')} rund in {match.get('bowleroneover')} overs."}
    else:
        return {"type":"result","response":f"In {match.get('title')} {match.get('update')} "}
def extract_teams(url):
    # Updated regular expression to handle more complex URL structures
    match = re.search(r'/([a-z]{2,3}-vs-[a-z]{2,3})-', url)
    if match:
        return match.group(1)
    return None

def score(query):
    # Give the Flask app some time to start
    time.sleep(5)
    # Match
    match_id = matchId(query)

    # Fetch the score
    try:
        response = requests.get(f'http://127.0.0.1:1000/score?id={match_id}')
        if response.status_code == 200:
            data = response.json()
            print(classify_match(data))
        else:
            print(f'Error: Received status code {response.status_code}')
    except requests.ConnectionError:
        print('Connection issue')

def cricket(cmd):
    
    # Start the Flask app
    subprocess.Popen(['python', '-u', "f:/Friday/Brain/services/cricket-api/api/index.py"])
    # cmd = clean_query(cmd)
    
    # google_url = "https://www.google.com/search?q=cricket&oq=cricket&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIOCAEQRRgnGDsYgAQYigUyBggCEEUYOzIGCAMQRRg7MhIIBBAuGEMYxwEY0QMYgAQYigUyBggFEEUYPDIGCAYQRRg8MgYIBxBFGDyoAgiwAgE&sourceid=chrome&ie=UTF-8"
    
    driver = setup_selenium()
    # # time.sleep(500)
    # driver.get(google_url)
    
    html_content = driver.page_source
    # driver.quit()
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all match tiles
    matches = soup.find_all('td', class_='liveresults-sports-immersive__match-tile')
    
    # List to hold match details
    match_details = []

    for match in matches:
        match_info = {}
        
        # Extract match stage and match number
        match_stage = match.find('div', class_='imspo_mt__lg-st-co')
        if match_stage:
            match_info['stage'] = match_stage.span.text
        else:
            match_info['stage'] = 'Match stage not available'
        
        # Extract date
        match_date = match.find('div', class_='imspo_mt__pm-inf imspo_mt__pm-infc imspo_mt__date imso-medium-font')
        if match_date:
            match_info['date'] = match_date.text
        else:
            match_info['date'] = 'Date not available'
        
        # Extract teams
        teams = match.find_all('div', class_='ellipsisize kno-fb-ctx')
        if len(teams) >= 2:
            match_info['team1'] = teams[0].span.text
            match_info['team2'] = teams[1].span.text
        else:
            match_info['team1'] = 'Team name not available'
            match_info['team2'] = 'Team name not available'
        
        # Extract start time
        start_time = match.find('div', class_='imspo_mt__game-status')
        if start_time:
            match_info['start_time'] = start_time.text.replace('Starts at ', '')
        else:
            match_info['start_time'] = 'Start time not available'
        
        # Extract match status if available
        match_status = match.find('div', class_='imspo_mt__status imso-medium-font')
        if match_status:
            match_info['status'] = match_status.text
        else:
            match_info['status'] = 'Status not available'
        
        match_details.append(match_info)

    # Print the filtered match details in the desired format
    for details in match_details:
        print("Team 1:", details.get('team1', 'Team name not available'))
        print("Team 2:", details.get('team2', 'Team name not available'))
        print("Match Status:", details.get('status', 'Status not available'))
        print("Day:", details.get('date', 'Date not available'))
        print("Start Time:", details.get('start_time', 'Start time not available'))
        print("--------------------------------------------------")

    # Filter match details based on the command
    if "live" in cmd:
        # filtered_matches = [match for match in match_details if match['date'].lower() == 'today']
        filtered_matches = [match for match in match_details if "chose to in " in match['date'].lower()]
        for details in filtered_matches:
            query=f"{details.get('team1', 'Team name not available')} vs {details.get('team2', 'Team name not available')}"
            res= score(query)
    elif "results" in cmd:
        filtered_matches = [match for match in match_details if match['date'].lower() == 'date not available']
        for details in filtered_matches:
            res= f"In the cricket match between {details.get('team1', 'Team name not available')} and {details.get('team2', 'Team name not available')}. {details.get('status', 'Team name not available')}"
    elif "upcoming" in cmd:
        filtered_matches = [match for match in match_details if match['date'].lower() == 'tomorrow']
        for details in filtered_matches:
            res= f"The cricket match between {details.get('team1', 'Team name not available')} and {details.get('team2', 'Team name not available')} will start at {details.get('start_time', 'Team name not available')}"
    else:
        filtered_matches = []
    return {"response":res}

if __name__=="__main__":
    # Example usage
    cricket("live")
    # cricket("results")
    # cricket("upcoming")