# app.py
import streamlit as st
import requests

# Konfigurasi API (FastAPI backend)
API_URL = "http://127.0.0.1:8000/chat"  # Pastikan backend sudah jalan

# Konfigurasi tampilan halaman
st.set_page_config(page_title="WiFiBot - Customer Assistant", page_icon="📶", layout="centered")

st.markdown(
    """
    <style>
    .chat-container {
        max-width: 600px;
        margin: auto;
        background: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-align: right;
    }
    .bot-bubble {
        background-color: #E8EAF6;
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📶 WiFiBot - Customer Assistant")
st.write("Halo! Saya **WiFiBot**, siap membantu keluhan atau pertanyaan Anda seputar layanan internet 🌐")

# Session state untuk menyimpan percakapan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat percakapan
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input user
user_input = st.text_input("Ketik pesan Anda...", key="user_input")

if st.button("Kirim") and user_input:
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Kirim ke backend FastAPI
    try:
        response = requests.post(API_URL, json={"message": user_input})
        bot_reply = response.json().get("reply", "Maaf, terjadi kesalahan.")
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Simpan balasan bot
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

    # Refresh halaman agar bubble muncul
    st.experimental_rerun()
