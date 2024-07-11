import streamlit as st
from gtts import gTTS
from googletrans import Translator
import os
import base64

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Function to convert text to speech and save as an MP3 file
def convert_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)
        return True
    return False

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

def main():
    st.title("Text to Audio Conversion ")

    # Get user input
    text = st.text_area("Enter text to convert to speech:", height=300)

    target_language = st.selectbox("Select text language:", ["en","hi", "es","te", "fr","it","gu","mr","ta","ur","bn"])  # Add more languages as needed

    # Add a button to trigger the text-to-speech conversion
    if st.button("Convert to Speech and Download Audio"):
        output_file = "output.mp3"
        
        # Translate text to the selected language
        translated_text = translate_text(text, target_language)

        # Convert translated text to speech
        success = convert_text_to_speech(translated_text, output_file, language=target_language)

        if success:
            # Play the generated speech
            audio_file = open(output_file, 'rb')
            st.audio(audio_file.read(), format='audio/mp3')

            # Provide a download link for the MP3 file
            st.markdown(get_binary_file_downloader_html("Download Audio File", output_file, 'audio/mp3'), unsafe_allow_html=True)
        else:
            st.warning("Failed to generate audio. Please check your input.")

if __name__ == "__main__":
    main()
