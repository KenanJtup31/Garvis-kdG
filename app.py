import streamlit as st

st.set_page_config(page_title="Kenano AI", layout="wide")
st.title("⚡ Kenano: Command Center")

# 3 sadə bölmə
menu = ["Şərh Cavablayıcı", "Normal Söhbət", "Ayarlar"]
choice = st.sidebar.selectbox("Funksiyanı seç:", menu)

if choice == "Şərh Cavablayıcı":
    st.subheader("TikTok Şərhləri")
    st.write("Şərhləri bura yapışdır və cavabları al.")
    user_input = st.text_area("Şərhi bura yaz:")
    if st.button("Cavab yarat"):
        st.write("Kenano: Şərhə uyğun cavab hazırlanır...")

elif choice == "Normal Söhbət":
    st.subheader("Kenano ilə Söhbət")
    chat_input = st.text_input("Sualını yaz...")
    if st.button("Göndər"):
        st.write(f"Kenano: '{chat_input}' sualını qəbul etdim.")

elif choice == "Ayarlar":
    st.subheader("Sistem Ayarları")
    st.write("Burada sadə konfiqurasiyalar olacaq.")
    
