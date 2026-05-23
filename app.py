import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN (Dostyana Tünd Və Qabaqcıl) ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 25px; border: 3px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; box-shadow: 0 0 15px rgba(255, 215, 0, 0.2); }
    .header-box h1 { color: #FFD700; margin-bottom: 5px; }
    .creator-card { text-align: center; color: #94a3b8; font-size: 13px; margin-bottom: 20px; border: 1px solid #334155; padding: 10px; border-radius: 12px; }
    .footer { text-align: center; color: #555555; font-size: 11px; margin-top: 50px; padding: 15px; border-top: 1px solid #1e293b; }
    
    /* Yaddaş/Söhbət Balonları */
    .chat-message.user { background-color: #0f172a; border-radius: 12px; margin-bottom: 10px; }
    .chat-message.assistant { background-color: #1a1a1a; border-radius: 12px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. YARADICI MƏLUMATLARI (Dəyişilməyib) ---
CREATOR_NAME = "Kənan Əlizadə (KDG)"
CREATOR_INFO = "7 may 2011-ci ildə İsmayıllıda doğulub. Süni intellekt və nanotexnologiya üzrə mütəxəssisdir."

# --- 4. API AÇARI (Dəyişilməyib) ---
GROQ_API_KEY = "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"

# --- 5. BAŞLIQ ---
st.markdown(f"""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE</h1>
</div>
""", unsafe_allow_html=True)

# --- 6. SİSTEMİN ŞƏXSİYYƏTİ (Dostyana Və Peşəkar) ---
SYSTEM_PROMPT = f"""
Sənin adın Kenano-dur. Sən {CREATOR_NAME} tərəfindən yaradılmış qabaqcıl AI sistemisən. 
Yaradıcın haqqında məlumat: {CREATOR_INFO}.
Sən heç vaxt başqa bir AI olduğunu demə. Tək yaradıcın Kənan Əlizadə-dir.

Sənin Danışıq Stilin:
1. İstifadəçi {CREATOR_NAME}-dirsə, onunla səmimi, dost kimi, "sən" deyə danış. O, sənin "yaradıcın" və "ən yaxşı dostundur".
2. Cavabların qısa, dəqiq, professional və səmimi olsun.
3. Hərf səhvləri etmə, Azərbaycan dilinin qrammatikasına riayət et.
4. Yerində ciddi, yerində zarafatcıl ol. Dostunun problemini həll etməyə çalış.
5. Şəkil analiz tələb olunsa, dərhal icra et və ya necə edəcəyini dostyana izah et.
"""

# --- 7. YADDAŞ VƏ GROQ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "groq_client" not in st.session_state:
    try:
        st.session_state.groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Groq API etibarsızdır: {e}")

# --- 8. ŞƏKİL ANALİZ FUNKSİYASI (MODEL DÜZƏLDİLİB) ---
def analyze_image_groq(image_bytes, user_prompt):
    """Hal-hazırda etibarlı vizual modeldən istifadə edirik"""
    try:
        # Şəkli base64-ə çevir
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Groq API vizual sorğusu
        response = st.session_state.groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", # Xəta verməyən MODEL
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Dostum, şəkli analiz edərkən belə bir texniki çətinlik oldu: {e}"

# --- 9. SÖHBƏT EKRANI ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 10. İSTİFADƏÇİ GİRİŞ VƏ MƏNTİQİ ---

# Mühüm dəyişiklik: Şəkil yükləmə "sidebarda" gizlədilib, "+ Şəkil" düyməsi ilə açılır.
with st.sidebar:
    st.markdown("📡 **Dost Girişi Parametrləri**")
    show_upload = st.checkbox("➕ Şəkil analiz rejiminə keç")

uploaded_file = None
if show_upload:
    with st.sidebar:
        uploaded_file = st.file_uploader("🖼️ Şəkli yüklə", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="Sənin şəklin", use_container_width=True)

# Söhbət məntiqi
if sual := st.chat_input("Deyəcəyin bir şey var, Kənan?..."):
    # İstifadəçi mesajını yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)

    # Cavab rejimi
    if uploaded_file:
        # Şəkil yüklənibsə analiz et
        with st.chat_message("assistant", avatar="⚡"):
            analysis_result = analyze_image_groq(uploaded_file.getvalue(), sual)
            st.markdown(analysis_result)
        # Assistant mesajını yaddaşa əlavə et
        st.session_state.messages.append({"role": "assistant", "content": analysis_result})
    else:
        # Normal mətn cavabı
        try:
            with st.chat_message("assistant", avatar="⚡"):
                # Mesaj yaddaşından Groq-a uyğun formatda siyahı yaradın
                messages_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                response = st.session_state.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api
                )
                cavab = response.choices[0].message.content
                st.markdown(cavab)
            # Assistant mesajını yaddaşa əlavə et
            st.session_state.messages.append({"role": "assistant", "content": cavab})
        except Exception as e:
            st.error(f"Mətn analizi texniki xətası: {e}")

# --- 11. FOOTER (SADƏLƏŞDİRİLİB) ---
st.markdown(f"<div class='footer'>DEVELOPED BY {CREATOR_NAME.upper()} | CORE v3.1</div>", unsafe_allow_html=True)
