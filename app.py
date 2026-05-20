import streamlit as st
from groq import Groq
from pypdf import PdfReader
from PIL import Image

# 1. Konfiqurasiya
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

st.set_page_config(page_title="Kenano AI Pro", page_icon="⚡")

# 2. CSS Dizayn
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%); color: #f5f5f5; }
    .header-container {
        text-align: center; padding: 20px; border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 30px; background: rgba(255, 255, 255, 0.03);
    }
    .footer { text-align: center; color: #8e8e93; font-size: 13px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. Məlumat Bazası
kenan_info = "Kenano AI yaradıcısı Kənan Əlizadədir (KDG). Kənan 7 may 2011-də İsmayıllıda doğulub, süni intellekt və nanotexnologiya ilə maraqlanır."

if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": f"Sənin adın Kenano-dur. Sən AI və Nanotech üzrə mütəxəssissən. {kenan_info}"}]

# 4. İnterfeys
st.markdown("""<div class="header-container"><h1>⚡ Kenano AI Pro</h1></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚡ Kenano Vision")
    uploaded_image = st.file_uploader("Şəkil yüklə:", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, use_container_width=True)
        st.success("Şəkil yükləndi.")

# 5. Çat Məntiqi
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

if sual := st.chat_input("Kenano ilə söhbət et..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        cavab = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": cavab})
        st.markdown(cavab)

st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADƏ | KDG</div>", unsafe_allow_html=True)
