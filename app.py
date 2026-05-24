import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="KENANO AI | FIRST EDITION", layout="wide")

# --- 2. CSS ANIMASIYALAR VƏ STİLLƏR ---
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
        "English": {"title": "⚡ KENANO AI", "input": "Type your message...", "temp": "Temperature", "feedback": "Feedback", "info": "About", "placeholder": "Write here..."},
        "Русский": {"title": "⚡ KENANO AI", "input": "Введите сообщение...", "temp": "Температура", "feedback": "Отзывы", "info": "О нас", "placeholder": "Пишите здесь..."},
        "Türkçe": {"title": "⚡ KENANO AI", "input": "Mesajınızı yazın...", "temp": "Sıcaklık", "feedback": "Geri Bildirim", "info": "Hakkımızda", "placeholder": "Buraya yazın..."},
        "Deutsch": {"title": "⚡ KENANO AI", "input": "Nachricht eingeben...", "temp": "Temperatur", "feedback": "Feedback", "info": "Über uns", "placeholder": "Hier schreiben..."},
        "Français": {"title": "⚡ KENANO AI", "input": "Entrez votre message...", "temp": "Température", "feedback": "Commentaires", "info": "À propos", "placeholder": "Écrivez ici..."}
    }
    return data.get(lang, data["English"])

# --- 4. SIDEBAR - AYARLAR VƏ FEEDBACK ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    lang = st.selectbox("Language / Dil", ["Azərbaycan", "English", "Русский", "Türkçe", "Deutsch", "Français"])
    ui = get_ui(lang)
    temp = st.slider(ui['temp'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.subheader(f"💬 {ui['feedback']}")
    feedback = st.text_area(ui['placeholder'])
    if st.button("Send Feedback"):
        st.success("Təşəkkürlər! Rəyiniz qeyd olundu.")
    
    st.divider()
    st.subheader(f"ℹ️ {ui['info']}")
    st.info("Bu layihə Kenan Elızade tərəfindən yaradılmışdır. Bu onun ilk süni intellekt layihəsidir və gələcəkdə bir çox layihələrdə istifadə ediləcək.")

# --- 5. API VƏ SESSİYA ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": "Sənin yaradıcın Kənan Elızade-dir. Sən onun ilk layihəsisən və gələcəkdə çoxlu layihələrdə istifadə olunacaqsan."}]

# --- 6. HEADER ---
st.markdown(f"<div class='header-box'><h1>{ui['title']}</h1><p>Developed by Kenan Elızade</p></div>", unsafe_allow_html=True)

# --- 7. SÖHBƏT VƏ ANIMASİYALI GÖSTƏRİŞ ---
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
            full_response = f"Xəta: {e}"
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 8. FOOTER ---
st.markdown("<br><br><br><div style='text-align:center; color:gray;'>KENANO AI v12.0 | DEVELOPED BY KENAN ELIZADE</div>", unsafe_allow_html=True)
            
def send_email_feedback(feedback_text):
    sender_email = "kelizade349@gmail.com"
    app_password = "usjjdyqmjfykhfhj" # Boşluqsuz 16 simvol
    receiver_email = "kelizade349@gmail.com"
    
    msg = MIMEText(f"Yeni Feedback:\n\n{feedback_text}")
    msg['Subject'] = "KENANO AI - Yeni Feedback"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Xəta baş verdi: {e}")
        return False
        
