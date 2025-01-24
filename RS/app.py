import streamlit as st
from gtts import gTTS
import os
import string
import difflib
import numpy as np
import pandas as pd
from google.cloud import speech

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio_google(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response

# Main application
def main():
    st.title("🎙️ Speech Grader App")
    st.markdown("Evaluate your speaking fluency, pronunciation, and content match!")

    # Step 1: Input Sentence
    st.subheader("Step 1: Input a Sentence")
    default_sentence = "This is a sample sentence to repeat."
    selected_sentence = st.text_input("Enter or modify the sentence below:", default_sentence)

    if selected_sentence:
        st.success("Sentence selected!")

        # Step 2: Convert Text to Speech
        st.subheader("Step 2: Listen to the Sentence")
        tts = gTTS(text=selected_sentence, lang='en')
        tts.save("sentence.mp3")
        play_audio("sentence.mp3")

        # Step 3: Upload Speech
        st.subheader("Step 3: Upload Your Speech")
        uploaded_file = st.file_uploader("Upload a WAV file of your speech", type=["wav"])

        if uploaded_file is not None:
            st.audio(uploaded_file, format="audio/wav")
            st.info("Transcribing your speech...")

            # Transcribe uploaded audio
            try:
                with open("temp_uploaded.wav", "wb") as f:
                    f.write(uploaded_file.read())
                response = transcribe_audio_google("temp_uploaded.wav")
                recognized_text = response.results[0].alternatives[0].transcript
                st.success(f"Recognized Text: {recognized_text}")

                # Grading logic
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
                st.error(f"An error occurred during transcription: {e}")

# Run the application
if __name__ == "__main__":
    main()
