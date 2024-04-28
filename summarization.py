# -*- coding: utf-8 -*-
"""summarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XxiIq-xJVtPnXEQlJbkRPi79wq8kyB3I
"""



import streamlit as st
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize the text into words and remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words]

    return sentences, words

def calculate_word_freq(words):
    # Calculate word frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    return word_freq

def calculate_sentence_scores(sentences, word_freq, num_sentences):
    # Calculate the sentence scores based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]

    # Get the top N sentences with the highest scores
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    return summary_sentences

def generate_summary(file_path, num_sentences):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract the text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Preprocess the text
        sentences, words = preprocess_text(text)

        # Calculate word frequency
        word_freq = calculate_word_freq(words)

        # Calculate the sentence scores and get the summary sentences
        summary_sentences = calculate_sentence_scores(sentences, word_freq, num_sentences)

        # Join the summary sentences into a single string
        summary = ' '.join(summary_sentences)

        return summary

def main():
    st.title("PDF Summarizer")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Number of sentences slider
    num_sentences = st.slider("Number of sentences in the summary", min_value=1, max_value=10, value=5)

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())

        # Generate summary
        summary = generate_summary("temp.pdf", num_sentences)

        # Display the summary
        st.subheader("Summary")
        st.write(summary)

if __name__ == '__main__':
    main()
