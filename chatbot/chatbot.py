# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import streamlit as st

from azure_client_helper import get_client

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
            "content": "Olá! Sou um assistente virtual e estou aqui para lhe ajudar.\\n\\nDiga-me como posso ajudá-lo!",
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
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
