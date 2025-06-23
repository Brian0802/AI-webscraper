# Tutorial Link: https://youtu.be/Oo8-nEuDBkk?list=PLD47eF0PZsocRPQdd4HCVvBLCxHgJHKqd
# run streamlit app: streamlit run main.py
import streamlit as st
from parse import parse_with_gpt
from scrape import (
    scrape_site,
    extract_body_content,
    clean_body_content,
    split_dom_content
)

st.title("AI Web Scraper")
url = st.text_input("Enter the URL to scrape:")
# url for testing: https://translate.google.com.tw/?hl=zh-TW&sl=en&tl=zh-TW&op=translate

if st.button("Start scraping"):
    result = scrape_site(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM content"):
        st.text_area("DOM content", cleaned_content, height=300)
    
if "dom_content" in st.session_state:
    user_prompt = st.text_area("Describe what you want to parse:")
    print(user_prompt)

    if st.button("Parse Content"):
        if user_prompt:
            st.write("Parsing...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_gpt(dom_chunks, user_prompt)
            st.write(result)

