import streamlit as st
import wikipedia
from groq import Groq

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core", page_icon="⚡", layout="centered")
wikipedia.set_lang("az")

# --- 2. CSS DİZAYN ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; }
    .header-box { text-align: center; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. YARADICI MƏLUMATLARI ---
CREATOR_NAME = "Kənan Əlizadə (KDG)"
CREATOR_INFO = "7 may 2011-ci ildə İsmayıllıda doğulub. Süni intellekt və nanotexnologiya üzrə mütəxəssisdir."

# --- 4. API AÇARI ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- 5. BAŞLIQ ---
st.markdown(f"""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE</h1>
    <p>Developed by <b>{CREATOR_NAME}</b></p>
</div>
""", unsafe_allow_html=True)

# --- 6. SİSTEMİN ŞƏXSİYYƏTİ ---
SYSTEM_PROMPT = f"Sənin adın Kenano-dur. Yaradıcın {CREATOR_NAME}-dir. Sən qısa və dəqiq cavab verən süni intellektsən."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- 7. SÖHBƏT EKRANI ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 8. YAZI YAZMA YERİ (ƏN AŞAĞIDA) ---
st.markdown("---")
st.subheader("⌨️ Komanda Paneli")
user_input = st.chat_input("Komandanı daxil et, Kənan...")

if user_input:
    # Ekranda göstər
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Wikipedia axtarışı və Groq cavabı
    try:
        search_results = wikipedia.search(user_input)
        if search_results:
            ozet = wikipedia.summary(search_results[0], sentences=2)
            cavab = f"Kenan, {ozet}"
        else:
            cavab = "Bu mövzuda məlumat tapa bilmədim."
    except:
        cavab = "Kenano: Məlumatı tapmaqda çətinlik çəkirəm."

    with st.chat_message("assistant"):
        st.markdown(cavab)
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
