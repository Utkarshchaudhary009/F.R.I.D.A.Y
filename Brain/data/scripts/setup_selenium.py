import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.chrome.options import Options

def setup_selenium():
    selenium_folder = os.path.join("f:\\Friday\\Brain", 'data', 'selenium')
    if not os.path.exists(selenium_folder):
        os.makedirs(selenium_folder)

    # Check if ChromeDriver is already present
    driver_path = os.path.join(selenium_folder, 'chromedriver.exe')
    if not os.path.exists(driver_path):
        # Install ChromeDriver if not present
        print("installing chromedriver...")
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
    options.add_argument('--profile-directory=Default')
    options.add_argument(f'user-data-dir={selenium_folder}\\chromedata')
    # Desktop user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    ]

    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')

    # Set headless mode
    # options.add_argument('--headless')

    # Disable automation detection
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # Disable various Chrome security features to prevent detection
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    return driver
