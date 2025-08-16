from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import streamlit as st


def extract_main_content(soup):
    content = {}

    # Title
    page_title = soup.title.string if soup.title else "No title"
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]

    # Paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

    # Spans
    spans = [span.get_text(strip=True) for span in soup.find_all('span')]

    # Bold text
    bolds = [b.get_text(strip=True) for b in soup.find_all(['b', 'strong'])]

    content['title'] = page_title
    content['headings'] = headings
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


# Streamlit App
def main_content_scraper():
    st.title("🔍 Web Content Extractor")

    url = st.text_input("Enter URL to scrape:")
    method = st.radio("Choose scraping method:", ["BeautifulSoup", "Selenium"])

    if st.button("Scrape Now"):
        if url:
            if method == "BeautifulSoup":
                result = scrape_with_bs4(url)
            else:
                result = scrape_with_selenium(url)

            if "error" in result:
                st.error(result["error"])
            else:
                # Convert dict to formatted text
                quer = f"Title: {result['title']}\n\n"
                quer += f"Headings: {result['headings']}\n\n"
                quer += f"Paragraphs: {result['paragraphs']}\n\n"
                quer += f"Spans: {result['spans']}\n\n"
                quer += f"Bold Text: {result['bolds']}\n\n"

                st.subheader("✅ Extracted Content")
                st.text_area("Result", quer, height=300)

                # Download button
                st.download_button("⬇️ Download Result", quer, file_name="scraped_content.txt")
        else:
            st.warning("Please enter a URL.")


if __name__ == "__main__":
    main_content_scraper()
