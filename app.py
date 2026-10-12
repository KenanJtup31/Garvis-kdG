import streamlit as st
from groq import Groq
from datetime import datetime

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO AI", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODERN DİZAYN VƏ ANIMASIYALAR (CSS) ---
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
            background-color: #0b0b0d;
            border-right: 1px solid #1f1f23;
        }
        [data-testid="stSidebar"] * {
            color: #e5e5e7 !important;
        }
        
        /* Mesajların açılma animasiyası (Fade In) */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stChatMessage {
            background-color: #161618;
            border-radius: 14px;
            border: 1px solid #26262a;
            animation: fadeIn 0.4s ease-out;
            margin-bottom: 12px;
        }
        
        /* Sadə və müasir başlıq */
        .modern-header {
            text-align: center;
            padding: 15px 0 5px 0;
        }
        .modern-title {
            color: #ffffff;
            font-size: 24px;
            font-weight: 500;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        .modern-copyright {
            color: #6e6e73;
            font-size: 11px;
            letter-spacing: 0.5px;
        }
        
        /* Chat input */
        div[data-testid="stChatInput"] input {
            background-color: #161618 !important;
            color: #ffffff !important;
            border-radius: 12px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ÇOXDİLLİ LÜĞƏT ---
translations = {
    "Azərbaycan": {
        "new_chat": "+ Yeni Söhbət",
        "history_title": "Son Söhbətlər",
        "mode_label": "Rejim",
        "modes": ["Söhbət", "Xülasə", "Kod Analizi", "Haqqında"],
        "temp_label": "Temperatur",
        "input_placeholder": "Mesajınızı yazın...",
        "creator_info": "Kənan Əlizadə tərəfindən hazırlanmışdır."
    },
    "English": {
        "new_chat": "+ New Chat",
        "history_title": "Recent Chats",
        "mode_label": "Mode",
        "modes": ["Chat", "Summary", "Code Analysis", "About"],
        "temp_label": "Temperature",
        "input_placeholder": "Type your message...",
        "creator_info": "Developed by Kenan Alizade."
    },
    "Русский": {
        "new_chat": "+ Новый чат",
        "history_title": "Недавние чаты",
        "mode_label": "Режим",
        "modes": ["Чат", "Резюме", "Анализ кода", "О программе"],
        "temp_label": "Температура",
        "input_placeholder": "Введите сообщение...",
        "creator_info": "Разработано Кянаном Ализаде."
    }
}

# --- 4. API BAĞLANTISI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Xəta: {e}")

# --- 5. AĞILLI BAŞLIQ GENERATORU (MÖVZUYA UYGUN AD QOYMAQ ÜÇÜN) ---
def generate_chat_title(first_message):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Verilən mesaja uyğun 2-4 sözdən ibarət qısa, dəqiq və səliqəli başlıq adı yarat. Yalnız başlığı yaz, dırnaq işarəsi və ya başqa simvol istifadə etmə."},
                {"role": "user", "content": first_message}
            ],
            temperature=0.3
        )
        title = response.choices[0].message.content.strip()
        return title[:30] # Çox uzun olmasın
    except:
        return first_message[:20] + "..."

# --- 6. SESSİYA VƏ TARİXÇƏ (CHATS STATE) ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Yeni Söhbət": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Yeni Söhbət"

# --- 7. SIDEBAR (TARİXÇƏ VƏ TƏNZİMLƏMƏLƏR) ---
with st.sidebar:
    lang_choice = st.selectbox("Dil / Language / Язык", ["Azərbaycan", "English", "Русский"])
    ui = translations[lang_choice]
    
    st.divider()
    
    # Yeni söhbət düyməsi
    if st.button(ui['new_chat'], use_container_width=True):
        # Təkrarlanmayan müvəqqəti ad veririk
        temp_name = f"Yeni Söhbət {len(st.session_state.chats) + 1}"
        st.session_state.chats[temp_name] = []
        st.session_state.current_chat = temp_name
        st.rerun()
        
    st.markdown(f"**{ui['history_title']}**")
    
    # Tarixçədəki söhbətlərin siyahısı
    chat_names = list(st.session_state.chats.keys())
    if st.session_state.current_chat not in chat_names:
        st.session_state.current_chat = chat_names[0]
        
    selected_chat = st.radio("Söhbətlər", chat_names, label_visibility="collapsed", index=chat_names.index(st.session_state.current_chat))
    
    if selected_chat != st.session_state.current_chat:
        st.session_state.current_chat = selected_chat
        st.rerun()
        
    st.divider()
    app_mode = st.radio(ui['mode_label'], ui['modes'])
    temp = st.slider(ui['temp_label'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.caption(ui['creator_info'])

# --- 8. MODERN HEADER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="modern-header">
        <div class="modern-title">KENANO</div>
        <div class="modern-copyright">© {current_year} KENAN ALIZADE. ALL RIGHTS RESERVED.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #222225; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Cari söhbətin mesajları
current_messages = st.session_state.chats[st.session_state.current_chat]

# --- 9. REJİMLƏR ---
if app_mode == ui['modes'][0]:
    # Əgər söhbət boşdursa sistem təlimatı əlavə et
    if not current_messages:
        current_messages.append({
            "role": "system", 
            "content": "Sənin adın KENANO-dur. Yaradıcın Kənan Əlizadədir. Qısa, səliqəli və sadə cavablar ver."
        })

    for message in current_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input(ui['input_placeholder']):
        current_messages.append({"role": "user", "content": prompt})
        
        # Əgər bu ilk istifadəçi mesajıdırsa, AI avtomatik Gemini kimi söhbətə mövzu adı qoyacaq:
        user_msg_count = sum(1 for m in current_messages if m["role"] == "user")
        if user_msg_count == 1:
            ai_title = generate_chat_title(prompt)
            st.session_state.chats[ai_title] = current_messages
            del st.session_state.chats[st.session_state.current_chat]
            st.session_state.current_chat = ai_title
            current_messages = st.session_state.chats[ai_title]
            st.rerun()

        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": m["role"], "content": m["content"]} for m in current_messages],
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
                
            current_messages.append({"role": "assistant", "content": full_response})

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
