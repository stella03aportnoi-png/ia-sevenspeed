import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA Sevenspeed", page_icon="🏎️", layout="wide")

st.title("🏎️ Chatbot Oficial Sevenspeed")
st.markdown("Sou a IA especialista nos regulamentos da F1 in Schools. Pergunte!")

# --- CONFIGURAÇÃO DA API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Configure a GEMINI_API_KEY nos 'Secrets' do Streamlit.")
    st.stop()

# --- CARREGAR O TEXTO DO ARQUIVO ---
# Aqui a mágica acontece: ele lê o arquivo que você criou separado
try:
    with open('regras.txt', 'r', encoding='utf-8') as f:
        base_de_conhecimento = f.read()
except FileNotFoundError:
    st.error("⚠️ Erro: Não encontrei o arquivo 'regras.txt'. Crie ele no GitHub e cole o texto lá!")
    st.stop()

# --- CÉREBRO DA IA ---
modelo = genai.GenerativeModel('gemini-1.5-flash')

prompt_sistema = f"""
Você é a Engenheira Chefe da equipe 'Sevenspeed'.
Responda dúvidas sobre regras, dimensões e projeto baseada EXCLUSIVAMENTE no texto abaixo.

BASE DE CONHECIMENTO:
{base_de_conhecimento}
"""

# --- CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = modelo.start_chat(history=[
        {"role": "user", "parts": prompt_sistema},
        {"role": "model", "parts": "Entendido. Pode perguntar sobre as regras!"}
    ])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Qual a dúvida?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro na IA: {e}")
