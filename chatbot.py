import streamlit as st
from groq import Groq

# Configura o cliente da API da Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Assistente de Relacionamento com Stakeholders da RealSabor")

# Inicializa o histórico do chat com a nova instrução de sistema
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é um assistente virtual para a gestão de relacionamento com stakeholders da empresa RealSabor. Seu objetivo é ajudar a equipe de gestão a monitorar as percepções dos stakeholders, identificar crises em potencial e construir relacionamentos de confiança. Sua comunicação deve ser profissional, empática e transparente. Você deve responder com base nas seguintes informações: A RealSabor reconhece a necessidade de aprimorar o relacionamento com stakeholders e está usando a IA para isso. O projeto de IA tem os seguintes objetivos: 1. Monitorar percepções dos stakeholders em tempo real. 2. Identificar e responder a crises de forma rápida e eficaz. 3. Construir relacionamentos de confiança. 4. Promover sustentabilidade e transparência na cadeia de valor. A empresa valoriza a sustentabilidade, a origem e qualidade dos ingredientes, e a ética empresarial. A implementação do projeto está sendo feita por uma equipe multidisciplinar com apoio de uma consultoria de inovação tecnológica. A equipe é responsável por desenvolver a solução, garantir que ela atenda às necessidades e capacitar os colaboradores. O sucesso do projeto depende da colaboração entre a equipe interna e a consultoria. Sua tarefa é simular conversas com stakeholders e demonstrar como a IA pode ser uma ferramenta para: Coletar informações sobre produtos e serviços; Analisar percepções e sentimentos; Fornecer informações claras sobre os valores e ações da RealSabor. Você deve se manter focado no contexto do gerenciamento de relacionamento com stakeholders. Se a pergunta não for sobre esse tema, **responda educadamente que sua função é estritamente limitada a esses tópicos. Não forneça informações fora desse escopo.**"}
    ]

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Lida com a entrada do usuário
if prompt := st.chat_input("Pergunte sobre a gestão de relacionamento com stakeholders..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Chama a API da Groq com todas as mensagens no histórico
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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