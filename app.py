import streamlit as st
import google.generativeai as genai
import os

st.title("🔧 Modo de Diagnóstico Sevenspeed")

# 1. Teste da Chave
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ ERRO: Chave API não encontrada nos Secrets.")
    st.stop()
else:
    st.success(f"✅ Chave encontrada! (Começa com: {api_key[:4]}...)")

# 2. Configurar Google
try:
    genai.configure(api_key=api_key)
    st.write(f"📚 Versão da biblioteca Google: {genai.__version__}")
except Exception as e:
    st.error(f"❌ Erro ao configurar: {e}")

# 3. Testar quais modelos estão disponíveis para VOCÊ
st.write("🔍 Pesquisando modelos disponíveis para sua chave...")
try:
    modelos_disponiveis = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            modelos_disponiveis.append(m.name)
    
    if modelos_disponiveis:
        st.success(f"✅ Modelos encontrados: {modelos_disponiveis}")
        
        # Tenta usar o primeiro modelo que encontrar
        modelo_escolhido = modelos_disponiveis[0]
        st.info(f"🤖 Tentando conectar com: {modelo_escolhido}")
        
        model = genai.GenerativeModel(modelo_escolhido)
        response = model.generate_content("Diga 'Olá Equipe Sevenspeed'")
        st.balloons()
        st.success(f"🎉 SUCESSO! O modelo respondeu: {response.text}")
        st.markdown("---")
        st.markdown("### Agora sabemos que funciona! Pode voltar o código do chat.")
        
    else:
        st.warning("⚠️ A conexão funcionou, mas nenhum modelo foi encontrado para essa chave.")
        
except Exception as e:
    st.error(f"❌ ERRO GRAVE DE CONEXÃO: {e}")
    st.markdown("""
    **Soluções Possíveis:**
    1. Sua API Key pode não ter permissões (Crie uma nova).
    2. O Google AI Studio pode não estar disponível na região do servidor (EUA).
    """)
