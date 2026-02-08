import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# 1. Setting API Key dari Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key_asli = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key_asli)
else:
    st.error("❌ API Key tidak ditemukan di Secrets!")

# 2. Tampilan UI
st.title("🎬 AI Prompt Finder @rizgotutorial")
st.markdown("---")

uploaded_file = st.file_uploader("Unggah Video Anda", type=["mp4", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("✨ Hasilkan Prompt", use_container_width=True):
        # Membuat file sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            st.info("🔄 Sedang mengunggah dan memproses video...")
            
            # Proses Upload ke Google
            video_file = genai.upload_file(path=tmp_path)
            
            # Menunggu proses AI (menggunakan module time)
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            # Inisialisasi Model (Menggunakan nama model yang benar)
            # Baris ini yang sebelumnya menyebabkan error 'name model is not defined'
            model_ai = genai.GenerativeModel('gemini-1.5-flash')
            
            # Perintah ke AI
            response = model_ai.generate_content([
                video_file, 
                "Tolong buatkan prompt detail dalam Bahasa Indonesia untuk video ini agar bisa dibuat ulang di AI video generator."
            ])
            
            st.success("✅ Prompt Berhasil Ditemukan!")
            st.markdown("### Hasil Prompt:")
            st.write(response.text)
            
            # Hapus file dari server Google setelah selesai
            genai.delete_file(video_file.name)
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
            
        finally:
            # Hapus file sementara dari memori aplikasi
            if os.path.exists(tmp_path):
                os.remove(tmp_path)            
            st.success("Prompt Berhasil Ditemukan!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.remove(tmp_path)                
