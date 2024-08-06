# BIBLIOTECAS E MÓDULOS
import os
import streamlit as st
from dotenv import find_dotenv, load_dotenv
import chatbot_normal
# import chatbot_com_rag

# CONSTANTES E VARIÁVEIS DE AMBIENTE
load_dotenv(find_dotenv())
TOKEN_ACESSO = os.getenv("TOKEN_ACESSO", "")
if not TOKEN_ACESSO:
    raise EnvironmentError("TOKEN_ACESSO não está nas variáveis de ambiente!")

# FUNÇÕES

# -----------------------------------------------------------------------------
# Página de login <- pede que o usuário entre com o Token de Acesso

def login():
    token_acesso = st.text_input(
        "Token de acesso", key="usr_token1", type="password"
    )
    if st.button("Log in"):
        if not token_acesso:
            st.info("Insira uma chave de API antes de continuar!".upper())
            st.stop()
        if token_acesso != TOKEN_ACESSO:
            st.info("Token inválido.".upper())
            st.stop()
        st.session_state.logged_in = True
        st.rerun()


# -----------------------------------------------------------------------------
# Página "home"

def home():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

    st.write("# Bem-vindo ao Ultimate Chat Blaster! 👋")

    st.markdown(
        """
        Isso, exatamente, nós manjamos de UI também! Próximo passo é a dominação mundial.

        **👈 Selecione alguma das abas ao lado para ter uma conversa legalzinha com um dos nossos chats**
    """
    )


# =============================================================================
# CÓDIGO

def main() -> None:
    # -----------------------------------------------------------------------------
    # Inicializando o estado da sessão
    # -----------------------------------------------------------------------------

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    # -----------------------------------------------------------------------------
    # Definindo as páginas da aplicação
    # -----------------------------------------------------------------------------

    # Página de login
    login_page = st.Page(login, title="Log in", icon=":material/login:")

    # Página home
    home_page = st.Page(home, title="Home", icon="🏠")

    # Página chatbot convencional
    chatbot = st.Page("chatbot_normal.py", title="Chatbot", icon="🤖")

    # Página chatbot convencional
    chatbot_rag = st.Page("chatbot_com_rag.py", title="Chatbot Rag", icon="🐱")

    # -----------------------------------------------------------------------------
    # Verificando se a sessão atual está logada
    # -----------------------------------------------------------------------------

    if st.session_state.logged_in:
        pg = st.navigation({
            "Home": [home_page],
            "Chats": [chatbot, chatbot_rag],
        })
    else:
        pg = st.navigation([login_page])

    # -----------------------------------------------------------------------------
    # Inicializando a aplicação
    # -----------------------------------------------------------------------------

    pg.run()

    return None


if __name__ == "__main__":
    main()
