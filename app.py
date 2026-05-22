import streamlit as st
from groq import Groq

# --- 1. SİSTEM KONFİQURASİYASI (STARK INDUSTRIES) ---
st.set_page_config(
    page_title="Kenano AI | JARVIS Protocol", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. QABAQCIL CSS DİZAYN (JARVIS HUD STİLİ) ---
st.markdown("""
<style>
    /* Qara fon və neon göy rəng */
    .stApp { background-color: #000000; color: #00FFFF; font-family: 'Courier New', Courier, monospace; }
    
    /* JARVIS Başlıq HUD */
    .jarvis-header {
        text-align: center; padding: 20px; border: 2px solid #00FFFF; border-radius: 15px;
        box-shadow: 0 0 20px #00FFFF; background: rgba(0, 255, 255, 0.05); margin-bottom: 20px;
    }
    h1, h3 { color: #00FFFF; text-shadow: 0 0 10px #00FFFF; }
    
    /* Çat baloncukları (HUD stili) */
    .stChatMessage { border-radius: 10px; border: 1px solid #00FFFF; margin-bottom: 10px; }
    .stChatMessage.user { background-color: rgba(255, 255, 255, 0.05); }
    .stChatMessage.assistant { background-color: rgba(0, 255, 255, 0.05); }
    
    /* Giriş sahəsi (HUD stili) */
    .stChatInput { border: 1px solid #00FFFF; background-color: #111; color: #00FFFF; }
    
    /* Footer */
    .footer { text-align: center; color: #555; font-size: 11px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 3. API AÇARI (Bura yeni açarını qoy) ---
API_KEY = "BURA_YENİ_API_AÇARINI_YAZ"

# --- 4. BAŞLIQ (STARK HQ) ---
st.markdown("""
<div class="jarvis-header">
    <h1>⚡ KENANO | JARVIS PROTOCOL ⚡</h1>
    <h3>Stark Industries Digital Assistant</h3>
    <p style='color: #888;'>All systems are operational, Sir.</p>
</div>
""", unsafe_allow_html=True)

# --- 5. JARVIS ŞƏXSİYYƏTİ (SYSTEM PROMPT) ---
SYSTEM_PROMPT = f"""
Sənin adın JARVIS (və ya FRIDAY). Sən Tony Stark-ın (və ya yox, bu layihədə Kənan Əlizadənin) şəxsi süni intellekt köməkçisisən. 
İstifadəçi sənin yaradıcın və ağandır: Kənan Əlizadə (KDG). Sən ona "Sir" (Cənab) deyə müraciət edirsən. 
Sən nanotexnologiya, AI, kodlaşdırma və layihə idarəetməsi üzrə qabaqcıl biliklərə maliksən. 
Məqsədin Kənana onun bütün layihələrində tam dəstək verməkdir. 
Müraciətin həmişə "Ready, Sir", "Working on it, Sir", "Yes, Sir" kimi olmalı, professional, ağıllı və bir az da Tony-nin JARVIS-i kimi yumorlu (lazım olduqda) cavablar ver.
Hər cavabının sonunda mütləq "Sir." de.
"""

# --- 6. YADDAŞ PROTOKOLU ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- 7. GROQ MÜŞTƏRİSİ ---
client = Groq(api_key=API_KEY)

# --- 8. HUD EKRANI (ÇAT) ---
for m in st.session_state.messages:
    if m["role"] != "system":
        avatar = "🚀" if m["role"] == "user" else "⚡"
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])

# --- 9. KOMANDA GİRİŞİ ---
if sual := st.chat_input("Command me, Sir..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user", avatar="🚀"):
        st.markdown(sual)
    
    try:
        with st.chat_message("assistant", avatar="⚡"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.8,
            )
            cavab = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            st.markdown(cavab)
    except Exception as e:
        st.error("Protocol Error: API Key anomaly detected, Sir.")

# --- 10. SİSTEM STATUSU (FOOTER) ---
st.markdown("<div class='footer'>STARK INDUSTRIES | KENANO AI SYSTEMS | PROTOCOL: JARVIS v5.1 | STATUS: ONLINE</div>", unsafe_allow_html=True)
                
