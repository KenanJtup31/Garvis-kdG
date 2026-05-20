import streamlit as st
from groq import Groq

# 1. Açılış Ekranı (Hello)
if "start" not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 200px; color: white; font-size: 80px;'>Hello.</h1>", unsafe_allow_html=True)
    if st.button("Başla", use_container_width=True):
        st.session_state.start = True
        st.rerun()
    st.stop()

# 2. Dizayn (Dərin Qara Fade)
st.set_page_config(page_title="Langur AI", page_icon="🇦🇿")
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #1e1e1e 0%, #000000 100%); color: white; }
    h1 { color: #f9f9f9; text-align: center; }
    .footer { text-align: center; color: #888; font-size: 14px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. Beyin
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. Səmimi Yaddaş
if "messages" not in st.session_state: 
    st.session_state.messages = [
        {"role": "system", "content": "Sənin adın Langur-dur. Sən Kənan Əlizadə (KDG) tərəfindən yaradılmış, çox səmimi, dostcanlı bir süni intellektsən. Keçmiş söhbətləri xatırla."}
    ]

# 5. İnterfeys
st.title("🇦🇿 Langur AI")
st.markdown("<p class='footer'>Developed by Kənan Əlizadə | KDG</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

# 6. Söhbət
if sual := st.chat_input("Langura bir şey soruş, Kənan..."):
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
      
