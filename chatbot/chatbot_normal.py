# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import json
import streamlit as st
import logging
from azure_client_helper import get_client
import socket

# =============================================================================
# CÓDIGO
# =============================================================================

# ---------------- logs ------------------

# salva info basica do chatbot
logging.basicConfig(
    filename='./logs/chatbot_norm_info.logs',
    level=logging.INFO,
    format='%(asctime)s; %(message)s;',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Logger para os prompts
prompt_logger = logging.getLogger('prompt_logger')

if not prompt_logger.handlers:
    prompt_handler = logging.FileHandler('./logs/chatbot_prompt.logs')
    prompt_handler.setFormatter(logging.Formatter('%(asctime)s;%(message)s;', datefmt='%Y-%m-%d %H:%M:%S'))
    prompt_logger.addHandler(prompt_handler)

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
    
    # Log do prompt
    prompt_logger.info(f'Input: {tokens_input};Output: {tokens_output};Total: {total_tokens};PROMPT: {prompt}')

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
