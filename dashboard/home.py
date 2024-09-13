import streamlit as st
import streamlit.components.v1 as components
import api
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import jwt
from dotenv import load_dotenv
from dashboards.dashboard_user import dashboard_user
from dashboards.dashboard_admin import dashboard_admin

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
    
def side_bar(token,dados_user):
    st.sidebar.write(":material/account_circle:", dados_user['nome'])
                
    st.sidebar.title("Menu")
    dashboard_selecionado = st.sidebar.selectbox("Escolha um dashboard",
                                                 ("🏠 Dashboard Inicial","📊 Dashboard do Usuário","🛠 Dasboard do Administrador"),
                                                 key="sidebar_dashboard_home_selectbox")
    
    st.session_state['dashboard_selecionado'] = dashboard_selecionado
    
    return dashboard_selecionado
   

def get_params():
    query_string = st.query_params
    token = query_string.get('token')
    return token

def dashboard_padrao(token, dados_ciclomeses):
    
    st.title("Dashboard Inicial")

    df_ciclomeses = pd.DataFrame(dados_ciclomeses)

    df_ciclomeses['mes_ano'] = df_ciclomeses['nome'] + ' de ' + df_ciclomeses['ano'].astype(str)
    df_ciclomeses = df_ciclomeses.sort_values(by="id", ascending=True)

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
        

    col4,col5,col6 = st.columns([2,2,1])

    porcentagem_alcancada = (df_filtrado['porcentagem_alcancado'].values[0]) * 100

    with col4:
        st.metric(label="Alcançado", value=f"R${df_filtrado['alcancado'].values[0]:,.2f}")
    with col5:
        st.metric(label="Projeção", value=f"R${df_filtrado['projecao'].values[0]:,.2f}")
    with col6:
        st.metric(label="Porcentagem Alcançada", value=f"{porcentagem_alcancada}%")
        
    try:
        dados_dias = api.get_dias(token, df_filtrado['id'].values[0])
        df_dias = pd.DataFrame(dados_dias)
        df_dias = df_dias.sort_values(by="id", ascending=True)
        df_dias['dia_id'] = range(1, len(df_dias) + 1)
        
        fig = px.line(df_dias, x="dia_id", y=["juros", "alcancado_dia"], 
                labels={"value": "Valores", "variable": "Métricas"},
                title="Juros e Valor Alcançado por Dia")

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)
    except Exception as e:
        st.error("O mês selecionado não possui dados dos dias relacionados a ele")
        
    alcancado = df_filtrado['alcancado'].values[0]
    restante_para_projecao = df_filtrado['projecao'].values[0] - alcancado

    # Dados para o gráfico de pizza
    valores = [alcancado, restante_para_projecao]
    labels = ["Alcançado", "Restante da Projeção"]

    # Criando o gráfico de pizza
    fig_pizza = px.pie(
        names=labels,
        values=valores,
        title="Progresso da Projeção Alcançada",
        hole=0.4  # Torna o gráfico um "donut"
    )

    fig_pizza.update_traces(
        textinfo='percent+value',  # Exibe label, porcentagem e valor
        textfont_size=15,                # Tamanho da fonte dos valores
        hoverinfo='label+percent+value'  # Informações ao passar o mouse
    )

    # Exibir o gráfico de pizza
    st.plotly_chart(fig_pizza)
        
        
    fig = px.bar(df_ciclomeses, x="mes_ano", y="investimento", title="Valor Investido por Mês")
    st.plotly_chart(fig)
        

    fig_waterfall = go.Figure(go.Waterfall(
        name="Valor Líquido", 
        orientation="v",
        x=df_ciclomeses['mes_ano'],  # Eixo X com meses
        y=df_ciclomeses['valor_liquido'],  # Valores líquidos
        textposition="outside",
        text=df_ciclomeses['valor_liquido'].map(lambda x: f"R${x:,.2f}"),
        connector={"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig_waterfall.update_layout(
        title="Valores Líquidos por Mês",
        showlegend=False
    )

    # Exibir o gráfico de cascata
    st.plotly_chart(fig_waterfall)

def main():
    token = get_params()
    
    image_path = os.path.join(os.getcwd(), "teste.png")
    # Background image CSS
    # page_bg_img = '''
    # <style>
    # [data-testid="stAppViewContainer"]{
    # background-color: #03fce8;
    # }
    
    # </style>
    # '''
    # st.markdown(page_bg_img, unsafe_allow_html=True)
    
    if token:
        payload = verificar_token(token)
        user_id = payload['sub']
        if payload:
            try:
                dados_user = api.get_user(token, user_id)             
            except Exception as e:
                st.error("Erro ao processar os dados do usuário.")
                st.error(str(e))
                
            dados_ciclomeses = api.get_ciclomeses(token)
            
            
            st.header(f"Bem-vindo, {dados_user['nome']}!")
            dashboard_selecionado = side_bar(token, dados_user)
            
            if dashboard_selecionado == "🏠 Dashboard Inicial":
                dashboard_padrao(token, dados_ciclomeses)
            elif dashboard_selecionado == "📊 Dashboard do Usuário":
                dashboard_user(token)
            elif dashboard_selecionado == "🛠 Dasboard do Administrador":
                dados_usuario = api.getall_users(token)
                dados_ciclomeses = api.get_ciclomeses(token)
                dados_contas = api.get_contas(token)
                dashboard_admin(token, dados_usuario, dados_ciclomeses, dados_contas)
            
        else:
            st.error("Autenticação falhou. Faça login novamente.")
    else:
        st.error("Acesso não autorizado. Por favor, faça login.")
        
    
    
if __name__ == "__main__":
    main()
    

   
        
    
    
    
    