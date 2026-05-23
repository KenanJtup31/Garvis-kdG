import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import os

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 20px; border: 2px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; }
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 50px; }
    .stButton>button { border-radius: 50%; width: 50px; height: 50px; background: #FFD700; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIQ ---
st.markdown("""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE PRO</h1>
    <p>Developed by <b>Kənan Əlizadə</b></p>
</div>
""", unsafe_allow_html=True)

# --- 4. CLIENT QURULUMU ---
# API açarını Streamlit-in 'Secrets' hissəsinə qoymaq ən təhlükəsizidir, 
# amma kodda dəyişiklik etmədən işlətmək üçün buranı belə saxlayıram:
try:
    groq_client = Groq(api_key="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")
except:
    st.error("API Açarında xəta var!")

# --- 5. FUNKSİYALAR ---
def analyze_image(image_bytes, prompt):
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = groq_client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Hazırda vizual analiz modeli əlçatmazdır. Lütfən, sadəcə mətnlə davam et."

# --- 6. SÖHBƏT MƏNTİQİ ---
if "input_mode" not in st.session_state: st.session_state.input_mode = False

if st.button("+"): st.session_state.input_mode = not st.session_state.input_mode

uploaded_file = None
if st.session_state.input_mode:
    uploaded_file = st.file_uploader("Şəkil seç:", type=["jpg", "png"])

if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    with st.chat_message("user"): st.markdown(sual)
    with st.chat_message("assistant", avatar="⚡"):
        if uploaded_file:
            st.markdown(analyze_image(uploaded_file.getvalue(), sual))
        else:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": sual}]
            )
            st.markdown(response.choices[0].message.content)

st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADƏ</div>", unsafe_allow_html=True)

