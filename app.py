# app.py
import streamlit as st

st.markdown("<h1 style='text-align: center;'>💬 Zé Pretinho</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>O assistente que fala a verdade sem ofender!</h3>", unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "E aí, meu parceiro! Fala com o Zé!"}
    ]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f"👨‍💻 **Zé Pretinho:** {message['content']}")
    else:
        st.markdown(f"🙂 **Você:** {message['content']}")

user_input = st.text_input("Digite sua mensagem:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    resposta = "Ih, meu irmão... o Zé tá pensando ainda! Em breve ele vai responder com IA!"
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.rerun()# app.py
import streamlit as st
import requests
import os

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

# Mostrar histórico
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="response">👨‍💻 **Zé Pretinho:** {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user">🙂 **Você:** {message["content"]}</div>', unsafe_allow_html=True)

# Função para chamar Hugging Face
def gerar_resposta(pergunta):
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.7,
        "max_tokens": 128
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Ih, meu irmão... o Zé tá com problema de conexão. Tenta de novo?"

# Entrada do usuário
user_input = st.text_input("Digite sua mensagem (ou 'sair' para encerrar):", key="input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    resposta = gerar_resposta(user_input)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.rerun()

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Zé Pretinho © 2025 • Feito com Python, IA e muito amor</p>", unsafe_allow_html=True)