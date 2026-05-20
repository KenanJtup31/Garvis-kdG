import streamlit as st
import time
from groq import Groq
from streamlit_mic_recorder import mic_recorder
from pypdf import PdfReader

# Dizayn (Apple tərzi)
st.set_page_config(page_title="Langur AI", page_icon="🇦🇿")
st.markdown("""
<style>
    .stApp { background: #000000; color: white; }
    .stChatMessage { border-radius: 20px; background: #1c1c1e; }
    div[data-testid="stFileUploader"] { border: 2px dashed #3a3a3c; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# Başlıq
st.title("🇦🇿 Langur AI Pro")
st.markdown("<p style='color: #8e8e93;'>Developed by Kənan Əlizadə | KDG</p>", unsafe_allow_html=True)

# Beyin
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Fayl yükləmə
uploaded_file = st.file_uploader("Sənəd yüklə (PDF/TXT):", type=["pdf", "txt"])
if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])
    st.info("Sənəd analiz olundu. İndi sual verə bilərsən.")
    st.session_state.messages.append({"role": "system", "content": f"Analiz edilən mətn: {text[:2000]}"})

# Səsli əmr (Mikrofon)
audio = mic_recorder(key="audio", text="Səsli sual ver", icon="🎤")
if audio:
    st.write("Səs qəbul edildi!") # Burada audio-to-text funksiyası üçün model əlavə olunmalıdır

# Mesajlaşma
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": "Sənin adın Langur-dur. Səni Kənan Əlizadə (KDG) yaradıb."}]

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
