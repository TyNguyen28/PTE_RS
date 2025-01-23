import streamlit as st
from gtts import gTTS
import os
import string
import difflib
import numpy as np
import pandas as pd

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

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

        # Step 3: Placeholder for recording and recognition
        st.subheader("Step 3: Record Your Speech")
        st.warning("Recording and live speech recognition is currently unavailable in this environment.")
        st.text("You can update this app to accept uploaded audio for offline processing.")

# Run the application
if __name__ == "__main__":
    main()
