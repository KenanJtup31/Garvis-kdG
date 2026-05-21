import streamlit as st
from groq import Groq

# 1. Konfiqurasiya
st.set_page_config(page_title="Kenano AI | Master Core", layout="centered")

# 2. CSS - Daha yaxşı dizayn
st.markdown("""
<style>
    .stApp { background: #000; color: #fff; }
    .header-box { text-align: center; padding: 25px; border: 2px solid #FFD700; border-radius: 20px; background: #0a0a0a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. Başlıq
st.markdown("""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE</h1>
    <p>Developed by <b>Kənan Əlizadə (KDG)</b></p>
</div>
""", unsafe_allow_html=True)

# 4. Groq Client (API açarınla)
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Söhbət Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Yazı yeri (Aşağıda)
if prompt := st.chat_input("Komandanı daxil et, Kənan..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AĞILLI MƏNTİQ
    low_prompt = prompt.lower()
    
    # Sosial cavablar (Xəta verməsin deyə)
    if any(x in low_prompt for x in ["salam", "necəsən", "kimdir", "yaradıb"]):
        if "salam" in low_prompt: cavab = "Salam, Kənan! Necəsən? Sənə necə kömək edə bilərəm?"
        elif "necəsən" in low_prompt: cavab = "Əladayam, Kənan! Yeni komandalarını gözləyirəm."
        else: cavab = "Mən Kənan Əlizadə tərəfindən yaradılmış Master Core-am. Sənin şəxsi köməkçinəm."
    else:
        # Groq ilə geniş məlumat alırıq
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            cavab = chat_completion.choices[0].message.content
        except Exception as e:
            cavab = "Kenano: Üzr istəyirəm, bu mövzuda məlumatı emal edə bilmədim."

    with st.chat_message("assistant"):
        st.markdown(cavab)
    st.session_state.messages.append({"role": "assistant", "content": cavab})
    
