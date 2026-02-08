import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# Mengambil API Key secara aman dari Secrets Streamlit Cloud
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("Masukkan GEMINI_API_KEY di menu Secrets Streamlit!")

st.title("🎬 AI Prompt Finder @rizgotutorial")

uploaded_file = st.file_uploader("Unggah Video", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)
    
    if st.button("✨ Hasilkan Prompt"):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            st.info("Sedang mengunggah ke AI Engine...")
            video_file = genai.upload_file(path=tmp_path)
            
            # Menunggu proses AI (ini yang menyebabkan error 'time' sebelumnya)
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            models = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([video_file, "Buatkan prompt detail untuk video ini."])
            
            st.success("Prompt Berhasil Ditemukan!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.remove(tmp_path)                
