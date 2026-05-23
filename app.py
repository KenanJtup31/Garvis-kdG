import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
from openai import OpenAI

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 30px; border: 3px solid #FFD700; border-radius: 25px; background: #0a0a0a; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .header-box h1 { color: #FFD700; margin-bottom: 5px; }
    .header-box p { color: #94a3b8; font-size: 16px; margin: 0; }
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 60px; padding: 20px; border-top: 1px solid #1e293b; }
    .stChatInput { border: 2px solid #334155 !important; border-radius: 15px !important; margin-top: 10px !important; }
    .stChatInput:focus-within { border-color: #FFD700 !important; }
    .upload-btn-container { text-align: center; margin-bottom: 5px; }
    .upload-btn { background-color: transparent; color: #FFD700; border: 2px solid #FFD700; border-radius: 50%; width: 40px; height: 40px; font-size: 24px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# --- 3. YARADICI MƏLUMATLARI ---
CREATOR_NAME = "Kənan Əlizadə (KDG)"

# --- 4. API AÇARLARI ---
GROQ_API_KEY = "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"
OPENAI_API_KEY = "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"

# --- 5. BAŞLIQ ---
st.markdown(f"""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE PRO</h1>
    <p>Developed by <b>Kənan Əlizadə</b></p>
</div>
""", unsafe_allow_html=True)

# --- 6. SİSTEMİN ŞƏXSİYYƏTİ ---
SYSTEM_PROMPT = "Sənin adın Kenano-dur. Kənan Əlizadə tərəfindən yaradılmısan. Onunla dost kimi danış. Hərf səhvi etmə. Yerində ciddi, yerində səmimi ol."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "input_source" not in st.session_state:
    st.session_state.input_source = "mətn"

groq_client = Groq(api_key=GROQ_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- 7. FOTOMAX FUNKSİYASI (MODEL YENİLƏNİB) ---
def analyze_image_groq(image_bytes, user_prompt):
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", # YENİ MODEL
            messages=[{"role": "user", "content": [{"type": "text", "text": user_prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Dostum, şəkli analiz edərkən xəta oldu: {e}"

def generate_edited_image_openai(image_bytes, edit_prompt):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.format != "PNG":
            buf = io.BytesIO(); image.save(buf, format="PNG"); image_bytes_png = buf.getvalue()
        else: image_bytes_png = image_bytes
        response = openai_client.images.create_edit(image=image_bytes_png, prompt=edit_prompt, n=1, size="1024x1024", response_format="url")
        return response.data[0].url, None
    except Exception as e:
        return None, f"Dostum, şəkli redaktə edərkən xəta oldu: {e}"

# --- 8. SÖHBƏT EKRANI ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 9. GİRİŞ VƏ MƏNTİQ ---
st.markdown('<div class="upload-btn-container">', unsafe_allow_html=True)
if st.button("+", key="upload_btn"): st.session_state.input_source = "Şəkil + Mətn"
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.input_source == "Şəkil + Mətn":
    with st.expander("🖼️ Şəkli Yüklə", expanded=True):
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
            st.image(uploaded_file, use_container_width=True)
        if st.button("❌ Geri"): st.session_state.input_source = "mətn"; st.rerun()

if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"): st.markdown(sual)
    
    with st.chat_message("assistant", avatar="⚡"):
        if st.session_state.input_source == "Şəkil + Mətn" and 'image_bytes' in locals():
            if any(word in sual.lower() for word in ["redaktə", "dəyiş", "qoy", "əlavə et", "sil"]):
                url, error = generate_edited_image_openai(image_bytes, sual)
                st.markdown(f"![Redaktə]({url})" if url else error)
            else:
                st.markdown(analyze_image_groq(image_bytes, sual))
        else:
            response = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
            st.markdown(response.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

st.markdown(f"<div class='footer'>KENANO AI MASTER CORE | DEVELOPED BY KƏNAN ƏLİZADƏ</div>", unsafe_allow_html=True)

