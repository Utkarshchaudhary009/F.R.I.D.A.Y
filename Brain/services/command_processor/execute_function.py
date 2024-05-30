from ..news import get_news
from ..weather import get_weather
from ..memory import remember, recall
from ..response import get_response
from ..remind import set_reminder_and_write_to_file
from ..bright import change_brightness
from ..volume import change_volume
from ..win import perform_window_action
from ..application import open_application
from ..web import open_website
from ..jokes import tell_joke

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
    elif function_name == "perform_window_action":
        return perform_window_action(arguments)
    elif function_name == "open_application":
        return open_application(arguments)
    elif function_name == "open_website":
        return open_website(arguments)
    elif function_name == "tell_joke":
        return tell_joke(arguments)
    else:
        return {"response": "I'm not sure how to respond to that."}
