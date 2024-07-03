import os
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import spacy
import joblib
from urllib.parse import quote_plus
import sys
import json
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

# Load model from file
model = joblib.load('F:\Friday\Brain/models/querysite/gbm_model.pkl')



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

def clean_output(text_list):
    if type(text_list)==type(['']):
        combined_text = ' '.join(text.strip() for text in text_list if text.strip())

        # Use regular expressions to remove citation references like [2], [3][4], etc.
        cleaned_text = re.sub(r'\[\d+\]', '', combined_text)
        cleaned_text = re.sub(r'\[\d+\][\[\d+\]]*', '', cleaned_text)

        # Remove any extra spaces that might result from removing citations
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text
    else:
        return text_list


def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch HTML for URL: {url}")
            return None
    except Exception as e:
        print(f"Error fetching HTML: {e}")
        return None

def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

def extract_sentences_from_paragraphs(soup,site="none"):
    if "site:https://marvelcinematicuniverse.fandom.com" in site:
        # Find the first <div> with the class 'quick-answers__answer-text'
        answer_div = soup.find('div', class_='quick-answers__answer-text')

        if answer_div:
            # Extract the text content
            answer_text = answer_div.get_text(strip=True)
            return clean_output(answer_text)
        else:
            script_tags = soup.find_all('script', {'type': "application/ld+json"})
            if script_tags:
                     for script_tag in script_tags:
                         script_content = script_tag.string
                         if script_content:
                             try:
                                 data = json.loads(script_content)
                                 return clean_output( data["abstract"])
                             except json.JSONDecodeError:
                                 pass
            else:
                meta_tags = soup.find_all('meta', {'name': "description"})
                if meta_tags:
                    return clean_output(meta_tags[0]['content'])
                else:
                    pass
    paragraphs = soup.find_all('p')
    sentences = []
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text()
        doc = nlp(paragraph_text)
        paragraph_sentences = [sent.text for sent in doc.sents]
        sentences.extend(paragraph_sentences)
        # print(sentences)
        if len(sentences) >= 2:
            return sentences
        
    return clean_output(sentences[:2]) if sentences else None

def extract_question_answer_pairs(soup):
    qas = []
    qa_pairs = soup.find_all(['div', 'section', 'article'])
    for qa_section in qa_pairs:
        questions = qa_section.find_all(['h2', 'h3', 'h4', 'strong'])
        answers = qa_section.find_all('p')
        if questions and answers:
            for question, answer in zip(questions, answers):
                question_text = question.get_text().strip()
                answer_text = answer.get_text().strip()
                if question_text and answer_text:
                    qas.append({'question': question_text, 'answer': answer_text})
    return qas[:2] if qas else None

def extract_table_data(soup):
    tables = soup.find_all('table')
    table_data = []
    for table in tables:
        headers = [header.get_text().strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            cell_data = [cell.get_text().strip() for cell in cells]
            if cell_data:
                rows.append(cell_data)
        if headers and rows:
            table_data.append({'headers': headers, 'rows': rows})
    return table_data if table_data else None

def summriser(text):
    summary=summarize_text(text)
    return summary

def google_search(url):
    # Path to your webdriver. Replace 'chromedriver' with the name of your WebDriver if using a different browser.
    driver = setup_selenium()
    driver.get(url)

    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    urls = [result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for result in search_results]
    
    driver.quit()
    return urls[:1]
    
def webSearch(cquery):
    # cquery=clean_query(query)
    # Example usage:
    #site = model.predict([cquery])[0]
        # Format the Google search URL
    
    search_query = f"{cquery}"
    # search_query = f"{cquery} {site}"
    encoded_query = quote_plus(search_query)
    google_url = f"https://www.google.com/search?q={encoded_query}"

    filtered_urls=google_search(google_url)
    if not filtered_urls:
        return "failed google search"
    
    for url in filtered_urls:

        print(url)
        print(google_url)
        html_content = fetch_html(url)
        # print(html_content)
        if not html_content:
            continue

        soup = parse_html(html_content)

        # Priority 1: Extract first two sentences from paragraphs
        sentences = clean_output(extract_sentences_from_paragraphs(soup))
        # sentences = clean_output(extract_sentences_from_paragraphs(soup,site))
        if sentences:
            # print("\n")
            # print(sentences)
            # print("\n")
            summary = {summriser(sentences)}
            # print(summary)
            return summary

        # Priority 2: Extract question-answer pairs
        qas = clean_output(extract_question_answer_pairs(soup))
        if qas:
            qa_texts = ["Q: " + qa['question'] + " A: " + qa['answer'] for qa in qas]
            summary = summriser(" ".join(qa_texts))
            # print(summary)
            return summary

        # Priority 3: Extract table data
        tables = clean_output(extract_table_data(soup))
        if tables:
            table_texts = ["Headers: " + ", ".join(table['headers']) + " Rows: " + ", ".join(["; ".join(row) for row in table['rows']]) for table in tables]
            summary = f"{summriser(' '.join(table_texts))}"
            # print(summary)
            return summary

    print("No relevant data found.")
    return None

# Example usage:
if __name__=="__main__":
    # queries=["what is black hole","who is iron man","upcomming series of marvel"]
    queries = ["What is green business?","What Is a Budget?"]

    # Perform Google search and scrape for each query
    for q in queries:
        print(f"Query: {q}\n")
        print(webSearch(q))
        print("\n")