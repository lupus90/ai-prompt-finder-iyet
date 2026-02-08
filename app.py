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

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([video_file, "Buatkan prompt detail untuk video ini."])
            
            st.success("Prompt Berhasil Ditemukan!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.remove(tmp_path)    
    return response.text

# --- UI STREAMLIT (STYLING RIZGOTUTORIAL) ---
st.set_page_config(page_title="AI Prompt Finder", page_icon="🔍")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .upload-box {
        border: 2px dashed #6366f1;
        background-color: rgba(99, 102, 241, 0.1);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white;'>AI Prompt Finder @rizgotutorial</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Dapatkan prompt dari video yang kamu unggah</p>", unsafe_allow_html=True)

with st.container():
    uploaded_file = st.file_uploader("Unggah Video (MP4/MOV)", type=["mp4", "mov"], label_visibility="visible")

    if uploaded_file:
        st.video(uploaded_file)
        
        st.markdown("<p style='color: white; font-size: 14px; margin-bottom: 5px;'>Bahasa Prompt:</p>", unsafe_allow_html=True)
        bahasa_pilihan = st.selectbox("", ["Bahasa Indonesia", "English"], label_visibility="collapsed")

        if st.button("✨ Hasilkan Prompt", use_container_width=True):
            try:
                # Simpan file sementara secara lokal
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                # Jalankan fungsi analisis
                with st.spinner("AI sedang menonton video Anda..."):
                    hasil_prompt = process_video_to_prompt(tmp_path, bahasa_pilihan)
                
                # Tampilkan Hasil
                st.success("Analisis Selesai!")
                st.markdown("### 📝 Prompt Hasil Deteksi:")
                st.info(hasil_prompt)
                
                # Bersihkan file sementara
                os.remove(tmp_path)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
