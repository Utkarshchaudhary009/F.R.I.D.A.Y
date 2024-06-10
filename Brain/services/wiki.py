import requests
import spacy

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

def preprocess_query(query):
    # Process the query using spaCy
    doc = nlp(query)
    # Extract relevant tokens (ignoring stopwords and punctuation)
    filtered_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    # Join tokens back into a string
    cleaned_query = ' '.join(filtered_tokens)
   # print(cleaned_query)
    return cleaned_query
def get_google_knowledge_graph(query):
    api_key = 'AIzaSyDqadZwa9HMk4PG0oZmrTiKhO975bY0kNo'
    try:
        query_key=preprocess_query(query)
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
                name = entity.get('name', 'No name available')
                description = entity.get('description', 'No description available')
                detailed_description = entity.get('detailedDescription', {}).get('articleBody', 'No detailed description available')
                #return f"{detailed_description}"
            if 'No detailed description available' in detailed_description:
                    params = {
                        'query': query,
                        'key': api_key,
                        'limit': 1,
                        'indent': True,
                    }
                    response_CODE = requests.get(url, params=params)
                    if response_CODE.status_code == 200:
                        data = response_CODE.json()
                        if 'itemListElement' in data and data['itemListElement']:
                            entity = data['itemListElement'][0]['result']
                            name = entity.get('name', 'No name available')
                            description = entity.get('description', 'No description available')
                            detailed_description = entity.get('detailedDescription', {}).get('articleBody', 'No detailed description available')
            return {"response":detailed_description}
        return "Sorry, I couldn't find the information."
    except:
        return {"response":"Some error occur try again after sometime"}
if __name__=="__main__":
    questions = [
         "what is black hole",
         "how developed python"
    ]

    for question in questions:
        answer = get_google_knowledge_graph(question)
        print(f"Question: {question}")
        print(f"Answer: {answer}\n")
