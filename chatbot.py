import streamlit as st
from groq import Groq

# Configura o cliente da API da Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Atendimento RealSabor")

# Inicializa o histórico do chat com a instrução de sistema
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é um representante de atendimento ao cliente da RealSabor. Sua função é fornecer informações precisas sobre a empresa e seus produtos, que são temperos e realçadores de sabor para a indústria de alimentos. Responda perguntas baseando-se nas seguintes informações: A RealSabor foi fundada no sul do Brasil nos anos 1950 por uma família de imigrantes. Inicialmente, a empresa fornecia temperos e realçadores de sabor para a indústria de alimentos. Com a rápida urbanização, impulsionou o consumo de alimentos semiprontos e congelados. Nos anos 2000, com o apoio de investidores, a empresa se tornou uma multinacional, com presença na América Latina, EUA, Canadá e Austrália. A cultura organizacional da empresa é baseada em tradição e confiança. Há um forte respeito à hierarquia, disciplina e foco em processos. O processo de contratação é baseado em indicações e confiança, transformando o 'funcionário indicador' em mentor. As vendas e o marketing são baseados em relacionamentos de longo prazo com grandes clientes industriais. A empresa foca no canal B2B (empresas para empresas) e distribuidores para vendas ao varejo e ao consumidor final. A RealSabor incorpora robótica e outras tecnologias para se adaptar à Indústria 4.0. A empresa valoriza sustentabilidade, a origem e qualidade dos ingredientes, e a ética empresarial. Mantenha a comunicação profissional, focada nos valores de tradição e confiança da empresa. Se a pergunta não for sobre a RealSabor, responda educadamente que você só pode fornecer informações sobre a empresa e seus produtos."}
    ]

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Lida com a entrada do usuário
if prompt := st.chat_input("Pergunte sobre a RealSabor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Chama a API da Groq com todas as mensagens no histórico, incluindo a instrução de sistema
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Nome do modelo Llama 3
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
        )
        response_text = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
            
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")