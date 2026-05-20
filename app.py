import streamlit as st
from groq import Groq
import time
import datetime
import pandas as pd

# --- 1. SİSTEMİN İLKİN PARAMETRLƏRİ ---
st.set_page_config(
    page_title="Kenano AI | Master Core", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. QABAQCIL CSS STİLLƏRİ ---
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {border: 1px solid #333; border-radius: 10px;}
    .stButton>button {width: 100%; border-radius: 5px; border: 1px solid #FFD700; color: #FFD700;}
    .reportview-container {background: #000;}
    </style>
""", unsafe_allow_html=True)

# --- 3. İDARƏETMƏ PANELİ (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/200/000000/artificial-intelligence.png", width=150)
    st.title("⚡ Kenano OS Control")
    st.markdown("---")
    api_key = st.text_input("🔑 System API Key:", type="password")
    model_choice = st.selectbox("🧠 Neural Engine:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    
    st.subheader("System Stats")
    status = st.empty()
    status.markdown("✅ **Status: Online**")
    
    if st.button("⚠️ Emergency Purge Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ƏSAS PANEL (HEADER) ---
st.markdown("<h1 style='color: #FFD700;'>⚡ KENANO MASTER COMMAND CORE ⚡</h1>", unsafe_allow_html=True)
st.markdown("**Developer:** Kenan Elizade | **Environment:** Production | **Uptime:** 99.9%")
st.markdown("---")

# --- 5. YADDAŞ VƏ KONTEKST ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sən Kenano-san, Kənan Elizadə tərəfindən kodlaşdırılmış qabaqcıl AI sistemisən. Hər zaman analitik, professional və səmimi cavablar ver."}
    ]

# --- 6. SÖHBƏT MƏNTİQİ ---
if api_key:
    client = Groq(api_key=api_key)
    
    # Söhbəti ekrana çıxar
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # İstifadəçi girişi
    if prompt := st.chat_input("Daxil et..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Cavablandırma
        with st.chat_message("assistant", avatar="⚡"):
            try:
                # Real-time cavablaşma
                full_response = ""
                placeholder = st.empty()
                stream = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                    stream=True,
                    temperature=0.7,
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Sistem Anomaliyası: {str(e)}")
else:
    st.info("Sistemi işə salmaq üçün API açarınızı yan paneldən daxil edin.")

# --- 7. SİSTEM ANALİTİKA FOOTER ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Memory Usage", "128MB", "+2.4MB")
col2.metric("Response Time", "0.4s", "-0.1s")
col3.metric("Neural Nodes", "70B", "Active")
                
