import streamlit as st
import nltk
import re
from rake_nltk import Rake
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer
import time

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')


# Function to preprocess text
def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters except periods
    text = re.sub(r'[^a-zA-Z0-9.\s]', '', text)
    return text


# Function to summarize text
def summarize_text(input_text):
    # Preprocess input text
    input_text = preprocess_text(input_text)

    # Extract keywords using RAKE
    r = Rake()
    r.extract_keywords_from_text(input_text)
    extracted_keywords = r.get_ranked_phrases_with_scores()[:5]  # Get top 5 ranked phrases

    # Parse the input text
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))

    # Create an LSA summarizer
    stemmer = Stemmer("english")
    summarizer = LsaSummarizer(stemmer)

    # Generate the summary
    summary = summarizer(parser.document, sentences_count=2)  # Always summarize into 2 sentences

    return summary, extracted_keywords


# Set page title and favicon
st.set_page_config(
    page_title="Text Summarizer",
    page_icon=":clipboard:",
    layout="wide"
)

# Custom CSS styles with colorful background and text colors
st.markdown(
    """
    <style>
        body {
            background-color: #F2F4F6;  /* Light Gray */
            font-family: Arial, sans-serif;
        }
        .st-eb {
            background-color: #FFFFFF;  /* White */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .st-el {
            border-radius: 10px;
        }
        .st-at {
            font-size: 18px;
            font-weight: bold;
            color: #2F4F4F;  /* Dark Slate Gray */
        }
        .summary-container {
            margin-top: 20px;
            padding: 20px;
            background-color: #FDF5E6;  /* Old Lace */
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .keywords-container {
            margin-top: 20px;
            padding: 20px;
            background-color: #FFF8DC;  /* Cornsilk */
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description with colorful text
st.title("Text Summarizer")
st.markdown("Summarize your text with ease!", unsafe_allow_html=True)

# Text input area
input_text = st.text_area("Enter your text here:", height=200)

# Summarize button with Dodger Blue color
if st.button("Summarize", help="Click to summarize"):
    if input_text:
        # Display loading message and progress bar
        progress_bar = st.progress(0)
        status_text = st.text("Summarizing...")

        # Call the summarize_text function
        summary, extracted_keywords = summarize_text(input_text)

        # Simulate progress with time.sleep() and update progress bar
        for percent_complete in range(1, 101):
            time.sleep(0.01)
            progress_bar.progress(percent_complete)

        # Display summary container
        status_text.text("Done")
        st.markdown("<div class='summary-container'><h3>Summary:</h3>", unsafe_allow_html=True)
        for sentence in summary:
            st.write(sentence)
        st.markdown("</div>", unsafe_allow_html=True)

        # Display keywords container
        st.markdown("<div class='keywords-container'><h3>Extracted Keywords:</h3>", unsafe_allow_html=True)
        keywords_table = "<table><tr><th>Keyword</th><th>Score</th></tr>"
        for score, phrase in extracted_keywords:
            keywords_table += f"<tr><td>{phrase}</td><td>{score}</td></tr>"
        keywords_table += "</table>"
        st.markdown(keywords_table, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Remove loading message and progress bar
        status_text.empty()
        progress_bar.empty()
    else:
        st.warning("Please enter some text to summarize.")
