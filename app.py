import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="KENANO AI | FIRST EDITION", layout="wide")

# --- 2. CSS ANIMASIYALAR ---
st.markdown("""
    <style>
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .stChatMessage { animation: fadeIn 0.5s ease-out; }
        div[data-testid="stChatInput"] { z-index: 999999 !important; position: fixed; bottom: 20px; width: 95%; margin: auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .header-box { text-align: center; padding: 20px; border: 2px solid #FFD700; border-radius: 15px; margin-bottom: 20px; background: #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DİL VƏ MƏTN LÜĞƏTİ ---
def get_ui(lang):
    data = {
        "Azərbaycan": {"title": "⚡ KENANO AI", "input": "Mesajını yaz...", "temp": "Temperatur", "info": "Haqqımızda"},
        "English": {"title": "⚡ KENANO AI", "input": "Type your message...", "temp": "Temperature", "info": "About"}
    }
    return data.get(lang, data["English"])

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    lang = st.selectbox("Language / Dil", ["Azərbaycan", "English"])
    ui = get_ui(lang)
    temp = st.slider(ui['temp'], 0.0, 1.0, 0.7)
    seriousness = st.selectbox("ciddilik / seriousness", ["Səmimi", "ciddi"])
    st.divider()
    st.subheader(f"ℹ️ {ui['info']}")
    st.info("Bu layihə Kənan Əlizadə tərəfindən yaradılmışdır. İlk süni intellekt layihəsidir.")

# --- 5. API VƏ SESSİYA ---
# BURAYA YENİ YARATDIĞIN AÇARI YAPIŞDIR (gsk_... ilə başlayan)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": "Sənin yaradıcın Kənan Əlizadə-dir."}]

# --- 6. HEADER ---
st.markdown(f"<div class='header-box'><h1>{ui['title']}</h1><p>Developed by Kenan Elızade</p></div>", unsafe_allow_html=True)

# --- 7. SÖHBƏT ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input(ui['input']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
                temperature=temp
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            message_placeholder.markdown(f"Xəta: API Açarını yoxlayın. {e}")
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown("<br><br><br><div style='text-align:center; color:gray;'>KENANO AI v13.0 | DEVELOPED BY KENAN ELIZADE</div>", unsafe_allow_html=True)
