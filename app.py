import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA Sevenspeed", page_icon="🏎️", layout="wide")

# Cabeçalho
st.title("🏎️ Chatbot Oficial Sevenspeed")
st.markdown("""
Bem-vindo! Sou a inteligência artificial da equipe **Sevenspeed**. 
Estou treinada com:
* Regulamentos Técnicos e de Competição (2025)
* Regras do Projeto Social
* Guia de Gestão de Projetos (PMIEF)
""")

# --- CONFIGURAÇÃO DA API (CÉREBRO) ---
# O Streamlit vai buscar a senha nos "Secrets" do servidor
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro de Configuração: Não encontrei a chave da API. Se você é o dono do site, verifique os 'Secrets' no painel do Streamlit.")
    st.stop()

# --- BASE DE CONHECIMENTO (SEUS DOCUMENTOS) ---
# Aqui estão todos os textos que você enviou, organizados.
base_de_conhecimento = """
================================================================================
DOCUMENTO 1: REGULAMENTO TÉCNICO STEM RACING 2025 (RESUMO TÉCNICO)
================================================================================
(Principais regras técnicas inseridas anteriormente)
T3.4 Total width: Min 65.0mm / Max 85.0mm
T3.5 Total height: Max 65.0mm
T3.6 Total weight: Min 48.0g
T3.7 Track clearance: Min 1.5mm
T4.4 Halo: Obrigatório uso do arquivo oficial.
T5.1 Chamber Diameter: Min 18.0mm / Max 18.5mm
T7.1 Wheels: 4 rodas obrigatórias.
T9.5.1 Rear Wing Span: Min 50.0mm

================================================================================
DOCUMENTO 2: REGULAMENTO PROJETO SOCIAL 2024/2025
================================================================================
CLÁUSULA PS 1 – DEFINIÇÃO
PS 1.1 Porquê do Projeto Social: O projeto F1 in Schools busca proporcionar aos alunos participantes experiências práticas de empreendedorismo...
PS 1.2 O que são Projetos Sociais: Projetos sociais são iniciativas individuais ou coletivas que visam proporcionar a melhoria da qualidade de vida...
CLÁUSULA PS 5 – FORMATO DA COMPETIÇÃO (até 80 pontos)
PS 5.1 O que será julgado? A escolha do tema, originalidade, inovação, relevância para a comunidade...
PS 5.5 Requisitos do Portfólio: Portfólio A4 (capa + 7 páginas) e Vídeo de 2 minutos.

================================================================================
DOCUMENTO 3: REGULAMENTO DE COMPETIÇÃO (COMPETITION REGULATIONS 2025)
================================================================================
ARTICLE C1 – DEFINITIONS
C1.1 World Finals Event: Managed by STEM Racing™, aims to determine World Champions.
C1.7 Car race time value: Actual time taken for a car to travel the track.
C1.12 Engineering drawings: CAD produced drawings including dimensions, tolerances and material information.
C1.14 Team Digital Upload Folder: Where all digitally submitted work must be uploaded.

ARTICLE C2 – GENERAL INFORMATION
C2.1.2 Team Size: Minimum 3 students, maximum 6.
C2.3.4 Team Name: Cannot use Formula 1 Word Marks (e.g. "Infinity F1" is not allowed).
C2.11 Mandatory project elements:
- 2 Race Cars + 1 Display Car + 1 Unfinished Body + 1 Halo/Helmet.
- Portfolios: Design & Engineering (11 pages), Enterprise (12 pages), Project Management (7 pages).
- Pit Display.
- Verbal Presentation (10 mins).
- Engineering Drawings.

C2.13 Submission:
- Digital submission deadline: Sunday 14th September 2025 23:00 (GMT).
- Physical submission: Cars, Portfolios (2 copies each), Drawings.

ARTICLE C3 – COMPETITION AND JUDGING FORMAT
C3.5 Point Allocations (Total 1000 points):
- Scrutineering: 160 pts
- Design & Engineering: 180 pts
- Project Management: 90 pts
- Enterprise: 180 pts (Portfolio 100, Identity 20, Pit Display 60)
- Verbal Presentation: 140 pts
- Racing: 250 pts (Time Trials 105, Reaction 105, Knock-out 30, Fastest Car Bonus 10)

ARTICLE C4 – SPECIFICATION & SCRUTINEERING JUDGING
C4.1 What will be judged? Detailed inspection of BOTH race cars.
C4.5 Safe/Fit to race fix: 20-minute car service provided if car is unsafe.

ARTICLE C7 – ENTERPRISE JUDGING
C7.5 Enterprise Portfolio: Max 12 pages (A3). Content: Marketing, Sponsorship/ROI, Digital Media, Sustainability.
C7.6 Pit Display: Max 2 hours setup time. No outside assistance allowed. Max dimensions typically 3m x 1m x 2.4m (to be confirmed).

ARTICLE C9 – RACING
C9.1 Races: Reaction Racing (8 races total) and Knock-out Competition.
C9.11 Deceleration: Teams must use the Halo deceleration system.

================================================================================
DOCUMENTO 4: PROJECT MANAGEMENT GUIDE 2023/24 (GUIA DE GESTÃO)
================================================================================
PRINCIPLES OF PROJECT MANAGEMENT
Triple Constraints: Scope, Time (Schedule), Cost (Budget).
Key Roles: Project Manager, Stakeholder, Sponsor, Team Members.

THE PROJECT MANAGEMENT PROCESS (5 Phases):
1. Initiating: Define project, Identify stakeholders, Project Charter.
2. Planning: Scope statement, WBS (Work Breakdown Structure), Schedule (Gantt), Budget, RACI Matrix, Risk Plan.
3. Executing: Working through the plan.
4. Monitoring and Controlling: Scope validation, Status Reports, Adjusting for unexpected.
5. Closing: Final presentation, Lessons Learned, Celebration.

PORTFOLIO REQUIREMENTS (Project Management):
Max 7 pages (A3).
- Initiating (35 pts): Initiation Process, Project Schedule.
- Planning (25 pts): Budget/Resource Management, Roles and Responsibilities.
- Executing (20 pts): Team & Stakeholder Comm, Risk Management.
- Monitoring and Controlling (10 pts): Monitoring & Controlling.

Risk Management:
Identify risks (Threats or Opportunities). Use a Risk Assessment Matrix (Impact vs Probability). Responses: Mitigate, Avoid, Accept, etc.

Tools suggested: Gantt Charts, RACI Matrix, Budget Tables, Status Reports.
"""

# --- INSTRUÇÕES PARA A IA ---
modelo = genai.GenerativeModel('gemini-1.5-flash')

# Aqui definimos como a IA deve se comportar
prompt_sistema = f"""
Você é o assistente virtual oficial da equipe de F1 in Schools 'Sevenspeed'.
Seu objetivo é ajudar membros da equipe, juízes e interessados a entenderem o projeto e as regras complexas da competição.

Sua fonte de verdade é EXCLUSIVAMENTE o texto abaixo (Base de Conhecimento).
Se a resposta não estiver no texto, diga: "Desculpe, essa informação não consta nos regulamentos que tenho acesso no momento."

BASE DE CONHECIMENTO:
{base_de_conhecimento}

IMPORTANTE:
1. Ao responder sobre regras, tente citar o artigo (ex: "Conforme o artigo T3.4...").
2. Se perguntarem sobre prazos ou pontos, seja exato.
3. Seja educado e incentive a equipe Sevenspeed.
"""

chat = modelo.start_chat(history=[
    {"role": "user", "parts": prompt_sistema},
    {"role": "model", "parts": "Entendido. Sou a IA da Sevenspeed e estou pronta para responder com base nos regulamentos e guias fornecidos."}
])

# --- INTERFACE DE CHAT ---
# Inicializa o histórico do chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada do usuário
if prompt := st.chat_input("Pergunte sobre regulamento, pontuação ou gestão..."):
    # Mostra a pergunta do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # A IA pensa e responde
    try:
        response = chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro ao conectar com a IA: {e}")