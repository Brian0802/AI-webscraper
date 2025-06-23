import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def scrape_site(website: str):
    # may use service from bright data to bypass human test
    print("Log: lauching chrome browser")
    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Log: page load Successfully")
        html = driver.page_source
        time.sleep(10)
        return html
    except Exception as e:
        print(e)
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

# Isolate readable text
def clean_body_content(body_content):
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
    url_for_testing = "https://translate.google.com.tw/?hl=zh-TW&sl=en&tl=zh-TW&op=translate"
    html = scrape_site(url_for_testing)
    body_content = extract_body_content(html)
    cleaned_content = clean_body_content(body_content)
    if cleaned_content:
        print("Refined text result")
        print(cleaned_content)
    
    