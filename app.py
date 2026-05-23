import streamlit as st
from groq import Groq
import time
from datetime import datetime

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="KENANO AI | ANIMATED PRO", layout="wide")

# --- 2. CSS ANIMASIYALAR VƏ STİLLƏR ---
st.markdown("""
    <style>
        /* Animasiya effekti */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .stChatMessage { animation: fadeIn 0.5s ease-out; }
        
        /* Yazı sahəsinin ölçüsü və aktivliyi */
        div[data-testid="stChatInput"] { 
            z-index: 999999 !important; 
            position: fixed; 
            bottom: 20px; 
            width: 95%; 
            margin: auto;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .header-box { text-align: center; padding: 20px; border: 1px solid #333; border-radius: 15px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DİL VƏ MƏTN ---
def get_ui(lang):
    return {
        "Azərbaycan": {"title": "⚡ KENANO AI", "input": "Mesajını yaz və göndər..."},
        "English": {"title": "⚡ KENANO AI", "input": "Type your message..."}
    }.get(lang, {"title": "⚡ KENANO AI", "input": "Type..."})

lang = st.sidebar.selectbox("Language", ["Azərbaycan", "English"])
ui = get_ui(lang)

# --- 4. API VƏ SESSİYA ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state: st.session_state.messages = []

# --- 5. HEADER ---
st.markdown(f"<div class='header-box'><h1>{ui['title']}</h1><p>Developer: Kənan Əlizadə</p></div>", unsafe_allow_html=True)

# --- 6. SÖHBƏT VƏ ANIMASİYALI GÖSTƏRİŞ ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(ui['input']):
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Assistant mesajı (Animasiya ilə)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Xəta baş verdi: {e}"
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 7. FOOTER ---
st.markdown("<br><br><br><div style='text-align:center; color:gray;'>KENANO AI v12.0 | ANIMATED CORE</div>", unsafe_allow_html=True)
