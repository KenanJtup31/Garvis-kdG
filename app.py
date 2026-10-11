import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO AI", 
    page_icon="💻", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TÜND (QARA) MİNİMALİST DİZAYN (CSS) ---
st.markdown("""
    <style>
        /* Tünd fon və təmiz Apple şriftləri */
        .stApp {
            background-color: #0b0b0c;
            color: #f5f5f7;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
        }
        
        /* Sidebar tünd dizaynı */
        [data-testid="stSidebar"] {
            background-color: #141416;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] * {
            color: #f5f5f7 !important;
        }
        
        /* Kart dizaynı */
        .ios-card {
            background: #1c1c1e;
            padding: 24px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 20px;
        }
        
        /* Başlıqlar */
        .ios-title {
            color: #ffffff;
            font-weight: 600;
            font-size: 26px;
            text-align: center;
            letter-spacing: -0.5px;
            margin-bottom: 5px;
        }
        
        .ios-subtitle {
            color: #8e8e93;
            font-size: 14px;
            text-align: center;
            margin-bottom: 25px;
        }
        
        /* Söhbət mesajları */
        .stChatMessage {
            background-color: #1c1c1e;
            border-radius: 14px;
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Chat input */
        div[data-testid="stChatInput"] input {
            background-color: #1c1c1e !important;
            color: #ffffff !important;
        }
        
        /* Footer */
        .ios-footer {
            text-align: center;
            color: #8e8e93;
            font-size: 12px;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ÇOXDİLLİ LÜĞƏT (AZ, EN, RU - Emojisiz) ---
translations = {
    "Azərbaycan": {
        "title": "KENANO AI",
        "subtitle": "Süni İntellekt Sistemi",
        "sidebar_control": "İdarəetmə Paneli",
        "lang_label": "Dil Seçimi",
        "mode_label": "Rejim Seçin",
        "modes": ["Söhbət", "Mətn Xülasəsi", "Kod Analizi", "Haqqında"],
        "temp_label": "Yaradıcılıq Səviyyəsi",
        "tone_label": "Cavab Tonu",
        "tones": ["Səmimi", "Ciddi", "Kreativ"],
        "input_placeholder": "Mesajınızı yazın...",
        "creator_info": "Bu layihə Kənan Əlizadə tərəfindən hazırlanmışdır.",
        "summary_btn": "Xülasə Et",
        "summary_input": "Xülasə olunacaq mətn:",
        "code_input": "İzah olunacaq kod:",
        "code_btn": "Kodu İzah Et"
    },
    "English": {
        "title": "KENANO AI",
        "subtitle": "Artificial Intelligence System",
        "sidebar_control": "Control Panel",
        "lang_label": "Language",
        "mode_label": "Select Mode",
        "modes": ["Chat", "Text Summary", "Code Analysis", "About"],
        "temp_label": "Creativity Level",
        "tone_label": "Response Tone",
        "tones": ["Friendly", "Serious", "Creative"],
        "input_placeholder": "Type your message...",
        "creator_info": "This project was created by Kenan Alizade.",
        "summary_btn": "Summarize",
        "summary_input": "Text to summarize:",
        "code_input": "Code to explain:",
        "code_btn": "Explain Code"
    },
    "Русский": {
        "title": "KENANO AI",
        "subtitle": "Система Искусственного Интеллекта",
        "sidebar_control": "Панель управления",
        "lang_label": "Язык",
        "mode_label": "Выберите режим",
        "modes": ["Чат", "Резюме текста", "Анализ кода", "О программе"],
        "temp_label": "Уровень творчества",
        "tone_label": "Тон ответа",
        "tones": ["Дружелюбный", "Серьезный", "Креативный"],
        "input_placeholder": "Введите сообщение...",
        "creator_info": "Этот проект разработан Кянаном Ализаде.",
        "summary_btn": "Сделать резюме",
        "summary_input": "Текст для резюме:",
        "code_input": "Код для анализа:",
        "code_btn": "Объяснить код"
    }
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### İdarəetmə")
    lang_choice = st.selectbox("Dil / Language / Язык", ["Azərbaycan", "English", "Русский"])
    ui = translations[lang_choice]
    
    st.divider()
    app_mode = st.radio(ui['mode_label'], ui['modes'])
    
    temp = st.slider(ui['temp_label'], 0.0, 1.0, 0.7)
    selected_tone = st.selectbox(ui['tone_label'], ui['tones'])
    
    st.divider()
    st.caption(ui['creator_info'])

# --- 5. API BAĞLANTISI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"API Xətası: {e}")

if "messages" not in st.session_state: 
    st.session_state.messages = [{
        "role": "system", 
        "content": "Sənin adın KENANO AI-dır. Sənin yaradıcın Kənan Əlizadə-dir. Həmişə qısa, səliqəli, təmiz və peşəkar cavablar ver."
    }]

# --- 6. ƏSAS EKRAN ---
st.markdown(f"<div class='ios-title'>{ui['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='ios-subtitle'>{ui['subtitle']}</div>", unsafe_allow_html=True)

# Rejim 1: Söhbət
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

# Rejim 2: Xülasə
elif app_mode == ui['modes'][1]:
    st.subheader(ui['modes'][1])
    text_to_summarize = st.text_area(ui['summary_input'], height=150)
    if st.button(ui['summary_btn'], use_container_width=True):
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

# Rejim 3: Kod Analizi
elif app_mode == ui['modes'][2]:
    st.subheader(ui['modes'][2])
    code_snippet = st.text_area(ui['code_input'], height=150)
    if st.button(ui['code_btn'], use_container_width=True):
        if code_snippet:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "Sən proqramlaşdırma üzrə mütəxəssissən."},
                    {"role": "user", "content": f"Bu kodu izah et: \n\n{code_snippet}"}
                ],
                temperature=0.3
            )
            st.markdown(response.choices[0].message.content)
        else:
            st.warning("Kod daxil edin.")

# Rejim 4: Haqqında
elif app_mode == ui['modes'][3]:
    st.subheader(ui['modes'][3])
    st.markdown("""
    * Sistem: KENANO AI
    * Yaradıcı: Kənan Əlizadə
    * Dizayn: Minimalist Tünd Rejim (Dark Mode)
    * Dəstəklənən Dillər: Azərbaycan, İngilis, Rus
    """)

# --- 7. FOOTER ---
st.markdown("<div class='ios-footer'>KENANO AI | DEVELOPED BY KENAN ALIZADE</div>", unsafe_allow_html=True)
