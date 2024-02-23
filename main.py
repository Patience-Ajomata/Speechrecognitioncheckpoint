import streamlit as st
import speech_recognition as sr
import os


def transcribe_speech(language, api):
    try:
        # Initialize recognizer class
        r = sr.Recognizer()

        # Reading Microphone as source
        with sr.Microphone() as source:
            st.info("Speak now...")
            # listen for speech and store in audio_text variable
            audio_text = r.listen(source)
            st.info("Transcribing...")

        # Perform speech recognition based on the selected API
        if api == "Google Speech Recognition":
            text = r.recognize_google(audio_text, language=language)
        else:
            return "Invalid speech recognition API selected."
        return text

    except sr.RequestError:
        return "Sorry, there was an issue with the speech recognition service."


# Press the green button in the gutter to run the script.
def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")

    language = st.selectbox("Select the language you are speaking in:", ["English"])

    speech_recognition_apis = ["Google Speech Recognition"]
    selected_api = st.selectbox("Select the speech recognition API:", speech_recognition_apis)

    # Map selected language to language code for speech recognition
    language_code = "en-US"

    # add a button to trigger speech recognition
    recording = False
    if st.button("Start Recording"):
        recording = True

    if recording:
        text = transcribe_speech(language_code, selected_api)
        st.write("Transcription: ", text)

    if st.button("Stop Recording"):
        recording = False

    if st.button("Save to File"):
        if recording:
            st.warning("Please stop recording before saving the transcription.")
        else:
            save_directory = st.text_input("Enter the directory path to save the file:")
            if save_directory.strip() != "Scripts":
                file_path = os.path.join(save_directory, "transcription.txt")
                try:
                    with open(file_path, "w") as file:
                        file.write(text)
                    st.success("Transcription saved to file.")
                except IOError:
                    st.error("Failed to save the file.")
            else:
                st.warning("No directory path provided. Please enter a valid directory path.")

    if recording:
        st.warning("Recording is in progress...")

    if st.button("Pause Recording"):
        if recording:
            recording = False
            st.write("Recording paused.")
        else:
            st.warning("Recording is not in progress. Cannot pause.")

if __name__ == '__main__':
    main()
