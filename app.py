import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA da Seven", page_icon="🏎️", layout="wide")

st.title("🏎️ Chatbot Oficial Escuderia Seven")
st.markdown("Sou a IA da escuderia Seven, estou aqui para te ajudar!")

# --- CONFIGURAÇÃO DA API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro na Chave API. Verifique os 'Secrets' do Streamlit.")
    st.stop()

# --- CARREGAR O TEXTO (LÊ O ARQUIVO REGRAS.TXT) ---
base_de_conhecimento = ""
try:
    with open('regras.txt', 'r', encoding='utf-8') as f:
        base_de_conhecimento = f.read()
except FileNotFoundError:
    st.error("⚠️ ERRO CRÍTICO: Não encontrei o arquivo 'regras.txt'.")
    st.stop()

# --- CÉREBRO DA IA ---
nome_do_modelo = 'gemini-2.5-flash' # Atualizado para o formato padrão do nome do modelo

prompt_sistema = f"""
Você é a Assistente geral da escuderia 'Seven' (Stem Racing).
Seu objetivo é ajudar a equipe a construir o melhor carro e documentos possíveis dentro das regras.

FONTES DE INFORMAÇÃO:
1. REGULAMENTOS (Prioridade Máxima): Use o texto abaixo (Base de Conhecimento) para responder sobre regras, dimensões, penalidades e prazos. Seja rigorosa com as medidas (mm, gramas).
2. CONHECIMENTO GERAL: Se a pergunta for sobre conceitos de física, aerodinâmica, materiais ou gestão, use seu próprio conhecimento para ensinar.

BASE DE CONHECIMENTO (REGULAMENTOS):
{base_de_conhecimento}

IMPORTANTE:
- Se for uma dúvida de REGRA, cite o artigo (ex: "Segundo T3.4...").
- Se for uma dúvida de ENGENHARIA, explique o conceito físico.
"""

try:
    # Passando as regras como "Instrução de Sistema" em vez de histórico de chat
    modelo = genai.GenerativeModel(
        model_name=nome_do_modelo,
        system_instruction=prompt_sistema
    )
except Exception as e:
    st.error(f"Erro ao carregar o modelo {nome_do_modelo}: {e}")
    st.stop()

# --- CHAT ---
if "chat" not in st.session_state:
    st.session_state.chat = modelo.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Adiciona uma mensagem inicial de boas-vindas do assistente
    st.session_state.messages.append({"role": "assistant", "content": "Entendido. Sou a IA da Sevenspeed. Pode perguntar sobre o regulamento, finanças, captação de recursos ou engenharia!"})

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta
if prompt := st.chat_input("Qual a dúvida sobre o carro ou regras?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro na resposta: {e}")






