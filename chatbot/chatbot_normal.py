# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import json
import streamlit as st
import logging
from azure_client_helper import get_client

# =============================================================================
# CÓDIGO
# =============================================================================

# ---------------- logs ------------------

logging.basicConfig(
    filename='./logs/chatbot_normal.logs',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# -----------------------------------------------------------------------------
# Inicializando o cliente da API
# -----------------------------------------------------------------------------

azure_client = get_client()


# -----------------------------------------------------------------------------
# Título da página
# -----------------------------------------------------------------------------

st.title("💬 Chatbot")

# -----------------------------------------------------------------------------
# Inicializando o histórico do chat
# -----------------------------------------------------------------------------


def inicializa_historico() -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Você é um assistente virtual, auxilie com as informações e tarefas que o usuário pedir.",
        },
        {
            "role": "assistant",
            "content": "Olá! Sou um assistente virtual e estou aqui para lhe ajudar.  \n  Diga-me como posso ajudá-lo!",
        },
    ]


if "messages" not in st.session_state:
    st.session_state["messages"] = inicializa_historico()
elif "RAG" in st.session_state["messages"][0]["content"]:
    st.session_state["messages"] = inicializa_historico()

# -----------------------------------------------------------------------------
# Printa o histórico do chat
# -----------------------------------------------------------------------------

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# -----------------------------------------------------------------------------
# Lógica que roda quando usuário faz uma pergunta no chat
# -----------------------------------------------------------------------------

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    resposta_api = azure_client.invoke(input=st.session_state.messages)
    msg = resposta_api.content
    
    # save tokens to log
    metadados = resposta_api.response_metadata
    
    metadados = metadados.get('token_usage')

    tokens_input = metadados.get('prompt_tokens')
    tokens_output = metadados.get('completion_tokens')
    total_tokens = metadados.get('total_tokens')
    
    # Log dos tokens
    logging.info(f'Tokens usados - Input: {tokens_input}, Output: {tokens_output}, Total: {total_tokens}')

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
