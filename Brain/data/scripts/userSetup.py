import os
import sys

# Ensure the current script's parent directory is in sys.path for imports
scripts_dir = os.path.abspath(os.path.dirname(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)
    
import json
from save_user_data import save_user_data
from save_credentials import save_credentials
from setup_selenium import setup_selenium
from login import login_to_google
from login import login_to_gemini
from login import login_to_openai_chatgpt

def user_setup():
    save_user_data()
    save_credentials()
    driver = setup_selenium()
    login_to_google(driver)
    login_to_gemini(driver)
    login_to_openai_chatgpt(driver)
    
    # Add additional logic for Gemini and ChatGPT as needed.
    # For example, you can add similar functions to login to these services.
    
    driver.quit()
    print("Setup complete.")

if __name__ == "__main__":
    user_setup()
