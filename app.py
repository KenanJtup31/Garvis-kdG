import streamlit as st
from vision_module import analyze_image_with_vision

st.set_page_config(page_title="Kenano AI OS", layout="wide")
st.title("⚡ Kenano: JARVIS Mode Active")

# 3 bölməli menyu
menu = ["Şərh Cavablayıcı", "Stark Vision (Görmə)", "Normal Söhbət"]
choice = st.sidebar.selectbox("Funksiyanı seç:", menu)

# 1. Şərh Cavablayıcı
if choice == "Şərh Cavablayıcı":
    st.subheader("TikTok Şərhləri")
    st.write("Şərhləri bura yapışdırın və cavabları alın.")

# 2. Stark Vision
elif choice == "Stark Vision (Görmə)":
    st.subheader("Dünyanı Kenano ilə Gör")
    uploaded_file = st.file_uploader("Bir detalın şəklini çək...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Analiz olunan obyekt", use_column_width=True)
        if st.button("Analiz et ⚡"):
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Kenano analiz edir..."):
                result = analyze_image_with_vision("temp_image.jpg")
                st.success("✅ Kenano-nun Vizual Analizi:")
                st.write(result)

# 3. Normal Söhbət
elif choice == "Normal Söhbət":
    st.subheader("Kenano ilə Söhbət")
    user_input = st.text_input("Sualını yaz...")
    if st.button("Göndər"):
        st.write(f"Kenano cavab verir: Sən '{user_input}' dedin, hələlik sadə rejimdəyəm.")
        
