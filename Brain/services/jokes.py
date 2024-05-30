import requests
import pyjokes

def fetch_joke_from_api(type="general"):
    try:
        url = "https://official-joke-api.appspot.com/jokes/random"
        if type == "romantic":
            url = "https://official-joke-api.appspot.com/jokes/romantic/random"
        response = requests.get(url)
        joke = response.json()
        if isinstance(joke, list):
            joke = joke[0]
        return f"{joke['setup']} {joke['punchline']}"
    except Exception as e:
        return None

def tell_joke(arguments):
    joke_type = arguments.get("type", "general")
    joke = fetch_joke_from_api(joke_type)
    
    if not joke:
        if joke_type == "romantic":
            joke = "I asked my wife if I was the only one she had been with. She said yes, all the others were nines and tens!"
        else:
            joke = pyjokes.get_joke()

    return {"response": joke}
