import streamlit as st

# Kenano'nun cavab hazırlayan funksiyası
def generate_response(comment, is_negative):
    if is_negative:
        return "Salam, fikriniz üçün təşəkkürlər. Lakin nanotexnologiya və AI sahəsində elmi faktlar başqa istiqamətdədir. Gəlin bu mövzunu daha ətraflı müzakirə edək."
    return "Şərhiniz üçün çox sağ olun! Kenano AI layihəmiz haqqında düşüncələriniz mənim üçün dəyərlidir."

# Admin Panel
st.title("⚡ Kenano Command Center")

# Şərhlər siyahısı (buraya TikTok-dan gələn şərhlər düşəcək)
comments = [
    {"user": "Ali", "text": "Bu proqram səhvdir, işləmir.", "negative": True},
    {"user": "Veli", "text": "Əla layihədir, davam et!", "negative": False}
]

for item in comments:
    st.write(f"**{item['user']}:** {item['text']}")
    
    # Kenano'nun təklif etdiyi cavab
    suggested = generate_response(item['text'], item['negative'])
    
    # Sən cavabı redaktə edə bilərsən
    edited_response = st.text_area(f"Kenano'nun cavabı:", suggested, key=item['user'])
    
    if st.button(f"🚀 {item['user']} üçün cavabı göndər"):
        st.success(f"Cavab uğurla TikTok-a göndərildi!")
      
