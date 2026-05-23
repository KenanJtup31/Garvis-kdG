import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
import os

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN (Düzəldilib) ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 30px; border: 3px solid #FFD700; border-radius: 25px; background: #0a0a0a; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .header-box h1 { color: #FFD700; margin-bottom: 5px; }
    .header-box p { color: #94a3b8; font-size: 16px; margin: 0; }
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 60px; padding: 20px; border-top: 1px solid #1e293b; }
    .stChatInput { border: 2px solid #334155 !important; border-radius: 15px !important; margin-top: 10px !important; }
    .stChatInput:focus-within { border-color: #FFD700 !important; }
    .upload-btn-container { text-align: center; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 3. API AÇARLARI ---
GROQ_API_KEY = "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"

# --- 4. BAŞLIQ ---
st.markdown("""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE PRO</h1>
    <p>Developed by <b>Kənan Əlizadə</b></p>
</div>
""", unsafe_allow_html=True)

# --- 5. SİSTEMİN ŞƏXSİYYƏTİ ---
SYSTEM_PROMPT = "Sənin adın Kenano-dur. Kənan Əlizadə tərəfindən yaradılmısan. Onunla dost kimi danış. Hərf səhvi etmə."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

groq_client = Groq(api_key=GROQ_API_KEY)

# --- 6. FOTOMAX FUNKSİYASI ---
def analyze_image_groq(image_bytes, user_prompt):
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [{"type": "text", "text": user_prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Dostum, şəkli analiz edərkən xəta oldu: {e}"

# --- 7. SÖHBƏT EKRANI ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 8. GİRİŞ VƏ MƏNTİQ ---
if "input_source" not in st.session_state: st.session_state.input_source = "mətn"

if st.button("➕ Şəkil əlavə et"): st.session_state.input_source = "şəkil"
if st.button("❌ Mətn rejimi"): st.session_state.input_source = "mətn"

uploaded_file = None
if st.session_state.input_source == "şəkil":
    uploaded_file = st.file_uploader("Şəkli seç", type=["jpg", "jpeg", "png"])

if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)
    
    with st.chat_message("assistant", avatar="⚡"):
        if uploaded_file:
            cavab = analyze_image_groq(uploaded_file.getvalue(), sual)
        else:
            response = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
            cavab = response.choices[0].message.content
        st.markdown(cavab)
        st.session_state.messages.append({"role": "assistant", "content": cavab})

st.markdown("<div class='footer'>KENANO AI MASTER CORE | DEVELOPED BY KƏNAN ƏLİZADƏ</div>", unsafe_allow_html=True)
