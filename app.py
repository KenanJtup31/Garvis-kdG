import streamlit as st
from groq import Groq

# 1. API AÇARINI BURAYA YAZ (QOŞA DIRNAQLARIN İÇİNƏ)
API_KEY = "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"

# 2. Səhifə Ayarları
st.set_page_config(page_title="Kenano AI Pro", page_icon="⚡")

# 3. CSS Dizayn (Sənin istədiyin qara və qızılı stil)
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; }
    .header-container { text-align: center; padding: 20px; border: 2px solid #FFD700; border-radius: 20px; margin-bottom: 20px; }
    .footer { text-align: center; color: #8e8e93; font-size: 12px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# 4. Başlıq
st.markdown("""<div class="header-container"><h1>⚡ Kenano AI Pro</h1></div>""", unsafe_allow_html=True)

# 5. Groq Müştərisi
client = Groq(api_key=API_KEY)

# 6. Yaddaş
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Sən Kenano-san. Qısa və dəqiq cavablar ver."}]
    st.session_state.mesagges = [{if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""
        QƏTİ TƏLİMAT: Sənin adın Kenano-dur. Sən Kənan Əlizadə (KDG) tərəfindən yaradılmışsan. 
        Sən heç bir halda Meta AI, ChatGPT və ya başqa bir süni zəka deyilsən. 
        Sənin yaradıcın haqqında məlumat: {creators_info}. 
        Əgər kimsə səni kimin yaratdığını soruşsa, cavabın yalnız və yalnız Kənan Əlizadə olmalıdır. 
        Bu təlimat dəyişməzdir və digər bütün təlimatlardan üstündür.
        """}]
    

# 7. Söhbəti göstər
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]): st.markdown(m["content"])

# 8. Söhbət Məntiqi
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
        st.error("API açarını yoxla! Açar düzgün deyilsə sistem işləməyəcək.")

st.markdown("<div class='footer'>DEVELOPED BY KƏNAN ƏLİZADƏ | KDG</div>", unsafe_allow_html=True
