import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="KENANO AI | MASTER CORE", layout="wide")

# --- 2. CSS ANIMASIYALAR VƏ STİLLƏR ---
st.markdown("""
    <style>
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .stChatMessage { animation: fadeIn 0.5s ease-out; }
        div[data-testid="stChatInput"] { z-index: 999999 !important; position: fixed; bottom: 20px; width: 95%; margin: auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .header-box { text-align: center; padding: 20px; border: 1px solid #FFD700; border-radius: 15px; margin-bottom: 20px; background: #0a0a0a; }
        .dev-info { font-size: 0.9em; color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DİL VƏ MƏTN LÜĞƏTİ ---
def get_ui(lang):
    data = {
        "Azərbaycan": {"title": "⚡ KENANO AI", "input": "Mesajını yaz...", "temp": "Temperatur", "feedback": "Rəy və Şikayət", "dev": "Developed by Kenan Elizade"},
        "English": {"title": "⚡ KENANO AI", "input": "Type your message...", "temp": "Temperature", "feedback": "Feedback & Issues", "dev": "Developed by Kenan Elizade"},
        "Русский": {"title": "⚡ KENANO AI", "input": "Введите сообщение...", "temp": "Температура", "feedback": "Отзывы и жалобы", "dev": "Developed by Kenan Elizade"},
        "Türkçe": {"title": "⚡ KENANO AI", "input": "Mesajınızı yazın...", "temp": "Sıcaklık", "feedback": "Geri bildirim", "dev": "Developed by Kenan Elizade"},
        "Deutsch": {"title": "⚡ KENANO AI", "input": "Nachricht eingeben...", "temp": "Temperatur", "feedback": "Feedback", "dev": "Developed by Kenan Elizade"},
        "Français": {"title": "⚡ KENANO AI", "input": "Entrez votre message...", "temp": "Température", "feedback": "Retour d'information", "dev": "Developed by Kenan Elizade"},
        "Italiano": {"title": "⚡ KENANO AI", "input": "Scrivi il tuo messaggio...", "temp": "Temperatura", "feedback": "Feedback", "dev": "Developed by Kenan Elizade"},
        "Español": {"title": "⚡ KENANO AI", "input": "Escribe tu mensaje...", "temp": "Temperatura", "feedback": "Comentarios", "dev": "Developed by Kenan Elizade"}
    }
    return data.get(lang, data["English"])

# --- 4. SIDEBAR - GENİŞLƏNDİRİLMİŞ AYARLAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712038.png", width=100)
    lang = st.selectbox("🌍 Language", ["Azərbaycan", "English", "Русский", "Türkçe", "Deutsch", "Français", "Italiano", "Español"])
    ui = get_ui(lang)
    
    st.divider()
    st.subheader("⚙️ Advanced Settings")
    temp = st.slider(ui['temp'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.subheader(f"📩 {ui['feedback']}")
    user_feedback = st.text_area("Şikayətinizi və ya təklifinizi bura yazın:")
    if st.button("Göndər"):
        st.success("Rəyiniz mənə çatdı, təşəkkürlər!")
        # Burada feedback-i saxlamaq üçün əlavə kod yaza bilərsən
        
    st.divider()
    st.markdown(f"<p class='dev-info'>{ui['dev']}<br>Version: 12.5 (Pro Core)</p>", unsafe_allow_html=True)

# --- 5. API VƏ SESSİYA ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state: st.session_state.messages = []

# --- 6. HEADER ---
st.markdown(f"<div class='header-box'><h1>{ui['title']}</h1><p>{ui['dev']}</p></div>", unsafe_allow_html=True)

# --- 7. SÖHBƏT VƏ ANIMASİYALI GÖSTƏRİŞ ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(ui['input']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
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
            full_response = f"Xəta baş verdi: {e}"
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown("<br><br><div style='text-align:center; color:gray;'>KENANO AI MASTER CORE | 2026 | ALL RIGHTS RESERVED</div>", unsafe_allow_html=True)
