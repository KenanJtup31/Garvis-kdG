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
API_KEY = "BURA_YENİ_API_AÇARINI_YAZ"

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

# --- 10. SÖHBƏT MƏNTİQİ ---
if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)
    
    try:
        with st.chat_message("assistant", avatar="⚡"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            cavab = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            st.markdown(cavab)
    except Exception as e:
        st.error("Sistem xətası: API açarını yoxla və ya yenidən cəhd et.")

# --- 11. FOOTER ---
st.markdown(f"<div class='footer'>KENANO AI SYSTEM v3.0 | DEVELOPED BY {CREATOR_NAME.upper()}</div>", unsafe_allow_html=True)
