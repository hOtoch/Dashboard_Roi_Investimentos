import streamlit as st
import pandas as pd
import api

def formulario_edit_conta(token, conta_selecionada):
    with st.form(key=f'edit_form_conta_{conta_selecionada["id"]}'):
        st.write(f"Editando Conta: {conta_selecionada['nome']}")

        nome = st.text_input('Nome', value=conta_selecionada['nome'])
        deposito_inicial = st.number_input('Depósito Inicial', value=conta_selecionada['deposito_inicial'], format="%.2f")
        saldo_atual = st.number_input('Saldo Atual', value=conta_selecionada['saldo_atual'], format="%.2f")
        saques = st.number_input('Saques', value=conta_selecionada['saques'], format="%.2f")
        plano = st.selectbox('Plano', options=['Shrimp', 'Fish', 'Whale'], index=['Shrimp', 'Fish', 'Whale'].index(conta_selecionada['plano']))
        meses = st.selectbox('Meses', options=['Mensal', 'Trimestral', 'Anual'], index=['Mensal', 'Trimestral', 'Anual'].index(conta_selecionada['meses']))
        comissao = st.number_input('Comissão (%)', value=conta_selecionada['comissao'] * 100, format="%.2f")

       
        submit_button = st.form_submit_button("Salvar Alterações")

        if submit_button:
            
            dados_atualizados = {
                "nome": nome,
                "deposito_inicial": deposito_inicial,
                "saldo_atual": saldo_atual,
                "plano": plano,
                "meses": meses,
                "comissao": comissao / 100, 
                "saques": saques
            }
            resposta = api.edit_conta(token, int(conta_selecionada["id"]), dados_atualizados)
            if "erro" not in resposta:
                st.success("Conta atualizada com sucesso!")
                return True
            else:
                st.error(f"Erro: {resposta['erro']}")
    return False

def edit_conta_page(token, dados_contas):
   
    df_contas = pd.DataFrame(dados_contas)

    nomes_contas = df_contas['nome'].values
    conta_selecionada_nome = st.selectbox("Selecione uma conta para editar", options=nomes_contas)

    # Filtra o DataFrame para encontrar a conta selecionada
    conta_selecionada = df_contas[df_contas['nome'] == conta_selecionada_nome].iloc[0]

    if conta_selecionada is not None:
        st.divider()
        formulario_edit_conta(token, conta_selecionada)
        st.divider()

        if 'confirmando_remocao' not in st.session_state:
            st.session_state['confirmando_remocao'] = False

        if not st.session_state['confirmando_remocao']:
            remove_conta_button = st.button("Remover Conta")

            if remove_conta_button:
                st.session_state['confirmando_remocao'] = True

        if st.session_state['confirmando_remocao']:
            st.warning(f"Tem certeza que deseja remover esta conta?", icon="⚠️")
            col1, col2 = st.columns(2)

            with col1:
                confirma_remocao_button = st.button("Sim, remover")
            with col2:
                cancelar_remocao_button = st.button("Cancelar")

            if confirma_remocao_button:
                resposta = api.delete_conta(token, conta_selecionada['id'])

                if "erro" not in resposta:
                    st.success("Conta removida com sucesso!")
                    st.session_state['confirmando_remocao'] = False
                    dados_contas = api.get_contas(token)
                    df_contas = pd.DataFrame(dados_contas)
                    st.rerun()
                else:
                    st.error(f"Erro: {resposta['erro']}")
                    st.session_state['confirmando_remocao'] = False

            if cancelar_remocao_button:
                st.info("A remoção foi cancelada.")
                st.session_state['confirmando_remocao'] = False
                st.rerun()
