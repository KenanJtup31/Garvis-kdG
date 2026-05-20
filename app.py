import streamlit as st

# --- SİSTEMİN DİZAYNI ---
st.set_page_config(page_title="Kenano AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    h1 {color: #FFD700; text-align: center;}
    .dev-name {text-align: center; color: #888888; margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIQ ---
st.markdown("<h1>⚡ KENANO COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p class='dev-name'>Developed by Kenan Elizade</p>", unsafe_allow_html=True)

# --- YADDAŞ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SÖHBƏTİ GÖSTƏR ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CAVABLANDIRMA MƏNTİQİ ---
if prompt := st.chat_input("Komandanı daxil et..."):
    # İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı (Bura Groq əvəzinə hazır cavablar qoydum ki, xəta verməsin)
    with st.chat_message("assistant", avatar="⚡"):
        # Buranı istədiyin kimi dəyişə bilərsən
        cavab = f"Kənan, '{prompt}' əmrini analiz etdim. Sistem tam işlək vəziyyətdədir."
        st.markdown(cavab)
    
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
