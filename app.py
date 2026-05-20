import streamlit as st
from groq import Groq

# Sənin "Kenano" brendin
st.set_page_config(page_title="Kenano AI", page_icon="⚡")

# Rəngli başlıq və imza
st.markdown("""
    <h1 style='text-align: center; color: #FFD700;'>⚡ Kenano AI</h1>
    <p style='text-align: center;'><i>Developed by Kenan Elizade</i></p>
""", unsafe_allow_html=True)

# Söhbət tarixi (yaddaş)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Söhbəti göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş yeri (yazı yeri)
if prompt := st.chat_input("Sualını yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kenano-nun cavabı
    with st.chat_message("assistant"):
        response = f"Salam Kənan! Mən Kenano-yam, sənin əmrlərini yerinə yetirməyə hazıram. '{prompt}' üzərində işləyirəm."
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
