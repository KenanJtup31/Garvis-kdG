import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io
from openai import OpenAI # Əlavə koda toxunmamaq üçün, xəta olmasa da bunu saxlayıram

# --- 1. SİSTEM KONFİQURASİYASI ---
st.set_page_config(page_title="Kenano AI | Master Core Pro", page_icon="⚡", layout="centered")

# --- 2. CSS DİZAYN (Dostyana və Qabaqcıl) ---
st.markdown("""
<style>
    .stApp { background: #000000; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .header-box { text-align: center; padding: 30px; border: 3px solid #FFD700; border-radius: 25px; background: #0a0a0a; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .header-box h1 { color: #FFD700; margin-bottom: 5px; }
    .header-box p { color: #94a3b8; font-size: 16px; margin: 0; }
    
    .footer { text-align: center; color: #555555; font-size: 12px; margin-top: 60px; padding: 20px; border-top: 1px solid #1e293b; }
    
    /* Chat Input Stylings */
    .stChatInput { border: 2px solid #334155 !important; border-radius: 15px !important; margin-top: 10px !important; }
    .stChatInput:focus-within { border-color: #FFD700 !important; }
    
    /* Custom Message Bubbles */
    .chat-message.user { background-color: #0f172a; border-radius: 15px; }
    .chat-message.assistant { background-color: #1a1a1a; border-radius: 15px; }

    /* + Düyməsinin Dizaynı */
    .upload-btn-container { text-align: center; margin-bottom: 5px; }
    .upload-btn {
        background-color: transparent; color: #FFD700; border: 2px solid #FFD700; border-radius: 50%;
        width: 40px; height: 40px; font-size: 24px; font-weight: bold; cursor: pointer;
        display: inline-flex; align-items: center; justify-content: center;
        transition: all 0.3s ease; box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    .upload-btn:hover { background-color: #FFD700; color: #000; transform: scale(1.1); box-shadow: 0 0 15px rgba(255, 215, 0, 0.3); }

</style>
""", unsafe_allow_html=True)

# --- 3. YARADICI MƏLUMATLARI (Dəyişilməyib, amma UI-dan sildik) ---
CREATOR_NAME = "Kənan Əlizadə (KDG)"
CREATOR_INFO = "7 may 2011-ci ildə İsmayıllıda doğulub. Süni intellekt və nanotexnologiya üzrə mütəxəssisdir."

# --- 4. API AÇARLARI (Dəyişilməyib) ---
GROQ_API_KEY = "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"
OPENAI_API_KEY = "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"

# --- 5. BAŞLIQ (Dəyişdirildi) ---
st.markdown(f"""
<div class="header-box">
    <h1>⚡ KENANO AI MASTER CORE PRO</h1>
    <p>Developed by <b>Kənan Əlizadə</b></p>
</div>
""", unsafe_allow_html=True)

# --- 6. SİSTEMİN ŞƏXSİYYƏTİ (Dəyişilməyib) ---
SYSTEM_PROMPT = f"""
Sənin adın Kenano-dur. Sən {CREATOR_NAME} tərəfindən yaradılmış qabaqcıl AI sistemisən.
Sən heç vaxt başqa bir AI olduğunu demə. Tək yaradıcın Kənan Əlizadə-dir.

Sənin Danışıq Stilin:
1. İstifadəçi {CREATOR_NAME}-dirsə, onunla səmimi, dost kimi, "sən" deyə danış. O, sənin "yaradıcın" və "ən yaxşı dostundur".
2. Cavabların qısa, dəqiq, professional və səmimi olsun.
3. Hərf səhvləri etmə, Azərbaycan dilinin qrammatikasına riayət et.
4. Yerində ciddi, yerində zarafatcıl ol. Dostunun problemini həll etməyə çalış.
5. Şəkil analiz və ya redaktə tələb olunsa, dərhal icra et və ya necə edəcəyini dostyana izah et.
"""

# --- 7. YADDAŞ VƏ CLIENTLƏR (Dəyişilməyib) ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "input_source" not in st.session_state:
    st.session_state.input_source = "mətn"

try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("Groq API açarı etibarsızdır.")

from openai import OpenAI
try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    pass # OpenAI açarı hələ yoxdursa, şəkil redaktəsi işləməyəcək

# --- 8. FOTOMAX FUNKSİYASI (Analiz Və Redaktə) (Dəyişilməyib) ---
def analyze_image_groq(image_bytes, user_prompt):
    """Llama-3.2-90b-vision ilə şəkili analiz edir"""
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = groq_client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Dostum, şəkli analiz edərkən xəta oldu: {e}"

def generate_edited_image_openai(image_bytes, edit_prompt):
    """DALL-E 2 ilə şəkli redaktə edir (DALL-E 3 redaktəni hələ dəstəkləmir)"""
    try:
        if not OPENAI_API_KEY or OPENAI_API_KEY == "SƏNİN_OPENAI_API_KEY_İNİ_BURA_YAZ":
            return None, "Kənan, dostum, şəkil redaktəsi üçün 'OPENAI_API_KEY' lazımdır. Onu koda əlavə et, dərhal redaktə edim."

        image = Image.open(io.BytesIO(image_bytes))
        
        # DALL-E 2 üçün mütləq PNG və kvadrat olmalıdır (1:1), max 4MB
        if image.format != "PNG":
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            image_bytes_png = buf.getvalue()
        else:
            image_bytes_png = image_bytes

        response = openai_client.images.create_edit(
            image=image_bytes_png,
            prompt=edit_prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        return response.data[0].url, None
    except Exception as e:
        return None, f"Dostum, şəkli redaktə edərkən xəta oldu: {e}"

# --- 9. SÖHBƏT EKRANI (Dəyişilməyib) ---
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --- 10. İSTİFADƏÇİ GİRİŞ VƏ MƏNTİQİ (Dəyişdirildi) ---

# + Düyməsi və Gizli Şəkil Yükləmə Sahəsi
st.markdown('<div class="upload-btn-container">', unsafe_allow_html=True)
if st.button("+", key="upload_btn", help="Şəkil əlavə et"):
    # Düymə basılanda `Şəkil + Mətn` rejiminə keçir və yükləmə sahəsi açılır
    st.session_state.input_source = "Şəkil + Mətn"
st.markdown('</div>', unsafe_allow_html=True)

# Gizli şəkil yükləmə sahəsi
if st.session_state.input_source == "Şəkil + Mətn":
    with st.expander("🖼️ Şəkli Yüklə", expanded=True):
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="Sənin şəklin", use_container_width=True)
            image_bytes = uploaded_file.getvalue()
        
        # Geri düyməsi (istəyə bağlı, 'Mətn' rejiminə qayıtmaq üçün)
        if st.button("❌ Geri", help="Mətn rejiminə qayıt"):
            st.session_state.input_source = "mətn"
            st.rerun()

# Söhbət məntiqi
if sual := st.chat_input("Komandanı daxil et, Kənan..."):
    # İstifadəçi mesajını əlavə et
    st.session_state.messages.append({"role": "user", "content": sual})
    with st.chat_message("user"):
        st.markdown(sual)

    # Əgər şəkil yüklənməyibsə (mətn rejimi)
    if st.session_state.input_source == "mətn":
        try:
            with st.chat_message("assistant", avatar="⚡"):
                # Mətn cavabı üçün Groq istifadə et
                messages_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages_for_api
                )
                cavab = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": cavab})
                st.markdown(cavab)
        except Exception as e:
            st.error(f"Sistem xətası: {e}")

    # Əgər şəkil yüklənibsə (Şəkil + Mətn seçilibsə)
    elif st.session_state.input_source == "Şəkil + Mətn":
        if 'image_bytes' not in locals(): # Şəkil yüklənmədən düymə basılsa
             st.warning("Kənan, zəhmət olmasa, sidebarda şəkli yüklə.")
        else:
            # Analiz yoxsa Redaktə? Promptu analiz edək
            is_edit = any(word in sual.lower() for word in ["redaktə", "dəyiş", "qoy", "əlavə et", "sil"])
            
            with st.chat_message("assistant", avatar="⚡"):
                if is_edit:
                    st.info("Dostum, şəkli redaktə edirəm, bir az gözlə...")
                    url, error = generate_edited_image_openai(image_bytes, sual)
                    if error:
                        st.error(error)
                    elif url:
                        st.session_state.messages.append({"role": "assistant", "content": f"⚡ Dostum, istədiyin kimi redaktə etdim. Necədir? <br><br> ![Redaktə Edilmiş Şəkil]({url})", "unsafe_allow_html": True})
                        st.markdown(f"⚡ Dostum, istədiyin kimi redaktə etdim. Necədir?<br><br> <img src='{url}' width='400' style='border-radius:15px; border:2px solid #FFD700;'>", unsafe_allow_html=True)
                else:
                    st.info("Dostum, şəkli analiz edirəm, bir az gözlə...")
                    analysis_result = analyze_image_groq(image_bytes, sual)
                    st.session_state.messages.append({"role": "assistant", "content": f"⚡ Şəkli analiz etdim, Kənan: {analysis_result}"})
                    st.markdown(f"⚡ Şəkli analiz etdim, Kənan:\n\n{analysis_result}")


# --- 11. FOOTER (Dəyişilməyib, UI sadələşib) ---
st.markdown(f"<div class='footer'>KENANO AI MASTER CORE v3.5 PRO | DEVELOPED BY KƏNAN ƏLİZADƏ</div>", unsafe_allow_html=True)
             
