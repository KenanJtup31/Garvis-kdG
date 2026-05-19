import streamlit as st
from groq import Groq

# 1. Tətbiq Konfiqurasiyası
st.set_page_config(page_title="Langur Jarvis", page_icon="🤖", layout="wide")

# 2. CSS Dizayn
st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #c9d1d9; }
.footer { text-align: center; color: #58a6ff; font-size: 0.8rem; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# 3. Beyin (Groq) - Secrets istifadə edir!
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []

# 4. Giriş Ekranı
st.title("🐒 Langur Jarvis")
st.caption("Developed by Əlizadə Kənan | KDG")

# 5. Söhbət Məntiqi
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if sual := st.chat_input("Jarvisə bir şey soruş..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis analiz edir..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            cavab = response.choices[0].message.content
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
          
