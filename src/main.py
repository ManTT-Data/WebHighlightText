import streamlit as st
from translator_utils import translate, definition

st.set_page_config(
    page_title="Translator.AI",
    page_icon="🈶",
    layout="centered"
)

st.title("🈶 Translator App  - GPT-4")

# Chọn ngôn ngữ đầu vào và đầu ra
col1, col2 = st.columns(2)

with col1:
    input_languages_list = ["English", "Vietnamese", "German", "French"]
    input_language = st.selectbox(label="Input Language", options=input_languages_list)

with col2:
    output_languages_list = [x for x in input_languages_list if x != input_language]
    output_language = st.selectbox(label="Output Language", options=output_languages_list)

# Phần dịch văn bản
input_text = st.text_area("Type the text to be translated")

if st.button("Translate"):
    if input_text.strip():
        translated_text = translate(output_language, input_text)
        st.success(translated_text)
    else:
        st.warning("Please enter text to translate.")

# Phần tìm nghĩa từ
word = st.text_area("Meaning of: ")

if st.button("Search"):
    if word.strip():
        meaning = definition(output_language, input_text, word)
        st.success(meaning)
    else:
        st.warning("Please enter a word to search.")
