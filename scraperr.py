from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests, time

def extract_main_content(soup):
    parts = []

    if soup.title:
        parts.append(f"TITLE: {soup.title.string.strip()}")

    headings = [h.get_text(strip=True) for h in soup.find_all(['h1','h2'])]
    if headings:
        parts.append("HEADINGS:\n" + "\n".join(headings))

    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    if paragraphs:
        parts.append("PARAGRAPHS:\n" + "\n".join(paragraphs))

    spans = [span.get_text(strip=True) for span in soup.find_all('span')]
    if spans:
        parts.append("SPANS:\n" + "\n".join(spans))

    bolds = [b.get_text(strip=True) for b in soup.find_all(['b','strong'])]
    if bolds:
        parts.append("BOLDS:\n" + "\n".join(bolds))

    return "\n\n".join(parts)


def scrape_with_bs4(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return extract_main_content(soup)
    except Exception as e:
        return f"❌ Error: {e}"


def scrape_with_selenium(url):
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        return extract_main_content(soup)
    except Exception as e:
        return f"❌ Error: {e}"
