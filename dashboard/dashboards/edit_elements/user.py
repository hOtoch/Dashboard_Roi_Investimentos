import streamlit as st
import pandas as pd
import api

def formulario_edit_user(token, usuario_selecionado):
    # Exibe os dados do usuário selecionado para edição
    with st.form(key=f'edit_form_{usuario_selecionado["id"]}'):
        st.write(f"Editando usuário: {usuario_selecionado['nome']}")

        # Campos editáveis
        nome = st.text_input('Nome', value=usuario_selecionado['nome'])
        email = st.text_input('Email', value=usuario_selecionado['email'])
        tipo_usuario = st.selectbox('Tipo de Usuário', options=['comum', 'admin'], index=0 if usuario_selecionado['tipo_usuario'] == 'comum' else 1)

        # Botão para submeter as alterações
        submit_button = st.form_submit_button("Salvar Alterações")

        if submit_button:
            # Prepara os dados atualizados
            dados_atualizados = {
                "nome": nome,
                "email": email,
                "tipo_usuario": tipo_usuario
            }
            resposta = api.edit_user(token, usuario_selecionado["id"], dados_atualizados)
            if "erro" not in resposta:
                st.success("Usuário atualizado com sucesso!")
                return True
            else:
                st.error(f"Erro: {resposta['erro']}")
    return False

def edit_user_page(token, dados_usuario):
    # DataFrame dos usuários
    df_usuarios = pd.DataFrame(dados_usuario)

    # Selectbox para selecionar o usuário a ser editado
    nomes_usuarios = df_usuarios['nome'].values
    usuario_selecionado_nome = st.selectbox("Selecione um usuário para editar", options=nomes_usuarios)

    # Filtra o DataFrame para encontrar o usuário selecionado
    usuario_selecionado = df_usuarios[df_usuarios['nome'] == usuario_selecionado_nome].iloc[0]

    # Exibe o formulário para edição do usuário selecionado
    if usuario_selecionado is not None:
        st.divider()
        formulario_edit_user(token, usuario_selecionado)
        st.divider()
        
        if 'confirmando_remocao_user' not in st.session_state:
            st.session_state['confirmando_remocao_user'] = False
    
        if not st.session_state['confirmando_remocao_user']:
            remove_user_button = st.button("Remover Usuário")
            
            if remove_user_button:
                st.session_state['confirmando_remocao_user'] = True
        
        if st.session_state['confirmando_remocao_user']:
            st.warning(f"Tem certeza que deseja remover este usuário?", icon="⚠️")
            col1, col2 = st.columns(2)
            
            with col1:
                confirma_remocao_button = st.button("Sim, remover")
            with col2:
                cancelar_remocao_button = st.button("Cancelar")
            
            if confirma_remocao_button:
                resposta = api.delete_user(token, usuario_selecionado['id'])

                if "erro" not in resposta:
                    st.success("Usuário removido com sucesso!")
                    st.session_state['confirmando_remocao_user'] = False
                    dados_usuario = api.getall_users(token)
                    df_usuarios = pd.DataFrame(dados_usuario)
                    st.rerun()
                else:
                    st.error(f"Erro: {resposta['erro']}")
                    st.session_state['confirmando_remocao_user'] = False
            
            if cancelar_remocao_button:
                st.info("A remoção foi cancelada.")
                st.session_state['confirmando_remocao_user'] = False
        
