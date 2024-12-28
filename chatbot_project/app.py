import streamlit as st
import requests

# FastAPI API URL
API_URL = "http://localhost:8000/search/"

# Streamlit Başlığı
st.title("Temmuz 2023 Halka Arz İhraççı Bilgi Dokümanı Chatbot")
st.write("Bu chatbot, T. İş Bankası'nın Temmuz 2023 Halka Arz İhraççı Bilgi Dokümanı temel alınarak sorularınıza yanıt verir.")

# Kullanıcıdan Sorgu Al
query = st.text_input("Sorunuzu yazın:", "")

if st.button("Sorguyu Gönder"):
    if query:
        # API'ye istek gönder
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            st.write("### Yanıt:")
            st.write(response.json().get("answer", "Yanıt bulunamadı."))
        else:
            st.error("Hata: Yanıt alınamadı. API'nizi kontrol edin.")
    else:
        st.warning("Lütfen bir soru yazın.")
