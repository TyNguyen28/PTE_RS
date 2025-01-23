import streamlit as st
from gtts import gTTS
import os
import string
import difflib
import numpy as np
import pandas as pd
from scipy.io import wavfile

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

# Function to process the uploaded audio file
def process_uploaded_audio(file):
    try:
        fs, data = wavfile.read(file)
        return data, fs
    except Exception as e:
        st.error(f"An error occurred while processing the audio: {e}")
        return None, None

# Main application
def main():
    st.title("🎙️ Speech Grader App with Question Bank")
    st.markdown("Evaluate your speaking fluency, pronunciation, and content match!")

    # Load default question bank
    question_bank_path = 'RS/QB.csv'
    sentences = []
    if os.path.exists(question_bank_path):
        try:
            sentences = pd.read_csv(question_bank_path, encoding='ISO-8859-1')['Sentence'].tolist()
            st.success(f"Loaded default question bank with {len(sentences)} sentences.")
        except Exception as e:
            st.error(f"An error occurred while loading the question bank: {e}")
    else:
        st.error(f"Default question bank not found at {question_bank_path}. Please ensure it is in the app directory.")

    # Step 1: Input sentence
    st.subheader("Step 1: Select or Input a Sentence")
    if sentences:
        selected_sentence = st.selectbox("Choose a sentence to practice:", sentences)
    else:
        selected_sentence = st.text_input("Or enter a sentence manually:")

    if selected_sentence:
        st.success("Sentence selected!")

        # Step 2: Convert text to speech
        st.subheader("Step 2: Listen to the Sentence")
        tts = gTTS(text=selected_sentence, lang='en')
        tts.save("output.mp3")
        play_audio("output.mp3")

        st.info("Click play to listen to the sentence and then repeat it.")

        # Step 3: Upload and Process Speech
        st.subheader("Step 3: Upload Your Speech Recording")
        st.warning("Ensure your audio is in WAV format.")

        uploaded_file = st.file_uploader("Upload your recorded audio file", type=['wav'])
        if uploaded_file is not None:
            _, fs = process_uploaded_audio(uploaded_file)
            if fs:
                st.success("Audio uploaded and processed successfully!")

                # Step 4: Placeholder for Speech Recognition and Scoring
                st.subheader("Grading Results")
                st.warning("Speech recognition and scoring will be added here in future updates.")
            else:
                st.error("Failed to process the uploaded audio.")

# Run the application
if __name__ == "__main__":
    main()
