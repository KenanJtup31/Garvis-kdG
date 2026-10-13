# ==============================================================================
# LAYIHƏ ADI: KENANO AI | ENTERPRISE EDITION
# MÜƏLLİF VƏ TƏRTİBATÇI: KƏNAN ƏLİZADƏ
# ==============================================================================

import streamlit as st
from groq import Groq
from datetime import datetime
import urllib.parse
import base64

# --- 1. SİSTEM VƏ SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="KENANO AI", 
    page_icon="Logo.png", 
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
        
        /* Mesajların Açılma Animasiyası */
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
            font-size: 24px;
            font-weight: 500;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        .modern-copyright {
            color: #6e6e73;
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
        "modes": ["Söhbət", "Xülasə", "Kod Analizi", "Şəkil Yaratma", "Haqqında"],
        "temp_label": "Yaradıcılıq Əmsalı",
        "input_placeholder": "Mesajınızı daxil edin...",
        "creator_info": "Bu layihə Kənan Əlizadə tərəfindən hazırlanmışdır.",
        "summary_btn": "Mətni Xülasə Et",
        "code_btn": "Kodu Təhlil Et",
        "img_btn": "🎨 Şəkil Yarat"
    },
    "English": {
        "new_chat": "+ New Chat",
        "history_title": "Recent Chats",
        "mode_label": "Operation Mode",
        "modes": ["Chat", "Summary", "Code Analysis", "Image Generation", "About"],
        "temp_label": "Creativity Level",
        "input_placeholder": "Type your message here...",
        "creator_info": "This project was developed by Kenan Alizade.",
        "summary_btn": "Summarize Text",
        "code_btn": "Analyze Code",
        "img_btn": "🎨 Generate Image"
    },
    "Русский": {
        "new_chat": "+ Новый чат",
        "history_title": "Недавние чаты",
        "mode_label": "Режим работы",
        "modes": ["Чат", "Резюме", "Анализ кода", "Генерация изображений", "О программе"],
        "temp_label": "Уровень творчества",
        "input_placeholder": "Введите сообщение...",
        "creator_info": "Проект разработан Кянаном Ализаде.",
        "summary_btn": "Сделать резюме",
        "code_btn": "Анализировать код",
        "img_btn": "🎨 Создать изображение"
    }
}

# --- 4. API VƏ MODEL KONFİQURASİYASI ---
GROQ_API_KEY = "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"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Kritik API Bağlantı Xətası: {e}")

PRIMARY_MODEL = "openai/gpt-oss-20b"
VISION_MODEL = "llama-3.2-11b-vision-preview"

# --- 5. DİNAMİK BAŞLIQ GENERATORU ---
def generate_chat_title(first_message):
    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": "Verilən mesaja əsasən 2-4 sözdən ibarət qısa başlıq yaz. Başqa heç nə yazma."},
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
    
    if st.button(ui['new_chat'], use_container_width=True):
        unique_name = f"Söhbət {len(st.session_state.chats) + 1}"
        st.session_state.chats[unique_name] = []
        st.session_state.current_chat = unique_name
        st.rerun()
        
    st.markdown(f"**{ui['history_title']}**")
    
    chat_names = list(st.session_state.chats.keys())
    if st.session_state.current_chat not in chat_names:
        st.session_state.current_chat = chat_names[0]
        
    current_index = chat_names.index(st.session_state.current_chat) if st.session_state.current_chat in chat_names else 0
    
    selected_chat = st.radio(
        "Tarixçə Naviqasiyası", 
        chat_names, 
        label_visibility="collapsed", 
        index=current_index
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

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

current_messages = st.session_state.chats[st.session_state.current_chat]

SYSTEM_INSTRUCTION = {
    "role": "system", 
    "content": (
        "Sənin adın KENANO-dur. Sənin yaradıcın Kənan Əlizadədir. "
        "Sən yüksək biliklərə sahib, dəqiq və peşəkar intellektual sistemsən. "
        "Həmişə obyektiv, dəqiq və ətraflı cavablar ver."
    )
}

# --- 9. REJİMLƏR ---
if app_mode == ui['modes'][0]:  # Söhbət Rejimi
    if not current_messages:
        current_messages.append(SYSTEM_INSTRUCTION)

    # Əvvəlki mesajları göstər
    for message in current_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Mesaj qutusunun dərhal üstünə yerləşdirilən səliqəli Kamera/Qalereya fayl yükləyicisi
    uploaded_file = st.file_uploader("📷 Kamera / Qalereyadan şəkil əlavə et", type=["png", "jpg", "jpeg", "webp"], key="chat_uploader")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Əlavə edilmiş Şəkil", width=250)

    if prompt := st.chat_input(ui['input_placeholder']):
        with st.chat_message("user"): 
            st.markdown(prompt)

        # Əgər şəkil yüklənilibsə, Vision modelindən istifadə et
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            
            vision_messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            current_messages.append({"role": "user", "content": f"[Şəkil Yükləndi]: {prompt}"})
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    response = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=vision_messages,
                        temperature=temp
                    )
                    full_response = response.choices[0].message.content
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"Şəkil analizi xətası: {e}"
                    message_placeholder.markdown(full_response)
                    
                current_messages.append({"role": "assistant", "content": full_response})
        else:
            # Sırf mətn əsaslı sorğu
            current_messages.append({"role": "user", "content": prompt})
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

        user_msg_count = sum(1 for m in current_messages if m["role"] == "user")
        if user_msg_count == 1:
            new_title = generate_chat_title(prompt)
            if new_title in st.session_state.chats:
                new_title = f"{new_title} ({len(st.session_state.chats)})"
            st.session_state.chats[new_title] = current_messages
            del st.session_state.chats[st.session_state.current_chat]
            st.session_state.current_chat = new_title
            st.rerun()

elif app_mode == ui['modes'][1]:  # Xülasə
    st.subheader(ui['modes'][1])
    text_to_summarize = st.text_area("Xülasə olunacaq mətni daxil edin:", height=180)
    if st.button(ui['summary_btn'], use_container_width=True):
        if text_to_summarize:
            with st.spinner("İşlənir..."):
                response = client.chat.completions.create(
                    model=PRIMARY_MODEL,
                    messages=[
                        {"role": "system", "content": "Sən mətn xülasəedicisisən."},
                        {"role": "user", "content": f"Bu mətni qısa xülasə et: {text_to_summarize}"}
                    ],
                    temperature=0.3
                )
                st.success("Nəticə:")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Mətn daxil edin.")

elif app_mode == ui['modes'][2]:  # Kod Analizi
    st.subheader(ui['modes'][2])
    code_snippet = st.text_area("Kod parçasını daxil edin:", height=180)
    if st.button(ui['code_btn'], use_container_width=True):
        if code_snippet:
            with st.spinner("Təhlil edilir..."):
                response = client.chat.completions.create(
                    model=PRIMARY_MODEL,
                    messages=[
                        {"role": "system", "content": "Sən proqramlaşdırma mütəxəssisiyəm."},
                        {"role": "user", "content": f"Bu kodu izah et: \n\n{code_snippet}"}
                    ],
                    temperature=0.3
                )
                st.success("İzah:")
                st.markdown(response.choices[0].message.content)
        else:
            st.warning("Kod daxil edin.")

elif app_mode == ui['modes'][3]:  # 🎨 Şəkil Yaratma Rejimi
    st.subheader("🎨 KENANO AI — Şəkil Yaratma Mühərriki")
    img_prompt = st.text_area("Yaratmaq istədiyiniz şəklin təsvirini daxil edin (Prompt):", height=120, placeholder="Məsələn: Neon işıqlı gələcək şəhər, 8k resolution, photorealistic...")
    
    if st.button(ui['img_btn'], use_container_width=True):
        if img_prompt:
            with st.spinner("Şəkil yaradılır... Lütfən gözləyin..."):
                try:
                    encoded_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
                    st.image(image_url, caption=f"İstək: {img_prompt}", use_column_width=True)
                    st.success("Şəkil uğurla yaradıldı!")
                except Exception as e:
                    st.error(f"Şəkil yaradılarkən xəta baş verdi: {e}")
        else:
            st.warning("Zəhmət olmasa təsvir daxil edin.")

elif app_mode == ui['modes'][4]:  # Haqqında
    st.subheader(ui['modes'][4])
    st.markdown("""
    * **Layihə Adı:** KENANO AI
    * **Tərtibatçı:** Kənan Əlizadə
    * **Mühərrik:** OpenAI/GPT-OSS Model & Llama 3.2 Vision
    * **Status:** Stabil və Aktiv
    """)
                    
