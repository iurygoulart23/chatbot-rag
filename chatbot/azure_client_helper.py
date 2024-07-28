import os
from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI

# =============================================================================
# CONSTANTES E VARIÁVEIS DE AMBIENTE
# =============================================================================

load_dotenv(find_dotenv())

AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "")
if not AZURE_DEPLOYMENT:
    raise EnvironmentError(
        "AZURE_OPENAI_CHAT_DEPLOYMENT não está nas variáveis de ambiente!"
    )

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Retorna o client da API Azure OpenAI
# -----------------------------------------------------------------------------


def get_client() -> AzureChatOpenAI:
    client_azure_openai = AzureChatOpenAI(azure_deployment=AZURE_DEPLOYMENT)
    return client_azure_openai
    return client_azure_openai
