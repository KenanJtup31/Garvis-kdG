import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="KENANO AI | ULTIMATE PRO", layout="wide")

# --- DATABASE TƏNZİMLƏMƏSİ ---
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (role TEXT, content TEXT, timestamp DATETIME)''')
    conn.commit()
    return conn

def save_message(role, content):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (role, content, datetime.now()))
    conn.commit()
    conn.close()

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
        "Azərbaycan": {"title": "⚡ KENANO AI", "input": "Mesajını yaz...", "temp": "Temperatur", "feedback": "Rəy və Şikayət", "info": "Haqqımızda", "placeholder": "Bura yazın..."},
        "English": {"title": "⚡ KENANO AI", "input": "Type your message...", "temp": "Temperature", "feedback": "Feedback", "info": "About", "placeholder": "Write here..."}
    }
    return data.get(lang, data["English"])

# --- 4. SIDEBAR - AYARLAR, FEEDBACK VƏ HAQQIMIZDA ---
with st.sidebar:
    lang = st.selectbox("Language / Dil", ["Azərbaycan", "English"])
    ui = get_ui(lang)
    temp = st.slider(ui['temp'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.subheader(f"💬 {ui['feedback']}")
    feedback = st.text_area(ui['placeholder'])
    if st.button("Send Feedback"):
        st.success("Təşəkkürlər!")
    
    st.divider()
    st.subheader(f"ℹ️ {ui['info']}")
    st.info("Mən Kənan Elızade tərəfindən yaradılmış ilk layihəyəm. Gələcəkdə bir çox layihələrdə istifadə olunacağam.")
    
    if st.button("Sessiyanı Təmizlə (Reset)"):
        conn = init_db()
        conn.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        st.rerun()

# --- 5. API VƏ SESSİYA ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- 6. HEADER ---
st.markdown(f"<div class='header-box'><h1>{ui['title']}</h1><p>Developed by Kenan Elızade</p></div>", unsafe_allow_html=True)

# --- 7. SÖHBƏT VƏ TARİXCƏ ---
conn = init_db()
c = conn.cursor()
c.execute("SELECT role, content FROM messages")
history = c.fetchall()
conn.close()

for role, content in history:
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input(ui['input']):
    save_message("user", prompt)
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": r, "content": c} for r, c in history] + [{"role": "user", "content": prompt}],
                stream=True,
                temperature=temp
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Xəta: {e}"
            message_placeholder.markdown(full_response)
        
        save_message("assistant", full_response)

# --- 8. FOOTER ---
st.markdown("<br><br><br><div style='text-align:center; color:gray;'>KENANO AI v14.0 | FULL FEATURES ENABLED</div>", unsafe_allow_html=True)
        
