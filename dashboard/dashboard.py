import streamlit as st
import jwt
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')


if not SECRET_KEY:
    st.error("Chave secreta JWT não encontrada. Verifique as variáveis de ambiente.")

def verificar_token(token):
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Retorna o payload se for válido
    except jwt.ExpiredSignatureError:
        st.error("Token expirado. Faça login novamente.")
        return None
    except jwt.InvalidTokenError:
        st.error("Token inválido. Faça login novamente.")
        return None

# Função para extrair parâmetros da URL
def get_params():
    query_string = st.query_params
    token = query_string.get('token')
    return token

# Função principal do Streamlit
def main():
    token = get_params()
    
    # Verifica se o token foi passado na URL
    if token:
        payload = verificar_token(token)
        if payload:
            st.success(f"Bem-vindo, usuário {payload['sub']} ! Token válido.")
            # Exibe o dashboard ou dados relacionados ao usuário
            # Aqui você pode acessar as informações de `user_id` ou outras do payload JWT
        else:
            st.error("Autenticação falhou. Faça login novamente.")
    else:
        st.error("Acesso não autorizado. Por favor, faça login.")

if __name__ == "__main__":
    main()
    
    st.title("Dashboard")
    st.sidebar.title("Menu")

    # Dados exemplo no dashboard
    st.write("Bem-vindo ao seu dashboard.")
    chart_data = {"dados": [10, 20, 30, 40]}
    st.line_chart(chart_data)



