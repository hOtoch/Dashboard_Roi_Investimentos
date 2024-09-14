import streamlit as st
import pandas as pd
import api

def exibir_tabela_ciclomes(token,dados_ciclomes):
    df_ciclomes = pd.DataFrame(dados_ciclomes)

    st.title("Tabela de Meses")
    st.table(df_ciclomes[['nome', 'ano','atual', 'investimento', 'alcancado','projecao','porcentagem_alcancado','dias', 'shark', 'valor_liquido']]) 
    
    st.title("Tabela de Dias")
    mes_selecionado_nome =st.selectbox('Selecione um Mes', df_ciclomes['nome'])
    
    mes_selecionado = df_ciclomes[df_ciclomes['nome'] == mes_selecionado_nome].iloc[0]
    
    dados_dias = api.get_dias(token, mes_selecionado['id'])
    
    if dados_dias:
        df_dias = pd.DataFrame(dados_dias)
        df_dias['dia_num'] = range(1, len(df_dias) + 1)
        
        st.table(df_dias[['dia_num','juros','alcancado_dia']])
        
    else:
        st.warning("Não há dias cadastrados para este mês.")