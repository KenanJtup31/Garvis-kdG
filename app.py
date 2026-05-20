import streamlit as st
from groq import Groq

# 1. Konfiqurasiya
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

st.set_page_config(page_title="Kenano AI", page_icon="🇦🇿")
st.markdown("""
<style>
    .stApp { background: #000000; color: white; }
    .footer { text-align: center; color: #8e8e93; font-size: 14px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# 2. Məlumat bazası (Kenano-nun xarakteri)
kenan_info = """
Kenano AI haqqında:
- Yaradıcısı: Kənan Əlizadə (KDG)
- Doğum: 7 may 2011, İsmayıllı
- Maraqlar: Süni intellekt və Nanotexnologiya sahələrində innovasiyalar.
"""

if "messages" not in st.session_state: 
    st.session_state.messages = [
        {"role": "system", "content": f"Sənin adın Kenano-dur. Səni Kənan Əlizadə (KDG) yaradıb. Sən süni intellekt və nanotexnologiya üzrə ekspert, dostcanlı bir köməkçisən. Məlumatlar: {kenan_info}"}
    ]

# 3. İnterfeys
st.title("🇦🇿 Kenano AI")
st.markdown("<p style='text-align: center;'>KDG - Kənan Əlizadənin süni intellekt layihəsi</p>", unsafe_allow_html=True)

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

# 4. Footer
st.markdown("<div class='footer'>Developed by Kənan Əlizadə | KDG</div>", unsafe_allow_html=True)
