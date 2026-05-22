import streamlit as st
from groq import Groq

# API
client = Groq(api_key="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")

st.set_page_config(page_title="AutoFix Pro AI", layout="centered")

# Developed by Kenan Elizade - Üst hissədə
st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>Developed by Kenan Elizade</p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>🛠️ AvtoFix Pro Mühəndis</h1>", unsafe_allow_html=True)

# Modellər
models = ["Mercedes-Benz", "BMW", "Lada 2107", "Lada 2106", "Toyota", "Audi"]
if "model" not in st.session_state: st.session_state.model = None

if st.session_state.model is None:
    st.session_state.model = st.selectbox("Maşın modelini seçin:", models)
    if st.button("Başla"): st.rerun()
else:
    st.write(f"### Seçilib: {st.session_state.model}")
    if st.button("⬅️ Geri"):
        st.session_state.model = None
        st.rerun()

    if prompt := st.chat_input(f"{st.session_state.model} üçün probleminizi yazın:"):
        with st.chat_message("assistant"):
            with st.spinner("Mühəndislik təlimatları hazırlanır..."):
                system_prompt = f"""
                Sən {st.session_state.model} üzrə peşəkar mühəndis və ustasan.
                İstifadəçiyə cavab verərkən:
                1. Yalnız peşəkar avto-terminlərdən istifadə et (şam, karbürator, porşen, distribyutor, tork açarı).
                2. 'Quyu', 'lövhə', 'göbələk' kimi qeyri-texniki sözlərdən istifadə etmə.
                3. Problemi addım-addım, texniki detallarla (hissə adları ilə) izah et.
                """
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                
                st.markdown(response.choices[0].message.content)
                
                # Vizual dəstək
                st.info("🔍 Texniki diaqramlar üçün:")
                search_url = f"https://www.google.com/search?q={st.session_state.model}+{prompt}+technical+diagram&tbm=isch"
                st.markdown(f"[🛠️ Diaqramları görmək üçün bura klikləyin]({search_url})")
                st.image(f"https://source.unsplash.com/featured/?{st.session_state.model},car,engine,repair", caption="Texniki illüstrasiya")
                
