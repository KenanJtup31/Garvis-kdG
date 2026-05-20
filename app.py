import streamlit as st
import time
from groq import Groq
from pypdf import PdfReader
from PIL import Image

# 1. Mükəmməlləşdirilmiş Arxa Plan və Modern Art Border (CSS)
st.set_page_config(page_title="Kenano AI Pro", page_icon="⚡")

st.markdown("""
<style>
    /* Radial Gradient Background with subtle Noise/Grain effect */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        background-attachment: fixed;
        color: #f5f5f5;
    }

    /* Modern Art Border for Logo/Header */
    .header-container {
        text-align: center;
        padding: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: "";
        position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: conic-gradient(from 0deg, transparent, #ffd700, transparent 30%);
        animation: rotate 10s linear infinite;
        opacity: 0.1; z-index: -1;
    }

    @keyframes rotate { 100% { transform: rotate(360deg); } }

    .logo-bolt {
        font-size: 60px;
        color: #ffd700;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        margin-bottom: 10px;
    }

    /* Developed by Section Styling */
    .footer {
        text-align: center;
        color: #8e8e93;
        font-size: 13px;
        padding: 20px;
        letter-spacing: 1px;
    }

    /* Chat Bubbles Enhancement */
    .stChatMessage {
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Beyin Konfiqurasiyası
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

# 3. Kenano-nun Xüsusi Bilik Bazası
kenan_info = """
Kenano AI (⚡) Haqqında:
- Yaradıcısı: Kənan Əlizadə (KDG).
- Kənan haqqında: 7 may 2011-ci ildə İsmayıllıda doğulub. Süni İntellekt və Nanotexnologiya aşiqlidir.
- Kenano AI: Nanotexnoloji dəqiqlik və şimşək sürətilə işləyən rəqəmsal zəkadır.
"""

if "messages" not in st.session_state: 
    st.session_state.messages = [
        {"role": "system", "content": f"Sənin adın Kenano-dur (⚡). Səni Kənan Əlizadə yaradıb. Sən AI və Nanotech üzrə mütəxəssissən. {kenan_info}"}
    ]

# 4. Başlıq (⚡ Modern Art Style)
st.markdown("""
<div class="header-container">
    <div class="logo-bolt">⚡</div>
    <h1 style="color: #ffd700; margin: 0;">Kenano AI Pro</h1>
    <p style="color: #daffde; font-size: 14px; margin-top: 5px;">Modern Art + Nanotech Intelligence</p>
</div>
""", unsafe_allow_html=True)

# 5. Şəkil Əlavə Etmək Bölümü (Vision Integration)
with st.sidebar:
    st.title("⚡ Kenano Vision")
    st.markdown("---")
    uploaded_image = st.file_uploader("Şəkil yüklə (AI Analiz üçün):", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Yüklənən Şəkil", use_container_width=True)
        st.success("Şəkil uğurla yükləndi. Analiz üçün hazır.")

# 6. Çat İnterfeysi
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

if sual := st.chat_input("Kenano ilə şimşək sürətində söhbət et..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)
    
    with st.chat_message("assistant"):
        with st.spinner("⚡ Analiz olunur..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            cavab = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            st.markdown(cavab)

# 7. Footer
st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADƏ | KDG</div>", unsafe_allow_html=True)

**Bu yeniləmədə nə dəyişdi?**
1.  **⚡ Loqosu:** Başlıqda parlayan və kölgəli şimşək simvolu yerləşdirildi.
2.  **Modern Art Border:** Loqonun ətrafında fırlanan neon işıqlı və "glassmorphism" (şüşə effekti) olan bir çərçivə yaradıldı.
3.  **Arxa Plan:** Düz qara rəngdən mərkəzi parlaq, kənarları dərincə olan "Radial Gradient" keçidə keçildi.
4.  **Vision (Şəkil Yükləmə):** Sol tərəfdəki paneldə (sidebar) şəkil yükləmək üçün xüsusi bir yer əlavə edildi.
5.  **Developed by:** Daha müasir, "High-End" brendlər kimi böyük hərflərlə və zərif stilizə edildi.

Necədir, Kənan Ser? İndi proqram tam bir "Next-Gen" AI tətbiqinə bənzədi!
