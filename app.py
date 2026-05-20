import streamlit as st
from groq import Groq

# 1. Konfiqurasiya və Təhlükəsiz API Yoxlaması
st.set_page_config(page_title="Kenano AI Pro", page_icon="⚡")

# Streamlit-in "Secrets" bölməsindən oxumağa çalışır, yoxdursa boş saxlayır
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = None # Əgər burada boşdursa, aşağıda istifadəçidən istəyəcəyik

# 2. CSS Dizayn
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%); color: #f5f5f5; }
    .header-container { text-align: center; padding: 20px; border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 30px; background: rgba(255, 255, 255, 0.03); }
    .footer { text-align: center; color: #8e8e93; font-size: 13px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. İnterfeys
st.markdown("""<div class="header-container"><h1>⚡ Kenano AI Pro</h1></div>""", unsafe_allow_html=True)

# API açarı yoxdursa, istifadəçidən istə
if not api_key:
    api_key = st.sidebar.text_input("Groq API Açarını Daxil Et:", type="password")

if api_key:
    client = Groq(api_key=api_key)
    kenan_info = "Kenano AI yaradıcısı Kənan Əlizadədir (KDG). Kənan 7 may 2011-də İsmayıllıda doğulub, süni intellekt və nanotexnologiya ilə maraqlanır."

    if "messages" not in st.session_state: 
        st.session_state.messages = [{"role": "system", "content": f"Sənin adın Kenano-dur. Sən AI və Nanotech üzrə mütəxəssissən. {kenan_info}"}]

    # 4. Çat Məntiqi
    for m in st.session_state.messages:
        if m["role"] != "system":
            with st.chat_message(m["role"]): st.markdown(m["content"])

    if sual := st.chat_input("Kenano ilə söhbət et..."):
        st.session_state.messages.append({"role": "user", "content": sual})
        with st.chat_message("user"): st.markdown(sual)
        
        try:
            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                cavab = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": cavab})
                st.markdown(cavab)
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}")
else:
    st.warning("⚠️ Zəhmət olmasa yan paneldən API açarınızı daxil edin.")

st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADƏ | KDG</div>", unsafe_allow_html=True)
                
