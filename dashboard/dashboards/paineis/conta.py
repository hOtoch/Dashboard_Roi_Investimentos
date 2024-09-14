import streamlit as st
import pandas as pd
import api

def exibir_tabela_contas(token, dados_contas, dados_usuario):

    df_contas = pd.DataFrame(dados_contas)
    df_usuarios = pd.DataFrame(dados_usuario)
    
    mapa_usuarios = pd.Series(df_usuarios.nome.values, index=df_usuarios.id).to_dict()
    
    df_contas['nome_usuario'] = df_contas['usuario_id'].map(mapa_usuarios)
    df_contas.drop('inicio', axis=1, inplace=True)
    
    # Exibe a tabela de contas no Streamlit
    st.title("Tabela de Contas")
    st.table(df_contas[['nome_usuario','nome', 'deposito_inicial','saldo_atual','multiplicador','plano','meses','liquido','comissao','comissao_fundo','saques','margem_lucro', 'operacoes_finalizadas']])  # Exibe somente as colunas relevantes


