import streamlit as st
from googletrans import Translator

# Function to translate text
def translate_text(text, source_language, target_language):
    """
    Translate text from one language to another.

    Args:
    text (str): The text to be translated.
    source_language (str): The source language code.
    target_language (str): The target language code.

    Returns:
    str: Translated text.
    """
    translator = Translator()
    translated_text = translator.translate(text, src=source_language, dest=target_language)
    return translated_text.text

# Set page title and favicon
st.set_page_config(
    page_title="Text Translator",
    page_icon=":clipboard:",
    layout="wide"
)

# Custom CSS styles to mimic the provided design
st.markdown(
    """
    <style>
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }
        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: auto;
            max-width: 800px;
        }
        .translation-container {
            margin-top: 20px;
            padding: 20px;
            background-color: #FDF5E6;  /* Old Lace */
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
        }
        .translated-text-box {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            background-color: #ffffff;  /* White */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .selectbox-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .selectbox-container div {
            flex: 1;
            margin-right: 10px;
        }
        .selectbox-container div:last-child {
            margin-right: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description with colorful text
st.title("Text Translator")
st.markdown("Translate your text with ease!", unsafe_allow_html=True)

# Language selection
st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
source_language = st.selectbox("Source Language", ["English", "Spanish", "French", "Tagalog"], index=0, key="source_lang")
target_language = st.selectbox("Target Language", ["Spanish", "English", "French", "Tagalog"], index=1, key="target_lang")
st.markdown('</div>', unsafe_allow_html=True)

# Text input area
input_text = st.text_area("Enter text:", height=200)

# Translate button
if st.button("Translate", help="Click to translate"):
    if input_text:
        # Translate the text
        language_codes = {"English": "en", "Spanish": "es", "French": "fr", "Tagalog": "tl"}
        source_lang_code = language_codes[source_language]
        target_lang_code = language_codes[target_language]

        translated_text = translate_text(input_text, source_lang_code, target_lang_code)

        # Display translated text container
        st.markdown("<div class='translation-container'><h3>Translated Text:</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='translated-text-box'>{translated_text}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to translate.")
