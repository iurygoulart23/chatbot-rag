# BIBLIOTECAS E MÓDULOS

from pathlib import Path

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from azure_client_helper import get_client
from common import get_path_projeto
from vector_store_helper import get_vectorstore_as_retriver

# =============================================================================
# CONSTANTES E VARIAVEIS DE AMBIENTE
# =============================================================================

DIR_PROJETO = get_path_projeto()
assert isinstance(DIR_PROJETO, Path)

TEMPLATE_PROMPT = """Responda a pergunta utilizando o contexto como base, mas enriqueça a resposta se você souber sobre o assunto:

{context}

Pergunta: {question}
"""
PROMPT = ChatPromptTemplate.from_template(TEMPLATE_PROMPT)

# =============================================================================
# CÓDIGO
# =============================================================================

# -----------------------------------------------------------------------------
# Inicializando o cliente da API
# -----------------------------------------------------------------------------

azure_client = get_client()


# -----------------------------------------------------------------------------
# Título da página
# -----------------------------------------------------------------------------

st.title("💬 Chatbot com RAG")

# -----------------------------------------------------------------------------
# Parte responsavel pelo upload do arquivo do usuario
# -----------------------------------------------------------------------------

arquivo_upado = st.file_uploader("Faça o upload de um arquivo.", type=("pdf"))

pergunta = st.text_input(
    "Pergunte algo sobre o conteúdo do arquivo.",
    placeholder="Você poderia falar mais sobre X?",
    disabled=not arquivo_upado,
)


# -----------------------------------------------------------------------------
# Parte responsavel pelo RAG
# -----------------------------------------------------------------------------


def gruda_pedacos(docs):
    return "\\n\\n".join(doc.page_content for doc in docs)


rag_chain = None
if arquivo_upado:
    vectorstore_as_retriver = get_vectorstore_as_retriver(arquivo_upado)
    rag_chain = (
        {
            "context": vectorstore_as_retriver | gruda_pedacos,
            "question": RunnablePassthrough(),
        }
        | PROMPT
        | azure_client
        | StrOutputParser()
    )


# -----------------------------------------------------------------------------
# Lógica que roda quando usuário faz uma pergunta no chat
# -----------------------------------------------------------------------------

if arquivo_upado and pergunta and rag_chain:
    msg = rag_chain.invoke(pergunta)
    st.chat_message("assistant").write(msg)

