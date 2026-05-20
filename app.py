import streamlit as st
from groq import Groq
from pypdf import PdfReader

# 1. Konfiqurasiya
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

st.set_page_config(page_title="Langur AI", page_icon="🇦🇿")
st.markdown("""
<style>
    .stApp { background: #000000; color: white; }
    .footer { text-align: center; color: #8e8e93; font-size: 14px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# 2. Kənanın məlumatları (Langurun beyninə yerləşdiririk)
kenan_info = """
Kənan Əlizadə (KDG) haqqında məlumat:
- Doğum tarixi: 7 may 2011
- Doğulduğu yer: İsmayıllı rayonu
- Əsas maraq dairələri: Süni intellekt, nanotexnologiya və yeni texnologiyalar.
"""

# 3. Yaddaş və İnterfeys
if "messages" not in st.session_state: 
    st.session_state.messages = [
        {"role": "system", "content": f"Sənin adın Langur-dur. Səni Kənan Əlizadə yaradıb. Bu məlumatları yadda saxla və soruşulanda istifadə et: {kenan_info}"}
    ]

st.title("🇦🇿 Langur AI")
st.markdown("<p style='text-align: center;'>KDG - Kənan Əlizadənin süni intellekt layihəsi</p>", unsafe_allow_html=True)

# Çat
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

if sual := st.chat_input("Langura bir şey soruş..."):
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

# 4. Footer (Developed by)
st.markdown("<div class='footer'>Developed by Kənan Əlizadə | KDG</div>", unsafe_allow_html=True)
