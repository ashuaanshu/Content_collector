from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time


def extract_main_content(soup):
    content = {}

    # Title
    page_title = soup.title.string if soup.title else "No title"
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]

    # Images
    images = [img['src'] for img in soup.find_all('img') if img.get('src')]

    # Paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

    # Spans
    spans = [span.get_text(strip=True) for span in soup.find_all('span')]

    # Bold text
    bolds = [b.get_text(strip=True) for b in soup.find_all(['b', 'strong'])]

    content['title'] = page_title
    content['headings'] = headings
    content['images'] = images
    content['paragraphs'] = paragraphs
    content['spans'] = spans
    content['bolds'] = bolds

    return content


def scrape_with_bs4(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return extract_main_content(soup)
    except Exception as e:
        return {"error": f"❌ Error: {e}"}


def scrape_with_selenium(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        return extract_main_content(soup)
    except Exception as e:
        return {"error": f"❌ Error: {e}"}
