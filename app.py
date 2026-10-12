import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODERN VƏ SADƏ DİZAYN (CSS) ---
st.markdown("""
    <style>
        /* Tünd minimalist fon */
        .stApp {
            background-color: #000000;
            color: #e5e5e7;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        /* Sidebar tənzimləməsi */
        [data-testid="stSidebar"] {
            background-color: #0f0f11;
            border-right: 1px solid #1f1f23;
        }
        [data-testid="stSidebar"] * {
            color: #e5e5e7 !important;
        }
        
        /* Sadə və müasir başlıq */
        .modern-header {
            text-align: center;
            padding: 20px 0 10px 0;
        }
        .modern-title {
            color: #ffffff;
            font-size: 24px;
            font-weight: 500;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        .modern-copyright {
            color: #6e6e73;
            font-size: 12px;
            letter-spacing: 0.5px;
        }
        
        /* Mesaj qutuları */
        .stChatMessage {
            background-color: #161618;
            border-radius: 12px;
            border: 1px solid #26262a;
        }
        
        /* Chat input */
        div[data-testid="stChatInput"] input {
            background-color: #161618 !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ÇOXDİLLİ LÜĞƏT ---
translations = {
    "Azərbaycan": {
        "sidebar_control": "Tənzimləmələr",
        "lang_label": "Dil",
        "mode_label": "Rejim",
        "modes": ["Söhbət", "Xülasə", "Kod Analizi", "Haqqında"],
        "temp_label": "Temperatur",
        "input_placeholder": "Mesajınızı yazın...",
        "creator_info": "Kənan Əlizadə tərəfindən hazırlanmışdır."
    },
    "English": {
        "sidebar_control": "Settings",
        "lang_label": "Language",
        "mode_label": "Mode",
        "modes": ["Chat", "Summary", "Code Analysis", "About"],
        "temp_label": "Temperature",
        "input_placeholder": "Type your message...",
        "creator_info": "Developed by Kenan Alizade."
    },
    "Русский": {
        "sidebar_control": "Настройки",
        "lang_label": "Язык",
        "mode_label": "Режим",
        "modes": ["Чат", "Резюме", "Анализ кода", "О программе"],
        "temp_label": "Температура",
        "input_placeholder": "Введите сообщение...",
        "creator_info": "Разработано Кянаном Ализаде."
    }
}

# --- 4. SIDEBAR ---
with st.sidebar:
    lang_choice = st.selectbox("Dil / Language / Язык", ["Azərbaycan", "English", "Русский"])
    ui = translations[lang_choice]
    
    st.divider()
    app_mode = st.radio(ui['mode_label'], ui['modes'])
    temp = st.slider(ui['temp_label'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.caption(ui['creator_info'])

# --- 5. API BAĞLANTISI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Xəta: {e}")

if "messages" not in st.session_state: 
    st.session_state.messages = [{
        "role": "system", 
        "content": "Sənin adın KENANO-dur. Yaradıcın Kənan Əlizadədir. Qısa, səliqəli və sadə cavablar ver."
    }]

# --- 6. MODERN VƏ SADƏ HEADER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="modern-header">
        <div class="modern-title">KENANO</div>
        <div class="modern-copyright">© {current_year} KENAN ALIZADE. ALL RIGHTS RESERVED.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222225; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- 7. REJİMLƏR ---
if app_mode == ui['modes'][0]:
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input(ui['input_placeholder']):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
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
                message_placeholder.markdown(f"Xəta: {e}")
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})

elif app_mode == ui['modes'][1]:
    st.subheader(ui['modes'][1])
    text_to_summarize = st.text_area("Mətn daxil edin:", height=150)
    if st.button("Xülasə Et", use_container_width=True):
        if text_to_summarize:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "Sən mətn xülasəedicisən."},
                    {"role": "user", "content": f"Bu mətni qısa xülasə et: {text_to_summarize}"}
                ],
                temperature=0.3
            )
            st.write(response.choices[0].message.content)
        else:
            st.warning("Mətn daxil edin.")

elif app_mode == ui['modes'][2]:
    st.subheader(ui['modes'][2])
    code_snippet = st.text_area("Kod daxil edin:", height=150)
    if st.button("Analiz Et", use_container_width=True):
        if code_snippet:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "Sən proqramlaşdırma mütəxəssisiyəm."},
                    {"role": "user", "content": f"Bu kodu izah et: \n\n{code_snippet}"}
                ],
                temperature=0.3
            )
            st.markdown(response.choices[0].message.content)
        else:
            st.warning("Kod daxil edin.")

elif app_mode == ui['modes'][3]:
    st.subheader(ui['modes'][3])
    st.markdown("""
    * **Sistem:** KENANO AI
    * **Müəllif:** Kənan Əlizadə
    * **Status:** Aktiv & Stabil
    """)
            
