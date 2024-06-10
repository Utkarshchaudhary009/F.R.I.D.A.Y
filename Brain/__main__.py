# File: Brain/__main__.py

from services.news import get_news

if __name__ == "__main__":
    print(get_news(time='2023-06-01', category='technology'))
