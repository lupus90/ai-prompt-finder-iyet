import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# Konfigurasi API
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
            
            while v_file.state.name == "PROCESSING":
                time.sleep(2)
                v_file = genai.get_file(v_file.name)

            # LOGIKA AUTO-FIX MODEL
            try:
                # Coba cara standar pertama
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content([v_file, "Buat prompt video ini."])
            except:
                # Jika gagal, cari model flash yang tersedia di sistem
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                flash_model = next((m for m in available_models if 'flash' in m), available_models[0])
                model = genai.GenerativeModel(flash_model)
                res = model.generate_content([v_file, "Buat prompt video ini."])
            
            st.success("✅ Berhasil!")
            st.write(res.text)
            genai.delete_file(v_file.name)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
        finally:
            if os.path.exists(path_tmp):
                os.remove(path_tmp)
