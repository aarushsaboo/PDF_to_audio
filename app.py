import pdfplumber
from gtts import gTTS
from io import BytesIO
import streamlit as st
import time

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to convert text to audio
def text_to_audio(text):
    tts = gTTS(text, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

st.set_page_config(page_title="PDF to Audio Converter", page_icon="🔊")

st.title("🔊 PDF to Audio Converter")

st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #1e90ff;
    }
</style>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.expander("📄 PDF Content", expanded=True):
        st.info("Extracting text from PDF...")
        pdf_text = extract_text_from_pdf(uploaded_file)
        
        if pdf_text:
            st.text_area("Extracted Text", pdf_text, height=200)
        else:
            st.error("No text found in the PDF.")

    if pdf_text:
        st.markdown("---")
        st.subheader("🎵 Audio Conversion")
        
        progress_bar = st.progress(0)
        status_text = st.empty()

        # for i in range(100):
        #     progress_bar.progress(i + 1)
        #     status_text.text(f"Converting: {i+1}%")
        #     time.sleep(0.01)
        #I want the progress bar to actually display what % of conversion is already done and what's left, instead of just counting to 100... That creates a more visually appealing display

        audio_file = text_to_audio(pdf_text)
        
        st.success("Conversion complete!")
        st.audio(audio_file, format='audio/mp3')
        
        st.markdown("---")