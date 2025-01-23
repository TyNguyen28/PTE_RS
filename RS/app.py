import streamlit as st
from gtts import gTTS
import os
import string
import time
import difflib
import numpy as np
import pandas as pd
import speech_recognition as sr

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

# Function to process the uploaded file
def process_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)['Sentence'].tolist()
    elif uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode('utf-8').splitlines()
    else:
        st.error("Unsupported file type. Please upload a .csv or .txt file.")
        return []

# Main application
def main():
    st.title("🎙️ Speech Grader App with Question Bank")
    st.markdown("Evaluate your speaking fluency, pronunciation, and content match!")

    # Check if RS_QBs.csv exists and load it automatically
    default_sentences = []
    if os.path.exists('RS_QBs.csv'):
        default_sentences = pd.read_csv('RS_QBs.csv', encoding='ISO-8859-1')['Sentence'].tolist()
        st.success(f"Loaded default question bank with {len(default_sentences)} sentences.")

    # Upload question bank
    st.subheader("Upload a Question Bank")
    uploaded_file = st.file_uploader("Upload a CSV or TXT file containing sentences.", type=['csv', 'txt'])

    sentences = default_sentences
    if uploaded_file is not None:
        sentences = process_uploaded_file(uploaded_file)
        if sentences:
            st.success(f"Successfully loaded {len(sentences)} sentences from the uploaded file.")
            st.write("### Available Sentences:")
            st.write(sentences)

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
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Recording... Please repeat the sentence.")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)

                recognized_text = recognizer.recognize_google(audio)
                st.success(f"Recognized Text: {recognized_text}")

                # Step 4: Calculate Scores
                input_sentence_no_punctuation = selected_sentence.translate(str.maketrans('', '', string.punctuation))
                recognized_text_no_punctuation = recognized_text.translate(str.maketrans('', '', string.punctuation))

                # Content Score
                words_in_input = input_sentence_no_punctuation.split()
                words_in_recognized = recognized_text_no_punctuation.split()
                matched_words = sum(1 for word in words_in_input if word in words_in_recognized)
                content_percentage = (matched_words / len(words_in_input)) * 100
                content_score = 3 if content_percentage == 100 else 2 if content_percentage >= 50 else 1 if content_percentage >= 25 else 0

                # Fluency Score
                num_words = len(recognized_text.split())
                fluency_score = 5 if num_words >= 6 else 4 if num_words >= 4 else 3 if num_words >= 3 else 2 if num_words == 2 else 1

                # Pronunciation Score
                seq = difflib.SequenceMatcher(None, input_sentence_no_punctuation, recognized_text_no_punctuation)
                pronunciation_score = np.round(seq.ratio() * 5, 1)

                # Total Score
                total_score = content_score + pronunciation_score + fluency_score

                # Display Results
                st.subheader("Grading Results")
                st.metric("Content Score", f"{content_score}/3")
                st.metric("Pronunciation Score", f"{pronunciation_score}/5")
                st.metric("Fluency Score", f"{fluency_score}/5")
                st.metric("Total Score", f"{total_score}/13")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Run the application
if __name__ == "__main__":
    main()
