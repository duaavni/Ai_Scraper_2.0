import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("🕸️ AI Web Scraper using Ollama")

url = st.text_input("Enter a website URL to scrape", placeholder="https://example.com")

if st.button("Scrape Website"):
    if url:
        st.info("Scraping the website...")

        try:
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content

            st.success("Scraping complete!")
            with st.expander("🔍 View Scraped DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"Error scraping the site: {e}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what to extract from the content", placeholder="e.g. Extract all book titles and prices...")

    if st.button("Parse Content"):
        if parse_description.strip():
            st.info("Parsing with Ollama...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.success("Parsing done!")

            st.subheader("📄 Parsed Result")
            st.text_area("Result", parsed_result, height=300)
        else:
            st.warning("Please describe what you want to extract.")
