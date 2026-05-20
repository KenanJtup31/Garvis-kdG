import streamlit as st
import time

# --- SİSTEMİN DİZAYNI ---
st.set_page_config(page_title="Kenano AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    h1 {color: #FFD700; text-align: center;}
    .dev-name {text-align: center; color: #888888; margin-bottom: 30px;}
    .chat-bubble {background: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 4px solid #FFD700; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIQ VƏ İMZA ---
st.markdown("<h1>⚡ KENANO COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p class='dev-name'>Developed by Kenan Elizade</p>", unsafe_allow_html=True)

# --- SÖHBƏT YADDAŞI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- KEÇMİŞ SÖHBƏTLƏRİ GÖSTƏR ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- SÖHBƏT MƏNTİQİ ---
if prompt := st.chat_input("Komandanı daxil et..."):
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kenano-nun "Simulyasiya" cavabı
    with st.chat_message("assistant", avatar="⚡"):
        message_placeholder = st.empty()
        full_response = f"Sistem hazır! Sənin '{prompt}' əmrini qəbul etdim, Kənan. Kenano bütün funksiyaları ilə aktivdir."
        
        # Yazılma effekti
        typing_effect = ""
        for char in full_response:
            typing_effect += char
            message_placeholder.markdown(typing_effect + "▌")
            time.sleep(0.02)
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
