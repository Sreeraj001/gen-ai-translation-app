from io import StringIO
import streamlit as st
from PyPDF2 import PdfReader
from language_code import lan_code
import pandas as pd
from dotenv import load_dotenv
import os
from translator import translate_text
from audio import text_to_speech


text = ''

st.title('Welcome to Text translator')
st.subheader('Choose a file or provide your text in the box')

try:
    uploaded_file = st.file_uploader(label='', accept_multiple_files=False, type= ['pdf', 'txt', 'xlsx', 'csv'], key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            pdf = PdfReader(uploaded_file)
            for page in pdf.pages:
                text += page.extract_text() or ''
        elif uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
        elif uploaded_file.type in ["text/csv", "application/vnd.ms-excel"]:
            df = pd.read_csv(uploaded_file)
            text = df.to_string()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text = df.to_string()
        else:
            st.error(f"Invalid file type. Please upload a PDF, TXT, CSV, or XLSX file. You uploaded a file of type: {uploaded_file.type}")

    input_text = st.text_area('Provide your text here', value = text, height = 300)
    language = st.selectbox('Select a language', lan_code.keys())

    if st.button('Translate'):
        if input_text:
            with st.spinner('Translating...'):
                translated_text = translate_text(input_text, language)
            col1, col2 = st.columns(2)
            with col1:
                try:
                    audio_bytes = text_to_speech(translated_text, lang=lan_code[language])
                    st.audio(audio_bytes, format='audio/mp3')
                except Exception as e:
                    st.error(f"Text-to-speech conversion failed: {e}")
            with col2:  
                st.download_button(label= 'Download Audio', data=audio_bytes, file_name='translated_audio.mp3', mime='audio/mp3')
            st.text('Translated text')
            st.write(translated_text)
        else:
            st.error('Please provide text to translate')

except ValueError as ve:
    st.error("Please check your API key and ensure it is set correctly.")
except Exception as e:
    st.error(f"An error occurred: Please try again later. Error details:")






