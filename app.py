import streamlit as st
import google.generativeai as genai
import tempfile
import os

# --- KONFIGURASI API ---
# Masukkan API Key Anda di sini
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key belum dikonfigurasi di Secrets Streamlit!")
# --- FUNGSI PROSES VIDEO ---
def process_video_to_prompt(video_path, bahasa):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Unggah file ke Google File API
    st.info("Sedang mengunggah ke AI Engine...")
    video_file = genai.upload_file(path=video_path)
    
    # Tunggu proses pemrosesan video di sisi server Google
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    # Instruksi Prompt
    prompt_instruction = f"""
    Analisis video ini secara mendalam. 
    Berikan deskripsi teknis (Reverse Prompt) agar orang lain bisa membuat ulang video serupa.
    Sertakan: subjek, aksi, pencahayaan, gaya kamera, dan suasana.
    Tuliskan hasilnya dalam {bahasa}.
    Akhiri dengan satu paragraf 'Final Prompt' yang siap digunakan.
    """
    
    response = model.generate_content([video_file, prompt_instruction])
    
    # Hapus file dari server Google setelah selesai (opsional)
    genai.delete_file(video_file.name)
    
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
