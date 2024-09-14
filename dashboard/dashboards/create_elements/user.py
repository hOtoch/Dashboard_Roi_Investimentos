import streamlit as st
import pandas as pd
import api


def formulario_create_user(token, df_usuarios):
    # Simula um modal com uma chave única
    with st.form(key='teste'):
        st.write("Preencha os dados para criar um novo usuário:")
            
        nome = st.text_input('Nome')
        email = st.text_input('Email')
        senha = st.text_input('Senha', type='password')
        
        user_data = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "tipo_usuario": "comum"
        }
                
        submit_button = st.form_submit_button("Criar Usuário")
        
        if submit_button:
            if nome and email and senha:
                resposta = api.create_user(token, user_data)
                if "erro" not in resposta:    
                    dados_usuario = api.getall_users(token)
                    df_usuarios = pd.DataFrame(dados_usuario)
                    return True, df_usuarios
                else:
                    st.error(resposta['erro'])
                    return False, df_usuarios  
            else:
                st.error("Por favor, preencha todos os campos!")
                return False, df_usuarios 
            
    return False, df_usuarios  

def create_user_page(token, dados_usuario):
    df_usuarios = pd.DataFrame(dados_usuario)
   
    st.subheader('Criar Usuário')
    
    resposta_modal, df_usuarios_novo = formulario_create_user(token, df_usuarios)
    
        
    if resposta_modal:
        st.success("Usuário criado com sucesso!")
        df_usuarios = df_usuarios_novo
       
       