import time
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
except ImportError as e:
    print("Failed to import setup_selenium. Ensure the path is correct and the module exists.")
    raise e


def detect_language(text):
    tried = 0
    max_retries = 5

    while tried < max_retries:
        driver = setup_selenium()
        try:
            # Open Google Translate
            driver.get("https://translate.google.com/")
            print("Attempt:", tried + 1)

            # Locate the text input area and enter the text
            input_area = driver.find_element(By.XPATH, "//textarea[@aria-label='Source text']")
            input_area.send_keys(text)
            print("Text input completed")

            # Wait for the translation to complete and the language to be detected
            time.sleep(5 * (tried + 1))

            # Locate the detected language element
            detected_language = driver.find_element(By.XPATH, "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[1]")#c286 > span.VfPpkd-YVzG2b
            detected_language_text = detected_language.get_attribute('innerText').replace(" - Detected", "")
            
            if detected_language_text == "Detect language":
                raise ValueError("Language detection failed")

            print("Detected language:", detected_language_text)
            return LANGCODE.get(detected_language_text, None)
        except Exception as e:
            print(f"An error occurred: {e}")
            tried += 1
        finally:
            driver.quit()
    
    print("Failed to detect language after multiple attempts")
    return None


# LANGCODE={
#     "Afrikaans": "af",
#     "Albanian": "sq",
#     "Amharic": "am",
#     "Arabic": "ar",
#     "Armenian": "hy",
#     "Azerbaijani": "az",
#     "Basque": "eu",
#     "Belarusian": "be",
#     "Bengali": "bn",
#     "Bosnian": "bs",
#     "Bulgarian": "bg",
#     "Catalan": "ca",
#     "Cebuano": "ceb",
#     "Chichewa": "ny",
#     "Chinese Simplified": "zh-CN",
#     "Chinese Traditional": "zh-TW",
#     "Corsican": "co",
#     "Croatian": "hr",
#     "Czech": "cs",
#     "Danish": "da",
#     "Dutch": "nl",
#     "English": "en",
#     "Esperanto": "eo",
#     "Estonian": "et",
#     "Filipino": "tl",
#     "Finnish": "fi",
#     "French": "fr",
#     "Frisian": "fy",
#     "Galician": "gl",
#     "Georgian": "ka",
#     "German": "de",
#     "Greek": "el",
#     "Gujarati": "gu",
#     "Haitian Creole": "ht",
#     "Hausa": "ha",
#     "Hawaiian": "haw",
#     "Hebrew": "he",
#     "Hindi": "hi",
#     "Hmong": "hmn",
#     "Hungarian": "hu",
#     "Icelandic": "is",
#     "Igbo": "ig",
#     "Indonesian": "id",
#     "Irish": "ga",
#     "Italian": "it",
#     "Japanese": "ja",
#     "Javanese": "jw",
#     "Kannada": "kn",
#     "Kazakh": "kk",
#     "Khmer": "km",
#     "Kinyarwanda": "rw",
#     "Korean": "ko",
#     "Kurdish (Kurmanji)": "ku",
#     "Kyrgyz": "ky",
#     "Lao": "lo",
#     "Latin": "la",
#     "Latvian": "lv",
#     "Lithuanian": "lt",
#     "Luxembourgish": "lb",
#     "Macedonian": "mk",
#     "Malagasy": "mg",
#     "Malay": "ms",
#     "Malayalam": "ml",
#     "Maltese": "mt",
#     "Maori": "mi",
#     "Marathi": "mr",
#     "Mongolian": "mn",
#     "Myanmar (Burmese)": "my",
#     "Nepali": "ne",
#     "Norwegian": "no",
#     "Odia (Oriya)": "or",
#     "Pashto": "ps",
#     "Persian": "fa",
#     "Polish": "pl",
#     "Portuguese": "pt",
#     "Punjabi": "pa",
#     "Romanian": "ro",
#     "Russian": "ru",
#     "Samoan": "sm",
#     "Scots Gaelic": "gd",
#     "Serbian": "sr",
#     "Sesotho": "st",
#     "Shona": "sn",
#     "Sindhi": "sd",
#     "Sinhala": "si",
#     "Slovak": "sk",
#     "Slovenian": "sl",
#     "Somali": "so",
#     "Spanish": "es",
#     "Sundanese": "su",
#     "Swahili": "sw",
#     "Swedish": "sv",
#     "Tajik": "tg",
#     "Tamil": "ta",
#     "Tatar": "tt",
#     "Telugu": "te",
#     "Thai": "th",
#     "Turkish": "tr",
#     "Turkmen": "tk"
#     }

LANGCODE = {
    "Hindi": "hi",
    "English": "en",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Kannada": "kn",
    "Malayalam": "ml"
}

# Example usage
if __name__ == "__main__":
    text = "tum kaisa ho"
    language = detect_language(text)
    print(f"Detected language: {language}")
