import os
import sys

import streamlit as st

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import (
    CharacterTextSplitter,
)
from style.style_config import apply_custom_style

# Caminho para o avatar
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
avatar_path = os.path.join(base_path, "images", "icons", "logo_icon.ico")

# Aplicar estilo customizado
apply_custom_style()

# Título da página
st.title("❓❔ AjudAI PUC Invest ")

# Carregar variáveis de ambiente
load_dotenv()

# Configurar embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", task_type="retrieval_document"
)

# Parâmetros para divisão do texto
chunk_size = 1000
percentual_overlap = 0.3


# Função para abrir arquivo
def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"


# Inicializar o vectorstore no estado da sessão se não existir
if "vectorstore" not in st.session_state:
    arquivo = "puc_invest.md"

    # Obter caminho absoluto para o arquivo
    arquivo_path = os.path.join(base_path, arquivo)

    texto = open_file(arquivo_path)
    filename = os.path.basename(arquivo)
    metadatas = [{"nome do arquivo": filename}]

    text_splitter = CharacterTextSplitter(
        separator=r"%%%",
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size * percentual_overlap),
        length_function=len,
        is_separator_regex=True,
    )

    all_splits = text_splitter.create_documents([texto], metadatas=metadatas)

    # Criar ou carregar o vectorstore
    try:
        # Obter caminho absoluto para o diretório chroma
        chroma_path = os.path.join(base_path, "chroma")
        st.session_state.vectorstore = Chroma.from_documents(
            documents=all_splits, embedding=embeddings, persist_directory=chroma_path
        )
    except Exception as e:
        st.error(f"Erro ao criar banco de dados vetorial: {e}")
        st.session_state.vectorstore = None


def enviar_pergunta(question, docs):
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-lite-latest",
            temperature=0.3,
        )

        prompt = ChatPromptTemplate.from_template(
            """Responda a pergunta do usuário com base no contexto fornecido.

            Contexto: {context}
            Pergunta: {input}

            Você é um assistente especializado em investimentos e finanças, focado em fornecer informações precisas sobre o dashboard FinUp Investimentos.

            Ao responder perguntas:
            1. Use APENAS as informações contidas nos documentos de referência fornecidos.
            2. Se a informação não estiver presente nos documentos, indique claramente que não há informação disponível sobre esse tópico específico.
            3. Seja conciso e direto nas suas respostas.
            4. Forneça detalhes específicos quando disponíveis nos documentos.
            5. Não invente informações que não estejam presentes nos documentos.

            Resposta:"""  # noqa: E501
        )

        chain = create_stuff_documents_chain(llm, prompt)
        resposta = chain.invoke({"context": docs, "input": question})

        return resposta

    except Exception as e:
        return f"Ocorreu um erro: {e}"


# Inicializar histórico de chat se não existir
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Exibir histórico de chat
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        with st.chat_message("assistant", avatar=avatar_path):
            st.write(message["content"])

# Input do usuário
if prompt := st.chat_input("ajudAI PUC Invest Responde..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Exibir mensagem do usuário
    st.chat_message("user").write(prompt)

    # Exibir mensagem do assistente com loading
    with st.chat_message("assistant", avatar=avatar_path):
        message_placeholder = st.empty()

        try:
            if st.session_state.vectorstore:
                # Buscar documentos relevantes
                docs = st.session_state.vectorstore.similarity_search(prompt, k=8)

                # Gerar resposta com a pergunta original
                resposta = enviar_pergunta(question=prompt, docs=docs)

                # Exibir resposta
                message_placeholder.write(resposta)

                # Adicionar resposta ao histórico
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": resposta}
                )
            else:
                message_placeholder.write(
                    "Não foi possível carregar a base de conhecimento. Por favor, tente novamente mais tarde."
                )
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": "Não foi possível carregar a base de conhecimento. Por favor, tente novamente mais tarde.",  # noqa: E501
                    }
                )
        except Exception as e:
            message_placeholder.write(f"Ocorreu um erro: {e}")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": f"Ocorreu um erro: {e}"}
            )
