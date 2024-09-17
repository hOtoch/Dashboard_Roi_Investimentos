import streamlit as st
import pandas as pd
import api

def formulario_edit_ciclomes(token, ciclomes_selecionado):
    # Exibe os dados do CicloMes selecionado para edição
    with st.form(key=f'edit_form_ciclomes_{ciclomes_selecionado["id"]}'):
        st.write(f"Editando o Mês: {ciclomes_selecionado['nome']}")

        # Campos editáveis
        nome = st.text_input('Nome', value=ciclomes_selecionado['nome'])
        ano = st.text_input('Ano', value=ciclomes_selecionado['ano'])
        investimento = st.number_input('Investimento', value=ciclomes_selecionado['investimento'], format="%.2f")
        dias = st.number_input('Dias', value=ciclomes_selecionado['dias'], min_value=1)
        shark = st.number_input('Shark (%)', value=ciclomes_selecionado['shark'] * 100, format="%.2f")
        valor_liquido = st.number_input('Valor Líquido', value=ciclomes_selecionado['valor_liquido'], format="%.2f")

        # Botão para submeter as alterações
        submit_button = st.form_submit_button("Salvar Alterações")

        if submit_button:
            # Prepara os dados atualizados
            dados_atualizados = {
                "nome": nome,
                "ano": ano,
                "investimento": investimento,
                "dias": dias,
                "shark": shark / 100,  # Convertendo de % para decimal
                "valor_liquido": valor_liquido
            }
            resposta = api.edit_ciclomes(token, ciclomes_selecionado["id"], dados_atualizados)
            if "erro" not in resposta:
                st.success("CicloMes atualizado com sucesso!")
                return True
            else:
                st.error(f"Erro: {resposta['erro']}")
    return False

def formulario_edit_dia(token, dia_selecionado):
    
    # Campo editável para o valor de 'alcancado_dia'
    alcancado_dia = st.number_input('Alcançado Dia', value=dia_selecionado['alcancado_dia'], format="%.2f")
    
    dia_data = {
        "alcancado_dia": alcancado_dia
    }
    
    # Botão para salvar as alterações
    submit_button = st.button("Salvar Alterações")
 
    # Verifica se o botão foi clicado e realiza a ação
    if submit_button:
        resposta = api.edit_dia(token, int(dia_selecionado['id']), dia_data)
        
        if 'erro' not in "resposta":
            st.success(f"Dia atualizado com sucesso!")
        else:
            st.error(f"Erro ao atualizar o dia, error: {resposta['erro']}")
            
def edit_ciclomes_page(token, dados_ciclomes):
    
    if not dados_ciclomes:
        st.warning("Nenhum Mês cadastrado.")
        return

    df_ciclomes = pd.DataFrame(dados_ciclomes)

    nomes_ciclomes = df_ciclomes['nome'].values
    ciclomes_selecionado_nome = st.selectbox("Selecione um Mês para editar", options=nomes_ciclomes)

    ciclomes_selecionado = df_ciclomes[df_ciclomes['nome'] == ciclomes_selecionado_nome].iloc[0]

    if ciclomes_selecionado is not None:
        st.divider()
        formulario_edit_ciclomes(token, ciclomes_selecionado)
        st.divider()
        
        dados_dias = api.get_dias(token, ciclomes_selecionado['id'])

        if dados_dias:
        
            df_dias = pd.DataFrame(dados_dias).sort_values(by='id', ascending=True).reset_index(drop=True)
            
            df_dias['dia_num'] = range(1, len(df_dias) + 1)
            
            dia_selecionado = st.selectbox("Selecione um dia para editar", options=df_dias['dia_num'].values)
            
            formulario_edit_dia(token, df_dias[df_dias['dia_num'] == dia_selecionado].iloc[0])
            
            st.divider()
            
        if ciclomes_selecionado['atual'] == False:
            ativar_mes_button = st.button("Ativar Mês")
            
            if ativar_mes_button:
                resposta = api.ativar_ciclomes(token, ciclomes_selecionado['id'])
                
                if "erro" not in resposta:
                    st.success("Mês ativado com sucesso!")
                    dados_ciclomes = api.get_ciclomeses(token)
                    df_ciclomes = pd.DataFrame(dados_ciclomes)
                    st.rerun()
                else:
                    st.error(f"Erro: {resposta['erro']}")

        if 'confirmando_remocao_mes' not in st.session_state:
            st.session_state['confirmando_remocao_mes'] = False

        if not st.session_state['confirmando_remocao_mes']:
            remove_ciclomes_button = st.button("Remover Mes")

            if remove_ciclomes_button:
                st.session_state['confirmando_remocao_mes'] = True

        if st.session_state['confirmando_remocao_mes']:
            st.warning(f"Tem certeza que deseja remover este Mes?", icon="⚠️")
            col1, col2 = st.columns(2)

            with col1:
                confirma_remocao_button = st.button("Sim, remover")
            with col2:
                cancelar_remocao_button = st.button("Cancelar")

            if confirma_remocao_button:
                resposta = api.delete_ciclomes(token, ciclomes_selecionado['id'])

                if "erro" not in resposta:
                    st.success("CicloMes removido com sucesso!")
                    st.session_state['confirmando_remocao_mes'] = False
                    dados_ciclomes = api.get_ciclomeses(token)
                    df_ciclomes = pd.DataFrame(dados_ciclomes)
                    st.rerun()
                else:
                    st.error(f"Erro: {resposta['erro']}")
                    st.session_state['confirmando_remocao_mes'] = False

            if cancelar_remocao_button:
                st.info("A remoção foi cancelada.")
                st.session_state['confirmando_remocao_mes'] = False
                st.rerun()
                
