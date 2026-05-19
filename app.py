import streamlit as st
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Langur Jarvis", page_icon="🤖")

# 2. Açar təyini
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

if "messages" not in st.session_state: 
    st.session_state.messages = []

st.title("🐒 Langur Jarvis")

# 3. Söhbət məntiqi
for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

if sual := st.chat_input("Jarvisə bir şey soruş..."):
    # Məcburi cavab funksiyası
    if "səni kim yaradıb" in sual.lower() or "kim yaradıb" in sual.lower():
        cavab = "Məni Kənan Əlizadə (KDG) yaradıb. Mən onun xüsusi süni intellekt köməkçisiyəm!"
    else:
        # Normal sual olduqda
        st.session_state.messages.append({"role": "user", "content": sual})
        with st.chat_message("user"): st.markdown(sual)
        
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Sənin yaradıcın Kənan Əlizadədir."}] + st.session_state.messages
            )
            cavab = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": cavab})
    with st.chat_message("assistant"): st.markdown(cavab)
      
