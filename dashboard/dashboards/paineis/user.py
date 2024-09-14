import streamlit as st
import pandas as pd


def exibir_tabela_usuarios(token, dados_usuario):
    df_usuarios = pd.DataFrame(dados_usuario)
    
    # Exibe a tabela de usuários no Streamlit
    st.title("Tabela de Usuários")
    st.table(df_usuarios[['nome', 'email', 'tipo_usuario']])  # Exibe somente as colunas relevantes