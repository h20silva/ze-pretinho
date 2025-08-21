# app.py
import streamlit as st
import requests
import os
from gtts import gTTS
import tempfile
import base64

# Configuração da página
st.set_page_config(
    page_title="💬 Zé Pretinho",
    page_icon="🌸",
    layout="centered"
)

# Estilo CSS
st.markdown("""
    <style>
    .main { background-color: #f0f8ff; }
    .title { color: #8B4513; text-align: center; font-size: 2.5em; font-weight: bold; }
    .response { background-color: #e6f7ff; padding: 12px; border-radius: 12px; margin: 10px 0; max-width: 80%; margin-left: 0; }
    .user { background-color: #d4edda; padding: 12px; border-radius: 12px; margin: 10px 0; max-width: 80%; margin-left: auto; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# Título
st.markdown('<h1 class="title">💬 Zé Pretinho</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>O assistente que fala a verdade sem ofender!</h3>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "E aí, meu parceiro! Fala com o Zé!"}
    ]

# Função para falar
def falar(texto):
    try:
        tts = gTTS(texto, lang='pt', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            audio_file = f.name
        return audio_file
    except Exception as e:
        st.error(f"Erro ao gerar áudio: {e}")
        return None

# Mostrar histórico
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="response">👨‍💻 **Zé Pretinho:** {message["content"]}</div>', unsafe_allow_html=True)
        # Gera e toca áudio
        audio_file = falar(message["content"])
        if audio_file:
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
            <audio autoplay controls style="width: 100%;">
                <source src="audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user">🙂 **Você:** {message["content"]}</div>', unsafe_allow_html=True)

# Função para chamar Hugging Face
def gerar_resposta(pergunta):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}

    payload = {
        "inputs": pergunta,
        "max_new_tokens": 128,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()[0]["generated_text"].strip()
        else:
            return f"Erro {response.status_code}: não consegui pensar agora. Tenta de novo?"
    except Exception as e:
        return f"Zé Pretinho tá com problema: {str(e)}"

# Entrada do usuário
user_input = st.text_input("Digite sua mensagem (ou 'sair' para encerrar):", key="input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Zé Pretinho tá pensando..."):
        resposta = gerar_resposta(user_input)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Zé Pretinho © 2025 • Feito com Python, IA e muito amor</p>", unsafe_allow_html=True)