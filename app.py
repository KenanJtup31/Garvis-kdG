# ==============================================================================
# LAYIHƏ ADI: KENANO AI | ENTERPRISE EDITION
# MÜƏLLİF VƏ TƏRTİBATÇI: KƏNAN ƏLİZADƏ
# TƏSVİR: Müasir iOS üslublu, çoxdilli, tarixçə və animasiya dəstəkli AI sistemi
# ==============================================================================

import streamlit as st
from groq import Groq
from datetime import datetime
import time

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO AI | PRO", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS ANIMASIYALAR VƏ İOS DİZAYN ---
st.markdown("""
    <style>
        /* Ümumi Tünd Minimalist Fon */
        .stApp {
            background-color: #000000;
            color: #f5f5f7;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
        }
        
        /* Sidebar (Yan Panel) Dizaynı */
        [data-testid="stSidebar"] {
            background-color: #0b0b0d;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        [data-testid="stSidebar"] * {
            color: #f5f5f7 !important;
        }
        
        /* Mesajların Açılma Animasiyası (Fade In & Slide Up) */
        @keyframes messageAppear {
            0% {
                opacity: 0;
                transform: translateY(12px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stChatMessage {
            background-color: #161618;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            animation: messageAppear 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            margin-bottom: 16px;
            padding: 16px;
        }
        
        /* Müasir Başlıq Bölməsi */
        .modern-header {
            text-align: center;
            padding: 20px 0 10px 0;
        }
        .modern-title {
            color: #ffffff;
            font-size: 26px;
            font-weight: 600;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }
        .modern-copyright {
            color: #86868b;
            font-size: 11px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        /* Səliqəli Input Sahəsi */
        div[data-testid="stChatInput"] input {
            background-color: #1c1c1e !important;
            color: #ffffff !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Düymə Dizaynları */
        .stButton button {
            border-radius: 12px;
            background-color: #2c2c2e;
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #3a3a3c;
            border-color: rgba(255, 255, 255, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ÇOXDİLLİ İNTERFEYS LÜĞƏTİ ---
translations = {
    "Azərbaycan": {
        "new_chat": "+ Yeni Söhbət",
        "history_title": "Son Söhbətlər",
        "mode_label": "İş Rejimi",
        "modes": ["Söhbət", "Xülasə", "Kod Analizi", "Haqqında"],
        "temp_label": "Yaradıcılıq Əmsalı",
        "input_placeholder": "Mesajınızı daxil edin...",
        "creator_info": "Bu layihə Kənan Əlizadə tərəfindən hazırlanmışdır.",
        "summary_btn": "Mətni Xülasə Et",
        "code_btn": "Kodu Təhlil Et"
    },
    "English": {
        "new_chat": "+ New Chat",
        "history_title": "Recent Chats",
        "mode_label": "Operation Mode",
        "modes": ["Chat", "Summary", "Code Analysis", "About"],
        "temp_label": "Creativity Level",
        "input_placeholder": "Type your message here...",
        "creator_info": "This project was developed by Kenan Alizade.",
        "summary_btn": "Summarize Text",
        "code_btn": "Analyze Code"
    },
    "Русский": {
        "new_chat": "+ Новый чат",
        "history_title": "Недавние чаты",
        "mode_label": "Режим работы",
        "modes": ["Чат", "Резюме", "Анализ кода", "О программе"],
        "temp_label": "Уровень творчества",
        "input_placeholder": "Введите сообщение...",
        "creator_info": "Проект разработан Кянаном Ализаде.",
        "summary_btn": "Сделать резюме",
        "code_btn": "Анализировать код"
    }
}

# --- 4. API VƏ MODEL KONFİQURASİYASI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Kritik API Bağlantı Xətası: {e}")

# Groq platformasının ən güclü və dəqiq ensiklopedik modeli
PRIMARY_MODEL = "llama-3.3-70b-versatile"

# --- 5. DİNAMİK BAŞLIQ GENERATORU (GEMİNİ / CHATGPT ÜSLUBU) ---
def generate_chat_title(first_message):
    """İlk mesaja əsasən söhbətə avtomatik qısa və mənalı ad verir."""
    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "Verilən istifadəçi mesajına əsasən 2-4 sözdən ibarət qısa, konkret və mənalı başlıq adı yaz. Heç bir dırnaq işarəsi və ya izahat əlavə etmə."},
                {"role": "user", "content": first_message}
            ],
            temperature=0.3,
            max_tokens=15
        )
        title = response.choices[0].message.content.strip().replace('"', '').replace("'", "")
        return title[:32] if title else "Yeni Söhbət"
    except Exception:
        return first_message[:20] + "..."

# --- 6. SESSİYA İDARƏETMƏSİ VƏ TARİXÇƏ ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Yeni Söhbət": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Yeni Söhbət"

# --- 7. SIDEBAR İDARƏETMƏ PANELİ ---
with st.sidebar:
    lang_choice = st.selectbox("🌐 Dil / Language / Язык", ["Azərbaycan", "English", "Русский"])
    ui = translations[lang_choice]
    
    st.divider()
    
    # Yeni Söhbət Düyməsi
    if st.button(ui['new_chat'], use_container_width=True):
        unique_name = f"Söhbət {len(st.session_state.chats) + 1}"
        st.session_state.chats[unique_name] = []
        st.session_state.current_chat = unique_name
        st.rerun()
        
    st.markdown(f"**{ui['history_title']}**")
    
    # Tarixçə Siyahısı
    chat_names = list(st.session_state.chats.keys())
    if st.session_state.current_chat not in chat_names:
        st.session_state.current_chat = chat_names[0]
        
    selected_chat = st.radio(
        "Tarixçə Naviqasiyası", 
        chat_names, 
        label_visibility="collapsed", 
        index=chat_names.index(st.session_state.current_chat)
    )
    
    if selected_chat != st.session_state.current_chat:
        st.session_state.current_chat = selected_chat
        st.rerun()
        
    st.divider()
    app_mode = st.radio(ui['mode_label'], ui['modes'])
    temp = st.slider(ui['temp_label'], 0.0, 1.0, 0.7)
    
    st.divider()
    st.caption(ui['creator_info'])

# --- 8. ANA EKRAN HEADER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="modern-header">
        <div class="modern-title">KENANO</div>
        <div class="modern-copyright">© {current_year} KENAN ALIZADE. ALL RIGHTS RESERVED.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.08); margin-bottom: 25px;'>", unsafe_allow_html=True)

# Cari aktiv söhbətin mesajları
current_messages = st.session_state.chats[st.session_state.current_chat]

# AI SİSTEM TƏLİMATI (ENSİKLOPEDİK BAZA VƏ ŞƏXSİYYƏT)
SYSTEM_INSTRUCTION = {
    "role": "system", 
    "content": (
        "Sənin adın KENANO-dur. Sənin yaradıcın və tərtibatçın Kənan Əlizadədir. "
        "Sən istənilən sahədə (tarix, elm, texnologiya, ədəbiyyat, riyaziyyat, proqramlaşdırma) "
        "dərin ensiklopedik biliklərə malik peşəkar intellektual sistemsən. "
        "Həmişə obyektiv, faktlara əsaslanan, dəqiq, səliqəli və ətraflı cavablar ver. "
        "Heç vaxt məlumatları uydurma və ya səhv təqdim etmə. Suallara dərhal, peşəkar dildə cavab ver."
    )
}

# --- 9. REJİMLƏRİN İŞLƏNMƏSİ ---

# Rejim 1: Ağıllı Söhbət (Smart Chat)
if app_mode == ui['modes'][0]:
    if not current_messages:
        current_messages.append(SYSTEM_INSTRUCTION)

    # Mövcud mesajların ekrana çapı
    for message in current_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # İstifadəçi girişi
    if prompt := st.chat_input(ui['input_placeholder']):
        current_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        # Asistan cavabı və axın (streaming) mexanizmi
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    model=PRIMARY_MODEL,
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
                message_placeholder.markdown(f"Xəta baş verdi: {e}")
                
            current_messages.append({"role": "assistant", "content": full_response})

        # İlk mesaj yazıldıqda söhbətə avtomatik peşəkar ad verilməsi
        user_msg_count = sum(1 for m in current_messages if m["role"] == "user")
        if user_msg_count == 1:
            new_title = generate_chat_title(prompt)
            st.session_state.chats[new_title] = current_messages
            del st.session_state.chats[st.session_state.current_chat]
            st.session_state.current_chat = new_title

# Rejim 2: Mətn Xülasəsi (Text Summarizer)
elif app_mode == ui['modes'][1]:
    st.subheader(ui['modes'][1])
    text_to_summarize = st.text_area("Xülasə olunacaq mətni daxil edin:", height=180)
    if st.button(ui['summary_btn'], use_container_width=True):
        if text_to_summarize:
            with st.spinner("Mətn təhlil edilir..."):
                try:
                    response = client.chat.completions.create(
                        model=PRIMARY_MODEL,
                        messages=[
                            {"role": "system", "content": "Sən peşəkar mətn analitiki və xülasəedicisisən. Verilmiş mətni əsas məqamları saxlamaqla qısa, səliqəli və strukturlaşdırılmış şəkildə xülasə et."},
                            {"role": "user", "content": f"Zəhmət olmasa bu mətni xülasə et: {text_to_summarize}"}
                        ],
                        temperature=0.3
                    )
                    st.success("Xülasə Nəticəsi:")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Xəta: {e}")
        else:
            st.warning("Zəhmət olmasa mətn daxil edin.")

# Rejim 3: Kod Analizi (Code Explainer)
elif app_mode == ui['modes'][2]:
    st.subheader(ui['modes'][2])
    code_snippet = st.text_area("Təhlil olunacaq kod parçasını daxil edin:", height=180)
    if st.button(ui['code_btn'], use_container_width=True):
        if code_snippet:
            with st.spinner("Kod öyrənilir və izah edilir..."):
                try:
                    response = client.chat.completions.create(
                        model=PRIMARY_MODEL,
                        messages=[
                            {"role": "system", "content": "Sən senior proqramlaşdırma mütəxəssisisən. Kodları addım-addım, məntiqli və səlis şəkildə izah edirsən."},
                            {"role": "user", "content": f"Bu kodu ətraflı şəkildə izah et və optimizasiya tövsiyələri ver: \n\n{code_snippet}"}
                        ],
                        temperature=0.3
                    )
                    st.success("Kodun Təhlili:")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Xəta: {e}")
        else:
            st.warning("Zəhmət olmasa kod daxil edin.")

# Rejim 4: Layihə Haqqında (About Project)
elif app_mode == ui['modes'][3]:
    st.subheader(ui['modes'][3])
    st.markdown("""
    * **Layihə Adı:** KENANO AI (Enterprise Edition)
    * **Baş Tərtibatçı:** Kənan Əlizadə
    * **İntellektual Mühərrik:** LLaMA-3.3-70B Versatile (Real-time Cloud Intelligence)
    * **Dizayn Konsepsiyası:** Apple Human Interface Guidelines (Minimalist Dark Mode & Smooth Animations)
    * **Dəstəklənən Dillər:** Azərbaycan, English, Русский
    * **Status:** Tam Aktiv, Sabit və Müstəqil Sistem
    """)
