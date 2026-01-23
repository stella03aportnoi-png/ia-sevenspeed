import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA Sevenspeed", page_icon="🏎️", layout="wide")

st.title("🏎️ Chatbot Oficial Sevenspeed")
st.markdown("Sou a IA especialista nos regulamentos da F1 in Schools. Pergunte!")

# --- CONFIGURAÇÃO DA API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro na Chave API. Verifique os 'Secrets' do Streamlit.")
    st.stop()

# --- CARREGAR O TEXTO (LÊ O ARQUIVO REGRAS.TXT) ---
try:
    with open('regras.txt', 'r', encoding='utf-8') as f:
        base_de_conhecimento = f.read()
except FileNotFoundError:
    st.error("⚠️ ERRO CRÍTICO: Não encontrei o arquivo 'regras.txt' no GitHub. Crie ele e cole os regulamentos lá!")
    st.stop()

# --- CÉREBRO DA IA ---
# Vamos tentar o Flash primeiro, se falhar, ele avisa
modelo = genai.GenerativeModel('gemini-1.5-flash')

prompt_sistema = f"""
Você é a Engenheira Chefe da equipe 'Sevenspeed'.
Responda dúvidas sobre regras, dimensões, penalidades e projeto baseada EXCLUSIVAMENTE no texto abaixo.

BASE DE CONHECIMENTO (REGULAMENTOS):
{base_de_conhecimento}
"""

# --- CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = modelo.start_chat(history=[
        {"role": "user", "parts": prompt_sistema},
        {"role": "model", "parts": "Entendido. Estou pronta para ajudar com as regras e engenharia."}
    ])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta
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
        st.info("Dica: Se o erro for 404, tente ir em 'Manage App' > 'Reboot' para atualizar a biblioteca.")
