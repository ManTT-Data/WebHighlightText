import streamlit as st
from translator_utils import translate, definition

# Set page config first
st.set_page_config(
    page_title="Translator.AI",
    page_icon="🈶",
    layout="centered"
)

# Custom CSS to improve the appearance
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stSelectbox>div>div>div {
        background-color: #f0f2f6;
    }
    h1, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🈶 Translator.AI")
st.markdown("##### Powered by GPT-4")

# Language selection
st.markdown("### Select Languages")
col1, col2 = st.columns(2)

with col1:
    input_languages_list = ["English", "Vietnamese", "German", "French"]
    input_language = st.selectbox(label="Input Language", options=input_languages_list)

with col2:
    output_languages_list = [x for x in input_languages_list if x != input_language]
    output_language = st.selectbox(label="Output Language", options=output_languages_list)

# Translation section
st.markdown("### Translation")
input_text = st.text_area("Enter text to translate", height=150)

if st.button("Translate"):
    if input_text.strip():
        with st.spinner("Translating..."):
            translated_text = translate(output_language, input_text)
        st.success(translated_text)
    else:
        st.warning("Please enter text to translate.")

# Word definition section
st.markdown("### Word Definition")
word = st.text_input("Enter a word to find its meaning")

if st.button("Search Definition"):
    if word.strip():
        with st.spinner("Searching..."):
            meaning = definition(output_language, input_text, word)
        st.info(meaning)
    else:
        st.warning("Please enter a word to search.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Your Name")