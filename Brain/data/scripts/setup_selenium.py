import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_selenium():
    selenium_folder = os.path.join("f:\\Friday\\Brain", 'data', 'selenium')
    if not os.path.exists(selenium_folder):
        os.makedirs(selenium_folder)

    # Check if ChromeDriver is already present
    driver_path = os.path.join(selenium_folder, 'chromedriver.exe')
    if not os.path.exists(driver_path):
        # Install ChromeDriver if not present
        print("Installing chromedriver...")
        source_path = ChromeDriverManager().install()
        shutil.copy(source_path, driver_path)
        
    # Use existing ChromeDriver
    download_folder = "F:\\Friday\\Downloads"
    os.makedirs(download_folder, exist_ok=True)
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(download_folder),
        "download.prompt_for_download": False,
    })
    
    # Path to your packed Chrome extension (.crx file)
    # extension_path = "f:/Friday/Brain/data/selenium/app.crx"

    # # Ensure the extension path is valid
    # if not os.path.exists(extension_path):
    #     raise FileNotFoundError(f"Extension file not found: {extension_path}")

    # # Add the extension
    # options.add_extension(extension_path)
    
    options.add_argument('--profile-directory=Default')
    options.add_argument(f'user-data-dir={selenium_folder}\\chromedata')

    # Desktop user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')

    # Set headless mode if needed
    options.add_argument('--headless')

    # Disable automation detection
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # Disable various Chrome security features to prevent detection
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    return driver

if __name__ == "__main__":
    driver = setup_selenium()
    
    # Wait for the extension to load
    time.sleep(5)
    driver.get("chrome-extension://hajphibbdloomfdkeoejchiikjggnaif/tabs/fullChat.html?questionAiDate=1718344392556")
    # Switch to the extension's tab (assuming it's the only open tab after loading)
    driver.switch_to.window(driver.window_handles[0])
    
    # Interact with the extension's page
    try:
        # Enter a question into the input field and submit

        # Adjust the timeout value as needed
    # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter your homework question here"]')))
    
        # Interact with the element
        input_element.send_keys('Your homework question')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print(driver.page_source)
        driver.save_screenshot('screenshot.png')  # Save a screenshot for debugging

        
    #     # Wait for the response (adjust the time as needed)
    #     time.sleep(5)
        
    #     # Get the response text (adjust the selector as needed)
    #     responses = driver.find_elements(By.CSS_SELECTOR, 'div.chat-answer .ocrtext-body #setText > div')
    #     for response in responses:
    #         print(f"AI Response: {response.text}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    time.sleep(1)
    driver.quit()
