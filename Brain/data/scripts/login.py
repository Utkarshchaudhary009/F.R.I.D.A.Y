import time
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import random
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
    from setup_selenium import setup_selenium
except ImportError as e:
    print("Failed to import setup_selenium. Ensure the path is correct and the module exists.")
    raise e

def get_credentials():
    credentials_path = os.path.join("f:\\Friday\\Brain\\", 'data', 'credentials.crc')
    credentials = {}
    with open(credentials_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            credentials[key] = value
    return credentials

def login_to_google():
    driver = setup_selenium()

    # Replace with your actual credentials retrieval method
    credentials = credentials = get_credentials()

    try:

        # Open Google login page
        driver.get("https://accounts.google.com/signin")

        # Enter the email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys("utkarshchaudhary@gmail.com")
        email_input.send_keys(Keys.ENTER)

        # Wait for the password field to appear and enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("your-password")
        password_input.send_keys(Keys.ENTER)

        # Wait for the login to complete by checking for an element only present after login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://myaccount.google.com')]"))
        )

        print("Logged in successfully!")

        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

def login_to_gemini(driver):
    driver.get("https://www.gemini.com/")

    continue_with_google_button = driver.find_element(By.XPATH, "//span[text()='Continue with Google']")
    continue_with_google_button.click()
    time.sleep(2)

    print("Logged in to Gemini successfully.")

def login_to_openai_chatgpt(driver):
    driver.get("https://platform.openai.com/")

    continue_with_google_button = driver.find_element(By.XPATH, "//span[text()='Continue with Google']")
    continue_with_google_button.click()
    time.sleep(2)

    print("Logged in to OpenAI ChatGPT successfully.")

login_to_google()