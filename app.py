from audiorecorder import audiorecorder
from gtts import gTTS
import speech_recognition as sr
import streamlit as st
from groq import Groq

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; }
    .header-box { text-align: center; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; }
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 50px; }
    .stChatInput { border: 1px solid #FFD700; }
</style>
""", unsafe_allow_html=True)

# --- 3. YARADICI MƏLUMATLARI ---
CREATOR_NAME = "Kənan Əlizadə (KDG)"
CREATOR_INFO = "7 may 2011-ci ildə İsmayıllıda doğulub. Süni intellekt və nanotexnologiya üzrə mütəxəssisdir."

# --- 4. API AÇARI (Bura yeni açarını qoy) ---
API_KEY = "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"

# --- 5. BAŞLIQ ---
st.markdown(f"""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE</h1>
    <p>Developed by <b>{CREATOR_NAME}</b></p>
</div>
""", unsafe_allow_html=True)

# --- 6. SİSTEMİN ŞƏXSİYYƏTİ (SYSTEM PROMPT) ---
SYSTEM_PROMPT = f"""
Sənin adın Kenano-dur. Sən {CREATOR_NAME} tərəfindən yaradılmış qabaqcıl AI sistemisən. 
Yaradıcın haqqında məlumat: {CREATOR_INFO}. 
Sən heç vaxt başqa bir AI (Meta AI, ChatGPT və s.) olduğunu demə. 
Sənin tək yaradıcın Kənan Əlizadə-dir. 
Sual verildikdə qısa, dəqiq, professional və səmimi cavab ver.
"""

# --- 7. YADDAŞ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- 8. GROQ MÜŞTƏRİSİ ---
client = Groq(api_key=API_KEY)

# --- 9. SÖHBƏT EKRANI ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            # --- MASTER CORE INTELLIGENCE BLOCK (Bunu app.py-ın sonuna əlavə et) ---

# 1. Yazı ilə komanda vermək üçün yer
user_input = st.text_input("Komandanı daxil et, Kənan...")
if user_input:
    try:
        if any(word in user_input.lower() for word in ["salam", "necəsən"]):
            st.write("**Kenano:** Merhaba Kenan, iyiyim. Sənə necə kömək edə bilərəm?")
        else:
            ozet = wikipedia.summary(user_input, sentences=2)
            st.success(f"**Kenano:** {ozet}")
    except:
        st.write("Kenano: Bu mövzuda məlumat tapa bilmədim.")

st.markdown("---")

# 2. Səslə danışmaq üçün Master Core
st.subheader("🎤 Kenano Ağıllı Səs Modu")
audio = audiorecorder("🎤 Səslə Danış", "Dayandır")

if audio:
    audio.export("sesim.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile("sesim.wav") as source:
        audio_data = r.record(source)
        try:
            sual = r.recognize_google(audio_data, language="az-AZ")
            st.write(f"**Sən dedin:** {sual}")
            
            # Sosial salamlaşma və Wikipedia məntiqi
            if any(word in sual.lower() for word in ["salam", "necəsən", "əleyküm"]):
                cavab = "Merhaba Kenan, iyiyim, teşekkür ederim."
            else:
                ozet = wikipedia.summary(sual, sentences=2)
                cavab = f"Kenan, {ozet}"
            
            st.write(f"**Kenano:** {cavab}")
            tts = gTTS(text=cavab, lang='tr')
            tts.save("cavab.mp3")
            st.audio("cavab.mp3", format="audio/mp3")
        except:
            st.error("Üzr istəyirəm, bu mövzuda məlumat tapa bilmədim.")
            
