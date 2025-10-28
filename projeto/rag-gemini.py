import os

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", task_type="retrieval_document")

chunk_size = 1000
percentual_overlap = 0.2

criar_db = True


def open_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"


if criar_db:
    arquivo = "projeto/puc_invest.md"
    texto = open_file(arquivo)
    filename = os.path.basename(arquivo)
    metadatas = [{"nome do arquivo": filename}]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size * percentual_overlap),
        length_function=len,
    )

    all_splits = text_splitter.create_documents([texto], metadatas=metadatas)
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory="chroma")
    print("Banco de dados criado/atualizado.")

else:
    print("Usando banco de dados existente.")
    vectorstore = Chroma(embedding_function=embeddings, persist_directory="chroma")

question = "O que é o PUC Invest?"

docs = vectorstore.similarity_search(question, k=4)


def enviar_pergunta(question, docs):
    try:
        llm = ChatGoogleGenerativeAI(model="models/gemini-flash-lite-latest", temperature=0)
        prompt = ChatPromptTemplate.from_template(
            """Responda a pergunta do usuário com base no contexto fornecido.

            Contexto: {context}
            Pergunta: {input}

            Resposta:"""
        )

        chain = create_stuff_documents_chain(llm, prompt)
        resposta = chain.invoke({"context": docs, "input": question})
        return resposta

    except Exception as e:
        return f"Ocorreu um erro: {e}"


resposta = enviar_pergunta(question, docs)
print("Pergunta: ", question)
print("Resposta: ", resposta)
