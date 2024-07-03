import requests
import random
from datetime import datetime, timedelta
import sys
import os
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Brain.utilities.readEnv import readEnv  # Absolute import
from BOS.speak import speak

def get_news(time=None, category=None):
    base_url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': readEnv("NEWS"),  # Replace 'YOUR_API_KEY' with your actual News API key,
        'country': 'us'  # You can change this to the desired country
    }
    
    # Set default category if none is provided
    if not category:
        category = 'general'
    params['category'] = category.lower()
    
    # Handle 'today', 'yesterday', and 'tomorrow'
    today = datetime.today().date()
    if not time:
        time = 'today'
    
    if time.lower() == 'today':
        news_date = today
    elif time.lower() == 'yesterday':
        news_date = today - timedelta(days=1)
    elif time.lower() == 'tomorrow':
        future_responses = [
            "I'm not a fortune teller, but I see good things in your future!",
            "Why look at tomorrow's news when today is already exciting?",
            "Tomorrow never comes, they say. Let's focus on today!",
            "Predictions for tomorrow? How about some lottery numbers?",
            "The future is a mystery, enjoy the present!",
            "Indian astrologers are better at future predictions!",
            "Tomorrow's news? You'll just have to wait and see!",
            "No spoilers for tomorrow's headlines!",
            "Stay tuned, tomorrow is going to be legendary!",
            "Predicting the future? That’s above my pay grade!",
            "How about we just enjoy the present moment?",
            "Tomorrow’s news is like a Bollywood movie—full of surprises!",
            "You want tomorrow's news? Let me call my astrologer!",
            "Can I interest you in today's news instead?",
            "The crystal ball is a bit hazy, check back tomorrow!",
            "The stars say tomorrow will be amazing!",
            "I can tell you today's news; tomorrow is still a mystery!",
            "Let’s just say, tomorrow will be full of surprises!",
            "Trust me, tomorrow will be a great day!",
            "Why worry about tomorrow when today is already so interesting?"
        ]
        return {'response': random.choice(future_responses)}
    else:
        try:
            news_date = datetime.strptime(time, '%Y-%m-%d').date()
        except ValueError:
            return {'response': "Error: Invalid date format. Please use 'YYYY-MM-DD'."}
    
    params['from'] = news_date.isoformat()
    params['to'] = news_date.isoformat()
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        if articles:
            random_article = random.choice(articles)
            title=random_article.get('title') 
            desc=random_article.get('description')
            news = f"{title} , Now news in detail {desc}"
            return {'response': news}
        else:
            return {'response': 'No news articles found'}
    else:
        return {'response': f"Error: Unable to fetch news (Status code: {response.status_code})"}

# Example usage
if __name__ == "__main__":
    # speak("Why worry about tomorrow when today is already so interesting?")
    speak(get_news().get("response"))
