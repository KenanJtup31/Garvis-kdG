import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
# OpenAI-ı düzgün istifadə etmək üçün tələb olunan kitabxana
from openai import OpenAI 

# --- SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- CSS DİZAYN ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 30px; border: 3px solid #FFD700; border-radius: 25px; background: #0a0a0a; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .header-box h1 { color: #FFD700; margin-bottom: 5px; }
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 60px; padding: 20px; border-top: 1px solid #1e293b; }
    .upload-btn-container { text-align: center; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIQ ---
st.markdown("""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE PRO</h1>
    <p>Developed by <b>Kənan Əlizadə</b></p>
</div>
""", unsafe_allow_html=True)

# --- API ---
GROQ_API_KEY = "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"
# OpenAI açarını bura əlavə et
OPENAI_API_KEY = "BURA_OPENAI_ACARINI_YAZ"

groq_client = Groq(api_key=GROQ_API_KEY)

# --- ŞƏKİL ANALİZİ (YENİLƏNMİŞ MODEL) ---
def analyze_image_groq(image_bytes, user_prompt):
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = groq_client.chat.completions.create(
            model="llama-3.2-90b-vision-preview", # Əgər yenə xəta versə, "llama-3.2-11b-vision-preview" yaz
            messages=[{"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xəta: {e}"

# --- MƏNTİQ ---
if "input_source" not in st.session_state:
    st.session_state.input_source = "mətn"

st.markdown('<div class="upload-btn-container">', unsafe_allow_html=True)
if st.button("➕ Şəkil əlavə et"):
    st.session_state.input_source = "şəkil"
st.markdown('</div>', unsafe_allow_html=True)

uploaded_file = None
if st.session_state.input_source == "şəkil":
    uploaded_file = st.file_uploader("Şəkli seç", type=["jpg", "png"])
    if st.button("❌ Mətn rejiminə qayıt"):
        st.session_state.input_source = "mətn"
        st.rerun()

if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    with st.chat_message("user"):
        st.markdown(sual)
    
    with st.chat_message("assistant", avatar="⚡"):
        if uploaded_file:
            cavab = analyze_image_groq(uploaded_file.getvalue(), sual)
        else:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": sual}]
            )
            cavab = response.choices[0].message.content
        st.markdown(cavab)

st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADE</div>", unsafe_allow_html=True)
