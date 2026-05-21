import streamlit as st
import wikipedia
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Kenano AI | Master Core", layout="centered")
wikipedia.set_lang("az")

# 2. CSS (Dizaynı qoruyuruq)
st.markdown("""
<style>
    .stApp { background: #000; color: #fff; }
    .header-box { text-align: center; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. BAŞLIQ (QAYTARDIM)
st.markdown("""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE</h1>
    <p>Developed by <b>Kənan Əlizadə (KDG)</b></p>
</div>
""", unsafe_allow_html=True)

# 4. Groq və Wikipedia
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Söhbət Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. YAZI YERİ (Ən aşağıda)
if prompt := st.chat_input("Komandanı daxil et, Kənan..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ağıllı cavab (Salam və s. üçün)
    low_prompt = prompt.lower()
    if any(x in low_prompt for x in ["salam", "necəsən", "kim"]):
        if "salam" in low_prompt: cavab = "Salam, Kənan! Sənə necə kömək edə bilərəm?"
        elif "necəsən" in low_prompt: cavab = "Əladayam! Yeni tapşırıqlarını gözləyirəm."
        else: cavab = "Mən Kenano-yam, sənin şəxsi AI köməkçin."
    else:
        try:
            search = wikipedia.summary(prompt, sentences=2)
            cavab = f"Kenano: {search}"
        except:
            chat = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama3-8b-8192")
            cavab = f"Kenano: {chat.choices[0].message.content}"

    with st.chat_message("assistant"):
        st.markdown(cavab)
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
