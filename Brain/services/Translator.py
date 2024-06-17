from googletrans import Translator
import re
import json
import os
import sys
# Get the parent directory of the current file (Moniter_System.py)
import sys
sys.path.append(r'F:\Friday')  # Replace 'F:\Friday' with the actual path to the parent directory

from BOS.speak import googlespeak

CACHE_FILE = 'F:\Friday/brain/data/cache/translation_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

import pickle

# Load the saved model and label encoder

with open('F:\Friday/brain/models/lang/language_code_model.pkl', 'rb') as f:
    model, label_encoder = pickle.load(f)

# Predict language code
def get_language_code(language_name):
    prediction = model.predict([language_name])
    lang_code = label_encoder.inverse_transform(prediction)[0]
    print(lang_code)
    return lang_code

def translate_text(text, target_code='en', cache=None):
    cache_key = f"{text.lower()}:{target_code}"
    
    if cache is None:
        cache = load_cache()
    
    if cache_key in cache:
        return {"response":"009","data":{"text":cache[cache_key],"code":target_code}}
    
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_code)
        translated_text = translation.text
        cache[cache_key] = translated_text
        save_cache(cache)
        return {"response":"009","data":{"text":cache[cache_key],"code":target_code}}
    
    except Exception as e:
        print("Error during translation:", e)
        return {"response":"some error occur. try to transkate after sometime","data":None}

def extract_translation_input(user_input, cache):
    pattern = r'^translate\s+(.+?)\s+(?:into|to)\s+(.+)$'
    match = re.match(pattern, user_input, re.IGNORECASE)
    if match:
        text_to_translate, target_language = match.groups()
        target_code = get_language_code(target_language)
        if target_code:
            data= translate_text(text_to_translate, target_code, cache)
            googlespeak(data["data"]["text"],data["data"]["code"])
            return {"response":None}
        else:
            print(f"Unsupported language: {target_language}")
    else:
        print("Invalid input format. Please enter text to translate followed by 'into' or 'to' and the target language.")
    return None

def translator(user_input):
    cache = load_cache()
    return extract_translation_input(user_input, cache)

if __name__ == "__main__":
    while True:
        user_input = input("Enter text to translate : ")
        processed=f"translate {user_input} to korean"
        print(processed)
        translator(processed)
