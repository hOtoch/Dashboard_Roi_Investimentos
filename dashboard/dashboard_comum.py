import streamlit as st
import api
import pandas as pd
import plotly.express as px

def dashboard_comum(token):
    st.title("Dashboard Mês")
    
    dados_ciclomeses = api.get_ciclomeses(token)
    
    mes_ativo = [ciclomes for ciclomes in dados_ciclomeses if ciclomes['atual'] == True];
    
    df_ciclomeses = pd.DataFrame(dados_ciclomeses)
    
    df_ciclomeses['mes_ano'] = df_ciclomeses['nome'] + ' de ' + df_ciclomeses['ano'].astype(str)
    
    mes_selecionado = st.selectbox('Selecione um mês:', df_ciclomeses['mes_ano'])
    
    df_filtrado = df_ciclomeses[df_ciclomeses['nome'] == mes_selecionado.split(sep=' ')[0]]
    shark_porcentagem = (df_filtrado['shark'].values[0]) * 100
    
    col1, col2, col3 = st.columns([2,1,1])

    # Exibindo as métricas lado a lado
    with col1:
        st.metric(label="Investimento", value=f"R${df_filtrado['investimento'].values[0]:,.2f}")
    with col2:
        st.metric(label="Dias", value=df_filtrado['dias'].values[0])
    with col3:
        st.metric(label="Shark - Dia", value=f"{shark_porcentagem}%")
    
    