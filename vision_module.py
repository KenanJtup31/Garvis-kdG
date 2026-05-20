# Bu funksiyanı app.py-ə əlavə et
import base64

def analyze_image_with_vision(image_path):
    # Şəkli kodlaşdırırıq ki, AI başa düşsün
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Vision modeli ilə analizi göndəririk
    response = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview", # Vision qabiliyyətli model
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bu şəkildə nə görürsən? Əgər bir mexanizm və ya texniki detal varsa, onun funksiyasını və mümkün nasazlıqlarını izah et."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content
  
