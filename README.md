
# Projeto para Criação de um Chatbot

**Autor:** Iury Goulart
___
No momento o chatbot-rag ainda está em desenvolvimento...
Porém o chatbot normal já está finalizado e funcional.
___

### Requisitos
- **Python:** 3.10
- **python-dotenv:** 1.0.1
- **pyyaml:** 6.0.1
- **langchain:** 0.2.11
- **langchain-openai:** 0.1.19
- **tiktoken:** 0.7.0
- **streamlit:** 1.37.0
- **langchain-community:** 0.2.10
- **faiss-cpu:** 1.8.0
- **pypdf:** 4.3.1

___

## Como Usar

### Passos
1. Crie um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   ```

2. Instale as dependências:
   ```sh
   pip install -r ./requirements/prod.txt
   ```

3. Crie o arquivo `.env` com as variáveis de ambiente:
   ```env
   NOME_PROJETO=chatbot

   # Token de acesso é a senha que usará para acessar o chat
   TOKEN_ACESSO=iury12345

   # Tokens da Azure
   AZURE_OPENAI_API_KEY=**********
   OPENAI_API_VERSION=**********
   AZURE_OPENAI_ENDPOINT=**********
   AZURE_OPENAI_LOCATION=**********
   AZURE_OPENAI_CHAT_DEPLOYMENT=**********
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=**********
   ```

4. Rode o comando:
    ```sh
    streamlit run ./chatbot/app.py
    ```