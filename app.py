import streamlit as st
import wikipedia
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Kenano AI | Master Core", layout="centered")
wikipedia.set_lang("az")
# 2. CSS - Yazı yerini və stili tənzimləmək üçün
st.markdown("""
<style>
    .stApp { background: #000; color: #fff; }
    /* Yazı yerinin çərçivəsini qızılı rəngdə və səliqəli etdik */
    .stChatInput textarea {
        border: 2px solid #FFD700 !important;
        border-radius: 15px !important;
        background-color: #1a1a1a !important;
        color: white !important;
    }
    /* Söhbət balonlarını tənzimləyirik */
    [data-testid="stChatMessage"] {
        background-color: #0a0a0a;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Groq Client
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Söhbət Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. YAZI YERİ (Ən aşağıda)
if prompt := st.chat_input("Komandanı daxil et, Kənan..."):
    # İstifadəçi mesajı
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AĞILLI MƏNTİQ (Bura şərəfsizcəsinə dəqiqdir)
    low_prompt = prompt.lower()
    
    if any(x in low_prompt for x in ["salam", "necəsən", "kim", "yaradıb"]):
        # Sosial cavablar
        if "salam" in low_prompt: cavab = "Salam, Kənan! Necəsən? Sənə necə kömək edə bilərəm?"
        elif "necəsən" in low_prompt: cavab = "Əladayam, Kənan! Yeni komandalarını gözləyirəm."
        elif "kim" in low_prompt: cavab = "Məni Kənan Əlizadə (KDG) yaradıb, mən onun Master Core-uyam!"
        else: cavab = "Mən Kenano-yam, sənin şəxsi AI köməkçin."
    else:
        # Wikipedia və ya Groq
        try:
            search = wikipedia.summary(prompt, sentences=2)
            cavab = f"Kenano: {search}"
        except:
            chat = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama3-8b-8192")
            cavab = f"Kenano: {chat.choices[0].message.content}"

    # Cavabı göstər
    with st.chat_message("assistant"):
        st.markdown(cavab)
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
