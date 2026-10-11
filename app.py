import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO AI | iOS Edition", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. APPLE / İPHONE MİNİMALİST DİZAYN (CSS) ---
st.markdown("""
    <style>
        /* Ümumi səhifə fonu və Apple şriftləri */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar dizaynı - iOS Split View tərzi */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid rgba(0, 0, 0, 0.06);
        }
        
        /* iPhone üslubunda minimalist kartlar (Glassmorphism & Soft Shadow) */
        .ios-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.8);
            margin-bottom: 20px;
        }
        
        /* Başlıq üslubu */
        .ios-title {
            color: #1d1d1f;
            font-weight: 700;
            font-size: 28px;
            letter-spacing: -0.5px;
            text-align: center;
            margin-bottom: 5px;
        }
        
        .ios-subtitle {
            color: #86868b;
            font-size: 15px;
            text-align: center;
            font-weight: 400;
            margin-bottom: 25px;
        }
        
        /* Mesaj qutularının tənzimlənməsi */
        .stChatMessage {
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }
        
        /* Chat input sətri */
        div[data-testid="stChatInput"] {
            border-radius: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            background: #ffffff;
            border: 1px solid #d2d2d7;
        }
        
        /* Düymələr */
        .stButton button {
            border-radius: 12px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        /* Footer hissəsi */
        .ios-footer {
            text-align: center;
            color: #86868b;
            font-size: 13px;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ÇOXDİLLİ LÜĞƏT (AZ, EN, RU) ---
translations = {
    "Azərbaycan": {
        "title": "⚡ KENANO AI",
        "subtitle": "Apple Tərzində Ağıllı Köməkçi və Tədqiqat Mərkəzi",
        "sidebar_control": "⚙️ İdarəetmə Paneli",
        "lang_label": "Dil Seçimi / Language",
        "mode_label": "Rejim Seçin",
        "modes": ["💬 Ağıllı Söhbət", "📝 Mətn Xülasəsi", "💻 Kod İzahçısı", "ℹ️ Layihə Haqqında"],
        "temp_label": "Yaradıcılıq Səviyyəsi (Temperature)",
        "tone_label": "Cavab Tonu",
        "tones": ["Səmimi & Dost", "Ciddi & Akademik", "Kreativ & Maraqlı"],
        "input_placeholder": "Mesajınızı buraya yazın...",
        "creator_info": "Bu layihə istedadlı proqramçı Kənan Əlizadə tərəfindən müasir iOS standartlarına uyğun olaraq hazırlanmışdır.",
        "summary_btn": "Xülasə Et",
        "summary_input": "Xülasə olunacaq mətni daxil edin:",
        "code_input": "İzah olunacaq kodu daxil edin:",
        "code_btn": "Kodu İzah Et"
    },
    "English": {
        "title": "⚡ KENANO AI",
        "subtitle": "Apple-Style Intelligent Assistant & Research Center",
        "sidebar_control": "⚙️ Control Panel",
        "lang_label": "Language Selection",
        "mode_label": "Select Mode",
        "modes": ["💬 Smart Chat", "📝 Text Summarizer", "💻 Code Explainer", "ℹ️ About Project"],
        "temp_label": "Creativity Level (Temperature)",
        "tone_label": "Response Tone",
        "tones": ["Friendly & Casual", "Serious & Academic", "Creative & Engaging"],
        "input_placeholder": "Type your message here...",
        "creator_info": "This project was created by talented programmer Kenan Alizade according to modern iOS standards.",
        "summary_btn": "Summarize",
        "summary_input": "Enter text to summarize:",
        "code_input": "Enter code to explain:",
        "code_btn": "Explain Code"
    },
    "Русский": {
        "title": "⚡ KENANO AI",
        "subtitle": "Умный помощник в стиле Apple и центр исследований",
        "sidebar_control": "⚙️ Панель управления",
        "lang_label": "Выбор языка",
        "mode_label": "Выберите режим",
        "modes": ["💬 Умный чат", "📝 Резюме текста", "💻 Анализ кода", "ℹ️ О проекте"],
        "temp_label": "Уровень творчества (Temperature)",
        "tone_label": "Тон ответа",
        "tones": ["Дружелюбный", "Серьезный и академичный", "Креативный"],
        "input_placeholder": "Введите ваше сообщение...",
        "creator_info": "Этот проект разработан талантливым программистом Кянаном Ализаде в соответствии с современными стандартами iOS.",
        "summary_btn": "Сделать резюме",
        "summary_input": "Введите текст для резюме:",
        "code_input": "Введите код для объяснения:",
        "code_btn": "Объяснить код"
    }
}

# --- 4. SIDEBAR (AYARLAR VƏ İDARƏETMƏ) ---
with st.sidebar:
    st.markdown("###  KENANO AI OS")
    lang_choice = st.selectbox("🌐 Language / Dil / Язык", ["Azərbaycan", "English", "Русский"])
    ui = translations[lang_choice]
    
    st.divider()
    st.markdown(f"**{ui['sidebar_control']}**")
    app_mode = st.radio(ui['mode_label'], ui['modes'])
    
    temp = st.slider(ui['temp_label'], 0.0, 1.0, 0.7)
    selected_tone = st.selectbox(ui['tone_label'], ui['tones'])
    
    st.divider()
    st.info(ui['creator_info'])

# --- 5. API BAĞLANTISI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"API Connection Error: {e}")

# Sessiya yaddaşı
if "messages" not in st.session_state: 
    st.session_state.messages = [{
        "role": "system", 
        "content": "Sənin adın KENANO AI-dır. Sənin yaradıcın və tərtibatçın Kənan Əlizadə-dir. Həmişə Apple məhsulları kimi zərif, təmiz, dəqiq və peşəkar cavablar ver. Kənan Əlizadənin istedadlı proqramçı olduğunu qürurla qeyd et."
    }]

# --- 6. ƏSAS EKRAN & REJİMLƏR ---
st.markdown(f"<div class='ios-title'>{ui['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='ios-subtitle'>{ui['subtitle']}</div>", unsafe_allow_html=True)

# Rejim 1: Ağıllı Söhbət (Smart Chat)
if app_mode == ui['modes'][0]:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    
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
                message_placeholder.markdown(f"❌ Xəta: {e}")
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    st.markdown('</div>', unsafe_allow_html=True)

# Rejim 2: Mətn Xülasəsi (Text Summarizer)
elif app_mode == ui['modes'][1]:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.subheader("📝 " + ui['modes'][1])
    text_to_summarize = st.text_area(ui['summary_input'], height=150)
    if st.button(ui['summary_btn'], use_container_width=True):
        if text_to_summarize:
            with st.spinner("İşlənir..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": "Sən peşəkar mətn xülasəedicisən."},
                        {"role": "user", "content": f"Bu mətni qısa və səliqəli şəkildə xülasə et: {text_to_summarize}"}
                    ],
                    temperature=0.3
                )
                st.success("Nəticə:")
                st.write(response.choices[0].message.content)
        else:
            st.warning("Zəhmət olmasa mətn daxil edin.")
    st.markdown('</div>', unsafe_allow_html=True)

# Rejim 3: Kod İzahçısı (Code Explainer)
elif app_mode == ui['modes'][2]:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.subheader("💻 " + ui['modes'][2])
    code_snippet = st.text_area(ui['code_input'], height=150)
    if st.button(ui['code_btn'], use_container_width=True):
        if code_snippet:
            with st.spinner("Kod təhlil edilir..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": "Sən təcrübəli proqramlaşdırma müəllimisən. Kodları səlis və başa düşülən şəkildə izah edirsən."},
                        {"role": "user", "content": f"Bu kodu addım-addım izah et: \n\n{code_snippet}"}
                    ],
                    temperature=0.3
                )
                st.success("İzah:")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Zəhmət olmasa kod daxil edin.")
    st.markdown('</div>', unsafe_allow_html=True)

# Rejim 4: Layihə Haqqında (About)
elif app_mode == ui['modes'][3]:
    st.markdown('<div class="ios-card">', unsafe_allow_html=True)
    st.subheader("ℹ️ Layihə Haqqında")
    st.markdown("""
    * **Layihə Adı:** KENANO AI
    * **Tərtibatçı:** Kənan Əlizadə
    * **Dizayn Konsepsiyası:** Apple Human Interface Guidelines (Minimalist, Zərif iOS Kartları)
    * **Texnologiyalar:** Python, Streamlit, Groq Cloud API, LLaMA/GPT OSS arxitekturası.
    * **Xüsusiyyətlər:** Çoxdilli dəstək (Azərbaycan, İngilis, Rus), Süni İntellekt Söhbəti, Sürətli Mətn Xülasəsi və Kod İzahı.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown("<div class='ios-footer'>KENANO AI v15.0 Pro | DESIGNED FOR EXCELLENCE BY KENAN ALIZADE</div>", unsafe_allow_html=True)
    
