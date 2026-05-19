import streamlit as st
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Langur Jarvis", page_icon="🤖", layout="wide")

# 2. Açarın təyin edilməsi (Həm Secrets-ə baxır, həm də ehtiyat halı var)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# 3. Məntiq
if "messages" not in st.session_state: 
    st.session_state.messages = []

st.title("🐒 Langur Jarvis")
st.caption("Developed by Əlizadə Kənan | KDG")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

if sual := st.chat_input("Jarvisə bir şey soruş..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): 
        st.markdown(sual)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis analiz edir..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            cavab = response.choices[0].message.content
            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
          
