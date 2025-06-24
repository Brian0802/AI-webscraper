import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_site(website: str) -> str:
    # may use service from bright data to bypass human test
    print("Log: lauching chrome browser")
    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0")

    try:
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.get(website)
        logger.info("Page load initiated")
        html = driver.page_source
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        if html:
            logger.info("Page loaded successfully")
            return html  
              
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    finally:
        driver.quit()

def extract_body_content(html_content: str) -> str:
    try: 
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return ""

# Isolate readable text
def clean_body_content(body_content: str) -> str:
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

# This function is needed due to limit batch size for LLMs
def split_dom_content(dom_content, max_length = 6000):
    return [dom_content[i : i+max_length] for i in range(0, len(dom_content), max_length)]

if __name__ == "__main__":
    url_for_testing = "https://translate.google.com/?sl=en&tl=zh-TW&op=translate"
    html = scrape_site(url_for_testing)
    body_content = extract_body_content(html)
    cleaned_content = clean_body_content(body_content)
    if cleaned_content:
        print("Refined text result:")
        print(cleaned_content)
    
    