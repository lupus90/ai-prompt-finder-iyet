import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# Konfigurasi API yang lebih aman
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key tidak ditemukan di Secrets!")

st.title("🎬 AI Prompt Finder @rizgotutorial")

file_video = st.file_uploader("Unggah Video", type=["mp4", "mov"])

if file_video:
    st.video(file_video)
    if st.button("✨ Hasilkan Prompt"):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(file_video.read())
            path_tmp = tmp.name

        try:
            st.info("🔄 Memproses video...")
            v_file = genai.upload_file(path=path_tmp)
            
            # Menunggu proses upload/indexing
            while v_file.state.name == "PROCESSING":
                time.sleep(2)
                v_file = genai.get_file(v_file.name)

            # MENGATASI ERROR 404: Menggunakan nama model standar
            # Jika tetap 404, library Anda butuh update di requirements.txt
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            res = model.generate_content([v_file, "Buatkan prompt detail untuk video ini dalam Bahasa Indonesia."])
            
            st.success("✅ Berhasil!")
            st.write(res.text)
            
            # Bersihkan file di server Google
            genai.delete_file(v_file.name)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
        finally:
            if os.path.exists(path_tmp):
                os.remove(path_tmp)
