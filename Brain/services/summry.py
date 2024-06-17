from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Get the grandparent directory
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

def summarize_text(text, sentence_count=2):
    try:
        driver = setup_selenium()
        # Open QuillBot Summarizer
        driver.get("https://quillbot.com/summarize")

        # Wait until the text area is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='inputBoxSummarizer']"))
        )

        # Find the text area and enter the text to be summarized
        text_area = driver.find_element(By.XPATH, "//*[@id='inputBoxSummarizer']")
        text_area.clear()
        text_area.send_keys(text)

        short=driver.find_element(By.XPATH, "//*[@id='root-client']/div/div[3]/section[1]/div/div/div/section/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/span/span[3]")
        short.click()
        print("qwerty: ", short.text)

        # Wait until the Summarize button is clickable and click it
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='root-client']/div/div[3]/section[1]/div/div/div/section/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/span/div/button/span[1]"))
        ).click()

        # Wait for the summarized text to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='outputBoxSummarizer']"))
        )

        # for i in range(1,5):
        while True:
            try:
                time.sleep(3)
                text = driver.find_element(By.XPATH, "//*[@id='outputBoxSummarizer']").text
                if text != "":
                    break
            except:
                pass
        
        # Extract and return the summarized text
        summarized_text = driver.find_element(By.XPATH, "//*[@id='outputBoxSummarizer']").text
        return summarized_text

    except Exception as e:
        print(f"An error occurred with Selenium: {e}")
        # Fallback to using sumy for summarization
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join([str(sentence) for sentence in summary])
    finally:
        driver.quit()
# Example usage
if __name__ == "__main__":
    text = "Anthony Edward 'Tony' Stark[10] was a billionaire industrialist, a founding member of the Avengers, and the former CEO of Stark Industries. A brash but brilliant inventor, Stark was self-described as a genius, billionaire, playboy, and philanthropist. With his great wealth and exceptional technical knowledge, Stark was one of the world's most powerful men following the deaths of his parents and enjoyed the playboy lifestyle for many years until he was kidnapped by the Ten Rings in Afghanistan, while demonstrating a fleet of Jericho missiles. With his life on the line, Stark created an armored suit which he used to escape his captors. Upon returning home, he utilized several more armors to use against terrorists, as well as Obadiah Stane who turned against Stark. Following his fight against Stane, Stark publicly revealed himself as Iron Man.Fresh off from defeating enemies all over the world, Stark found himself dying due to his own Arc Reactor poisoning his body, all while he was challenged by Ivan Vanko who attempted to destroy his legacy. After the Stark Expo incident, Stark reluctantly agreed to serve as a consultant for S.H.I.E.L.D. where he used his position to upgrade their technology while he began a relationship with Pepper Potts. With the world yet again being threatened, Stark joined the Avengers and helped defeat the Chitauri and Loki. Due to the battle, he suffered from post-traumatic stress disorder, leading him to create the Iron Legion to safeguard the world and help him retire.The 2013 'Mandarin' terrorist attacks forced Stark to come out of retirement to protect his country, inadvertently putting his loved ones at risk and leaving him defenseless when his home was destroyed. Stark continued his mission, finding Aldrich Killian as the mastermind of the attacks. Eventually, Stark defeated Killian, and was prompted to destroy all of his armors with the Clean Slate Protocol after almost losing Potts. However, when the Avengers were officially demobilized due to the War on HYDRA, Stark built more armors and resumed his role as Iron Man, aiding them in the capture of Baron Strucker and acquiring Loki's Scepter.Once the threat of HYDRA had been ended, at last, Stark, influenced by Scarlet Witch's visions, built Ultron with the help of Bruce Banner as a new peacekeeping A.I. to protect the world and allow the Avengers to retire. However, Ultron believed that humanity threatened the world and thus, according to his program, decided to extinguish humanity. Through the work of the Avengers, Ultron was defeated, however, not without massive civilian cost and many lives being lost during which Sokovia was elevated into the sky.After the Ultron Offensive, Stark retired from active duty, still haunted by his role in the chaos the A.I. created. The guilt of creating Ultron and causing so much destruction and loss of life eventually convinced Stark to support the Sokovia Accords. Stark was forced to lead a manhunt for his ally Captain America when the latter began protecting the fugitive Winter Soldier, igniting the Avengers Civil War. The result left the Avengers in complete disarray, especially after Stark learned of the Winter Soldier's role in his parents' deaths. Afterwards, Stark returned to New York to mentor and guide Spider-Man into becoming a better hero than he ever was, also becoming engaged with Potts in the process."
    summary = summarize_text(text)
    print("Summary:", summary)

