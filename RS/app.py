import streamlit as st
from gtts import gTTS
import os
import string
import difflib
import numpy as np
import pandas as pd
import sounddevice as sd
from scipy.io.wavfile import write

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

# Function to record audio using sounddevice
def record_audio(duration=5, filename="output.wav", fs=44100):
    st.info(f"Recording for {duration} seconds...")
    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        write(filename, fs, audio_data)  # Save as WAV file
        st.success("Recording completed successfully!")
        return filename
    except Exception as e:
        st.error(f"An error occurred while recording: {e}")
        return None

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

        # Step 3: Record and Recognize Speech
        st.subheader("Step 3: Record Your Speech")
        st.warning("Ensure your microphone is enabled before starting!")

        record_btn = st.button("Start Recording")
        if record_btn:
            filename = record_audio()
            if filename:
                st.info(f"Audio recorded and saved as {filename}.")
                # Speech recognition could be added here if needed, using the recorded audio file

# Run the application
if __name__ == "__main__":
    main()
