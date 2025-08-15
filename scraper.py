import streamlit as st
from scraperr import scrape_with_bs4, scrape_with_selenium

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
            st.warning("Please enter a valid URL.")

# Run the function
if __name__ == "__main__":
    main_content_scraper()
