import streamlit as st
import api
import pandas as pd

from dashboards.create_elements.user import create_user_page
from dashboards.create_elements.ciclomes import create_ciclomes_page
from dashboards.create_elements.conta import create_conta_page
from dashboards.edit_elements.user import edit_user_page
from dashboards.edit_elements.ciclomes import edit_ciclomes_page
from dashboards.edit_elements.conta import edit_conta_page

def control_session_state_admin(create_user_button, create_mes_button, create_conta_button, painel_user_button, painel_ciclomes_button, painel_conta_button, edit_user_button, edit_ciclomes_button, edit_conta_button):
    # Verifica se o estado já foi inicializado, se não, inicializa
    if 'painel_ciclomes' not in st.session_state:
        st.session_state['painel_ciclomes'] = False
        st.session_state['painel_user'] = False
        st.session_state['painel_conta'] = False
        st.session_state['create_user'] = False
        st.session_state['create_mes'] = False
        st.session_state['create_conta'] = False
        st.session_state['edit_user'] = False
        st.session_state['edit_ciclomes'] = False
        st.session_state['edit_conta'] = False
        st.session_state['painel'] = True

    # Mapeia cada botão a um estado correspondente
    estados = {
        'create_user': create_user_button,
        'create_mes': create_mes_button,
        'create_conta': create_conta_button,
        'painel_user': painel_user_button,
        'painel_ciclomes': painel_ciclomes_button,
        'painel_conta': painel_conta_button,
        'edit_user': edit_user_button,
        'edit_ciclomes': edit_ciclomes_button,
        'edit_conta': edit_conta_button
    }

    for estado, ativo in estados.items():
        if ativo:
            for key in estados.keys():
                st.session_state[key] = False

            st.session_state[estado] = True
            st.session_state['painel'] = False 

    # Manter o estado da página atual, sem redefinir quando a página recarrega
    for estado in estados.keys():
        if st.session_state.get(estado, False):
            return



def side_bar_admin(token):
    
    st.sidebar.divider()

    st.sidebar.write(":material/group:", "Usuários")
    
    col1, col2, colx = st.sidebar.columns([2,1,1])
    
    with col1:
        painel_user_button = st.button("Painel Usuários")
        
    with col2:
        create_user_button = st.button(":material/person_add:",help="Criar Usuário")
        
    with colx:
        edit_user_button = st.button(":material/person_edit:",help="Editar Usuário")
        
        
    st.sidebar.write(":material/calendar_month:", "Meses")
    
    col3, col4, coly = st.sidebar.columns([2,1,1])
    
    with col3:
        painel_ciclomes_button = st.button("Painel Meses")
        
    with col4:
        create_mes_button = st.button(":material/calendar_add_on:", help="Criar mês")
    
    with coly:
        edit_ciclomes_button = st.button(":material/edit_calendar:", help="Editar mês")
        
        
    st.sidebar.write(":material/list_alt:", "Contas")
    
    col5, col6, colz = st.sidebar.columns([2,1,1])
    
    with col5:
        painel_conta_button = st.button("Painel Contas")
        
    with col6:
        create_conta_button = st.button(":material/post_add:", help="Criar Conta")
        
    with colz:
        edit_conta_button = st.button(":material/edit_note:", help="Editar Conta")
        
    st.sidebar.divider()
    
    control_session_state_admin(create_user_button, create_mes_button, create_conta_button, painel_user_button, painel_ciclomes_button, painel_conta_button, edit_user_button, edit_ciclomes_button, edit_conta_button)
    # st.sidebar.write(st.session_state)
    st.sidebar.image("assets/logo.png", use_column_width='always',width=250)
    


def dashboard_admin(token, dados_usuario, dados_ciclomeses, dados_contas):
    st.title('Dashboard do Administrador')
    side_bar_admin(token)
    
    if 'create_user' in st.session_state and st.session_state['create_user']:
        create_user_page(token, dados_usuario)
        
    elif 'create_mes' in st.session_state and st.session_state['create_mes']:
        create_ciclomes_page(token, dados_ciclomeses)
    
    elif 'create_conta' in st.session_state and st.session_state['create_conta']:
        create_conta_page(token, dados_contas, dados_usuario)
    
    elif 'edit_user' in st.session_state and st.session_state['edit_user']:
        edit_user_page(token, dados_usuario)
        
    elif 'edit_ciclomes' in st.session_state and st.session_state['edit_ciclomes']:
        edit_ciclomes_page(token, dados_ciclomeses)
        
    elif 'edit_conta' in st.session_state and st.session_state['edit_conta']:
        edit_conta_page(token, dados_contas)
        
    elif 'painel' in st.session_state and st.session_state['painel']:
        
        st.subheader('Painel')
    
    
