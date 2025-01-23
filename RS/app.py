import streamlit as st
from gtts import gTTS
import os
import string
import difflib
import numpy as np
import pandas as pd
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from google.cloud import speech

# Function to play audio
def play_audio(file_path):
    st.audio(file_path, format='audio/mp3')

# Function to record audio using sounddevice
def record_audio(duration=5, sample_rate=44100):
    st.info(f"Recording for {duration} seconds...")
    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write(temp_file.name, sample_rate, audio)  # Save audio as WAV file
        return temp_file.name
    except Exception as e:
        st.error(f"An error occurred while recording: {e}")
        return None

# Function to process audio with Google Cloud Speech-to-Text
def process_audio_with_google(file_path):
    try:
        client = speech.SpeechClient()
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            return result.alternatives[0].transcript
    except Exception as e:
        st.error(f"An error occurred during speech recognition: {e}")
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
            temp_audio_path = record_audio()
            if temp_audio_path:
                recognized_text = process_audio_with_google(temp_audio_path)
                if recognized_text:
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
                    fluency_score = round(5 if num_words >= 6 else 4 if num_words >= 4 else 3 if num_words >= 3 else 2 if num_words == 2 else 1, 1)

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

# Run the application
if __name__ == "__main__":
    main()
