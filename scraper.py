import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time


# ------------------- Scraper Utils -------------------
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


# ------------------- Streamlit UI -------------------
def main_content_scraper():
    st.set_page_config(page_title="🧠 Main Content Scraper", layout="wide")
    st.title("📄 Main Content Scraper")

    url = st.text_input("🔗 Enter Website URL:")
    use_selenium = st.toggle("Use Selenium (for dynamic sites)")

    if st.button("Scrape Content"):
        if url:
            with st.spinner("🔍 Scraping... Please wait..."):
                result = scrape_with_selenium(url) if use_selenium else scrape_with_bs4(url)

            if "error" in result:
                st.error(result["error"])
            else:
                with st.container():
                    all_text = ""

                    # Title
                    st.subheader("📝 Title")
                    st.write(result["title"])
                    all_text += f"Title: {result['title']}\n\n"

                    # Headings
                    st.subheader("🔠 Headings")
                    for h in result["headings"]:
                        st.markdown(f"- {h}")
                        all_text += f"Heading: {h}\n"

                    # Paragraphs
                    st.subheader("📄 Paragraphs")
                    for p in result["paragraphs"]:
                        st.markdown(f"> {p}")
                        all_text += f"{p}\n\n"

                    # Spans
                    st.subheader("🔤 Span Text")
                    for s in result["spans"]:
                        st.text(s)
                        all_text += f"Span: {s}\n"

                    # Bolds
                    st.subheader("🔡 Bold Text")
                    for b in result["bolds"]:
                        st.markdown(f"**{b}**")
                        all_text += f"Bold: {b}\n"

                # Copy Button Section
                st.divider()
                st.subheader("📋 Copy All Text")
                st.text_area("Click and Copy:", all_text, height=300)
        else:
            st.warning("⚠️ Please enter a valid URL.")


# ------------------- Run App -------------------
if __name__ == "__main__":
    main_content_scraper()
