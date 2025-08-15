import streamlit as st
from auto_chatgpt import run_auto_chatgpt_app
from scraper import main_content_scraper

st.set_page_config(page_title="🧠 Multi-Tool Dashboard", layout="wide")
st.sidebar.title("Select Model")

page = st.sidebar.radio("Choose a page:", ["Content Scraper", "ChatGPT Auto Sender"])

if page == "Content Scraper":
    main_content_scraper()
    
    
elif page == "ChatGPT Auto Sender":
    run_auto_chatgpt_app()
