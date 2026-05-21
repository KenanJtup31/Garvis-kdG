import streamlit as st
import wikipedia
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Kenano AI | Master Core", layout="centered")
wikipedia.set_lang("az")

# 2. CSS
st.markdown("<style>.stApp { background: #000; color: #fff; }</style>", unsafe_allow_html=True)

# 3. Başlıq
st.markdown("<h1 style='text-align: center;'>⚡ KENANO AI MASTER CORE</h1>", unsafe_allow_html=True)

# 4. Groq Client
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Söhbət Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. YAZI YERİ (Ən aşağıda)
if prompt := st.chat_input("Komandanı daxil et, Kənan..."):
    # İstifadəçi mesajı
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ağıllı cavab mexanizmi (Wikipedia + Groq)
    try:
        # Wikipedia-dan məlumat axtar
        search = wikipedia.summary(prompt, sentences=2)
        cavab = f"Wikipedia-dan tapdığım məlumata görə: {search}"
    except:
        # Wikipedia tapa bilməzsə Groq-a müraciət et
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        cavab = chat_completion.choices[0].message.content

    # Cavabı göstər
    with st.chat_message("assistant"):
        st.markdown(cavab)
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
