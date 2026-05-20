import streamlit as st
from groq import Groq
import time
import datetime

# --- 1. SİSTEMİN KONSEPSİYASI VƏ İMZASI ---
# Bu hissə sistemin "ürəyidir"
st.set_page_config(page_title="Kenano AI Pro | Enterprise", page_icon="⚡", layout="wide")

def display_header():
    st.markdown("""
        <div style='background-color: #0e1117; padding: 25px; border-radius: 15px; border: 2px solid #FFD700; text-align: center;'>
            <h1 style='color: #FFD700; margin: 0;'>⚡ KENANO AI SYSTEM CORE ⚡</h1>
            <p style='color: #888888; font-size: 16px;'>Developed and Engineered by <b>Kenan Elizade</b></p>
            <p style='color: #555555; font-size: 12px;'>Status: ACTIVE | Model: Llama-3.3-70B | Session ID: #KDG-2026</p>
        </div>
    """, unsafe_allow_html=True)

display_header()

# --- 2. API BAĞLANTISI VƏ TƏHLÜKƏSİZLİK ---
client = Groq(api_key="BURA_YENİ_API_AÇARINI_YAZ")

# --- 3. SİSTEMİN YADDAŞI VƏ KONTEKST İDARƏETMƏSİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sən Kenano-san, Kenan Elizade tərəfindən yaradılmış qabaqcıl AI sistemisən. Sən hər zaman professional, dəqiq və müasir texnologiyalarla bağlı dərin biliklərə malik bir köməkçisən."}
    ]

# --- 4. SÖHBƏTİN VİZUAL İNTERFEYSİ ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. İŞ MƏNTİQİ (CORE PROCESSING) ---
def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.7,
            max_tokens=2048
        )
        return response
    except Exception as e:
        return f"Sistem xətası: {str(e)}"

# --- 6. ƏSAS İCRA VƏ CAVABLANDIRMA ---
if prompt := st.chat_input("Komandanı daxil et, Kənan..."):
    # İstifadəçi mesajını yazdır
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Kenano analiz edir..."):
            stream = get_ai_response(prompt)
            response = st.write_stream(stream)
    
    # Cavabı yaddaşda saxla
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 7. SİSTEMİN ALT BİTİRİCİSİ ---
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    st.caption(f"İstifadə vaxtı: {datetime.datetime.now().strftime('%H:%M:%S')}")
with col2:
    st.caption("Kenano AI Engine v2.0 - Optimized for Speed & Accuracy")
                         
