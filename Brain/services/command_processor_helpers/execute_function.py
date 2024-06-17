from news import get_news
from weather import get_weather
from memory import remember, recall
from response import get_response
from remind import set_reminder_and_write_to_file
from bright import change_brightness
from volume import change_volume
from win import perform_window_action
from application import open_application
from website import open_website
from jokes import tell_joke
from onoff import onoff
from movieDetail import moviedetails
from spotify import get_music_details
from song import play_song
from cricket import cricket
from wiki import wiki
from wolframalpha_response import wolframalpha_response  # Ensure this import is correct and the function exists
import os
import sys
from book import book
from Brain.services.Translator import translator
from Brain.services.keyboardmagic import key
from Brain.services.search_on_web import search_web

# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

def execute_function(function_name, arguments):
    if function_name == "get_news":
        return get_news(arguments)
    elif function_name == "get_weather":
        return get_weather(arguments)
    elif function_name == "handle_memory":
        if "remember" in arguments:
            return remember(arguments)
        else:
            return recall()
    elif function_name == "get_response":
        return get_response(arguments)
    elif function_name == "set_reminder":
        return set_reminder_and_write_to_file(arguments)
    elif function_name == "change_brightness":
        return change_brightness(arguments)
    elif function_name == "change_volume":
        return change_volume(arguments)
    elif function_name == "translator":
        return translator(arguments)
    elif function_name == "search_on_web":
        return search_web(arguments)
    elif function_name == "key":
        return key(arguments)
    elif function_name == "get_cricket_updates":
        return cricket(arguments)
    elif function_name == "perform_window_action":
        return perform_window_action(arguments)
    elif function_name == "open_application":
        return open_application(arguments)
    elif function_name == "open_website":
        return open_website(arguments)
    elif function_name == "tell_joke":
        return tell_joke(arguments)
    elif function_name == "play_song":
            return play_song(arguments)
    elif function_name == "get_music_detail":
        return get_music_details(arguments)
    elif function_name == "get_movie_detail":
        return moviedetails(arguments)
    elif function_name == "toggle_on_off":
        return onoff(arguments)
    elif function_name == "book_detail":
        return book(arguments)
    elif function_name == "search_wikipedia":
        return wiki(arguments)
    elif function_name == "search_wolframalpha":
        return wolframalpha_response(arguments)
    else:
        return {"response": "I'm not sure how to execute it. Could you please try again"}