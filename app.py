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
    st.rerun()