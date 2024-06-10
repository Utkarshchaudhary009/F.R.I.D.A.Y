import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Add parent directory to sys.path to make relative imports work
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    print(f"{parent_dir}\scripts")
    sys.path.append(f"{parent_dir}\scripts")

def get_credentials():
    credentials_path = os.path.join("f:\\Friday\\Brain\\", 'data', 'credentials.crc')
    credentials = {}
    with open(credentials_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            credentials[key] = value
    return credentials

def login_to_google(driver):
    credentials = get_credentials()

    driver.get("https://accounts.google.com/signin")

    email_field = driver.find_element(By.ID, "identifierId")
    email_field.send_keys(credentials['Gmail'])
    email_field.send_keys(Keys.RETURN)
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(credentials['Password'])
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    print("Logged in to Google successfully.")

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