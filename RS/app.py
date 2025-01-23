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

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Run the application
if __name__ == "__main__":
    main()
Updated requirements.txt
Add the required dependencies to your requirements.txt file:

plaintext
Copy
Edit
streamlit
gTTS
pandas
numpy
SpeechRecognition
Steps to Deploy
Push Changes to GitHub:

Save the updated app.py and requirements.txt.
Commit and push the changes:
bash
Copy
Edit
git add app.py requirements.txt
git commit -m "Add microphone-based recording and scoring functionality"
git push origin <branch_name>
Redeploy the App:

Go to Streamlit Cloud.
Ensure the repository and branch are correctly linked.
Deploy the app using the main file (RS/app.py).
Expected Outcome
The app will allow users to select or input a sentence.
Users can listen to the sentence, record their speech, and view detailed scores for content, fluency, and pronunciation.
Let me know if you encounter any issues!







You said:
Step 1: Select or Input a Sentence
Choose a sentence to practice:

Please write your name on the essay cover sheet.
Sentence selected!

Step 2: Listen to the Sentence
Click play to listen to the sentence and then repeat it.

Step 3: Record Your Speech
Ensure your microphone is enabled before starting!


An error occurred: Could not find PyAudio; check installation
ChatGPT said:
ChatGPT
The Could not find PyAudio error indicates that the SpeechRecognition library requires the PyAudio package, which is not installed or is failing to install in your environment. This is a common issue when deploying apps on environments like Streamlit Cloud where low-level system libraries like PyAudio are not pre-installed.

Solution: Replace PyAudio with Alternative Recording
Since PyAudio often leads to compatibility issues, we can use an alternative approach to accept uploaded audio files instead of live microphone recording. This eliminates the need for PyAudio altogether.

Updated Full Code (Using Audio File Upload)
Here’s the updated app.py code where users upload their recorded audio files instead of using a live microphone:

python
Copy
Edit
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
