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
            # --- KENANO MASTER CORE INTELLIGENCE BLOCK ---
import wikipedia
from googlesearch import search
from audiorecorder import audiorecorder
from gtts import gTTS
import speech_recognition as sr

wikipedia.set_lang("az")

st.markdown("---")
st.subheader("🎤 Kenano Ağıllı Səs Modu")

# Səs yazma düyməsi
audio = audiorecorder("🎤 Səslə Danış", "Dayandır")

if audio:
    audio.export("sesim.wav", format="wav")
    r = sr.Recognizer()
    
    with sr.AudioFile("sesim.wav") as source:
        audio_data = r.record(source)
        try:
            sual = r.recognize_google(audio_data, language="az-AZ")
            st.write(f"**Sən dedin:** {sual}")
            
            # Siyasət və ya cari hadisədirsə Google axtarışı, yoxsa Wikipedia
            if "siyasət" in sual.lower() or "xeber" in sual.lower():
                st.write("Kenano xəbərləri araşdırır...")
                link = next(search(sual, num=1, stop=1, pause=2))
                cavab = f"Kenan, bu mövzu ilə bağlı ən son məlumatı buradan tapa bilərsən: {link}"
            else:
                st.write("Kenano Wikipedia-nı yoxlayır...")
                ozet = wikipedia.summary(sual, sentences=2)
                cavab = f"Kenan, {ozet}"
            
            st.write(f"**Kenano:** {cavab}")
            
            # Cavabı səsləndir
            tts = gTTS(text=cavab, lang='tr')
            tts.save("cavab.mp3")
            st.audio("cavab.mp3", format="audio/mp3")
            
        except Exception as e:
            st.error("Üzr istəyirəm, bu mövzuda məlumat tapa bilmədim.")
    
