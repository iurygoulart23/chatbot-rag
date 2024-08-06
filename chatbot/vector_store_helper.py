# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import os
from io import BytesIO
from pathlib import Path
from typing import List

from dotenv import find_dotenv, load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from common import get_path_projeto

# =============================================================================
# CONSTANTES E VARIÁVEIS DE AMBIENTE
# =============================================================================

load_dotenv(find_dotenv())

AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "")
if not AZURE_DEPLOYMENT:
    raise EnvironmentError(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT não está nas variáveis de ambiente!"
    )

# gera o path do projeto e path pra pasta data
DIR_PROJETO = get_path_projeto()
DIR_DADOS = Path(DIR_PROJETO) / "data"
DIR_DADOS.mkdir(exist_ok=True)

MODELO_EMBEDDING = AzureOpenAIEmbeddings(azure_deployment=AZURE_DEPLOYMENT)


# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Retorna o arquivo pdf como uma lista de documentos picotados para a vector store
# -----------------------------------------------------------------------------


def carrega_pdf(documento_pdf: BytesIO) -> List[Document]:
    path_pdf = DIR_DADOS / documento_pdf.name
    if not path_pdf.exists():
        with open(path_pdf, "wb") as pdf_f:
            pdf_f.write(documento_pdf.read())

    loader = PyPDFLoader(path_pdf)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    os.remove(path_pdf)

    return docs


# -----------------------------------------------------------------------------
# Cria uma vector store
# -----------------------------------------------------------------------------


def cria_vectorstore(
    documento_pdf: BytesIO,
    path_destino: Path) -> VectorStoreRetriever:
    
    docs = carrega_pdf(documento_pdf)
    db = FAISS.from_documents(docs, MODELO_EMBEDDING)
    db.save_local(str(path_destino))

    return db.as_retriever()


# -----------------------------------------------------------------------------
# Retorna uma vector store como referencia
# -----------------------------------------------------------------------------


def get_vectorstore_as_retriver(
    documento_pdf: BytesIO) -> VectorStoreRetriever:
    
    path_vectorstore = DIR_DADOS / f"{Path(documento_pdf.name).stem}"

    if not path_vectorstore.exists():
        return cria_vectorstore(documento_pdf, path_vectorstore)

    return FAISS.load_local(
        str(path_vectorstore),
        MODELO_EMBEDDING,
        allow_dangerous_deserialization=True,
    ).as_retriever()
