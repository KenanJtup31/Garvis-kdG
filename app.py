import streamlit as st
import time
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from pypdf import PdfReader

# 1. Təhlükəsiz Açar (Heç vaxt KeyError verməyəcək)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# 2. Dizayn
st.set_page_config(page_title="Langur AI", page_icon="🇦🇿")
st.markdown("""
<style>
    .stApp { background: #000000; color: white; }
    .stChatMessage { border-radius: 20px; background: #1c1c1e; }
</style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Langur AI Pro")

# 3. Məntiq
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": "Sənin adın Langur-dur. Səni Kənan Əlizadə (KDG) yaradıb."}]

# Fayl yükləmə
uploaded_file = st.file_uploader("Sənəd yüklə (PDF):", type=["pdf"])
if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])
    st.session_state.messages.append({"role": "system", "content": f"Sənəd məzmunu: {text[:2000]}"})
    st.success("Sənəd oxundu!")

# Çat
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

if sual := st.chat_input("Langura bir şey soruş..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        cavab = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": cavab})
        st.markdown(cavab)
            
