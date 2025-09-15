
# Importa as bibliotecas necessárias
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import datetime as dt

# ---
# 1. Configuração Inicial e Autenticação
# ---

# Título do aplicativo
st.title('SaaS de Gestão Financeira para Empresas')

# ---
# Seção de Autenticação (Simulada)
# ---
def login_form():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Entrar"):
        # Lógica de autenticação (poderia ser integrada com um banco de dados real)
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.sidebar.success(f"Bem-vindo, {username}!")
        else:
            st.sidebar.error("Usuário ou senha incorretos.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_form()
    st.stop()

# ---
# 2. Estrutura de Dados
# ---

# Inicialização dos dados em estado de sessão (simulando um banco de dados)
if 'movimentacoes' not in st.session_state:
    st.session_state['movimentacoes'] = pd.DataFrame(columns=[
        'Data', 'Plano de Contas', 'Sub Plano de Contas', 'Valor', 'Descrição', 
        'Forma de Pagamento', 'Status', 'ID'
    ])

if 'planos_contas' not in st.session_state:
    st.session_state['planos_contas'] = {
        'Receitas': ['Vendas de Produtos', 'Serviços Prestados', 'Juros Recebidos'],
        'Despesas': ['Salários', 'Aluguel', 'Marketing', 'Materiais de Escritório'],
        'Investimentos': ['Ações', 'Fundos Imobiliários'],
        'Outros': ['Transferências']
    }

# ---
# 3. Módulos do Aplicativo
# ---

# Menu de navegação na barra lateral
st.sidebar.header("Menu")
page = st.sidebar.radio("Navegar", ["Lançamentos Manuais", "Planos de Contas", "Resultados e Análises"])

# ---
# Módulo de Planos de Contas
# ---
if page == "Planos de Contas":
    st.header('Cadastro de Categorias (Planos de Contas)')
    st.markdown("---")
    
    # Exibe os planos de contas existentes
    st.subheader('Planos de Contas Existentes')
    for plano, sub_planos in st.session_state['planos_contas'].items():
        st.write(f"**{plano}**")
        st.write(f"  - {', '.join(sub_planos)}")
    
    st.markdown("---")
    
    # Formulário para adicionar novo plano de contas
    with st.expander("Adicionar Novo Plano de Contas"):
        novo_plano = st.text_input('Nome do Plano de Contas (Nível 1)')
        novo_sub_plano = st.text_input('Nome do Sub Plano de Contas (Nível 2)')
        
        if st.button('Adicionar Plano'):
            if novo_plano and novo_sub_plano:
                if novo_plano not in st.session_state['planos_contas']:
                    st.session_state['planos_contas'][novo_plano] = []
                
                if novo_sub_plano not in st.session_state['planos_contas'][novo_plano]:
                    st.session_state['planos_contas'][novo_plano].append(novo_sub_plano)
                    st.success(f'"{novo_sub_plano}" adicionado a "{novo_plano}".')
                else:
                    st.warning('Este sub plano já existe.')
            else:
                st.error('Por favor, preencha todos os campos.')

# ---
# Módulo de Lançamentos Manuais
# ---
elif page == "Lançamentos Manuais":
    st.header('Lançamentos de Movimentações Financeiras')
    st.markdown("---")

    # ---
    # Sub-Módulo de Lançamento Manual
    # ---
    st.subheader('Lançamento Manual')
    with st.form("manual_entry_form"):
        data = st.date_input('Data', dt.date.today())
        tipo_mov = st.radio('Tipo de Movimentação', ['Entrada (Receita)', 'Saída (Despesa)'])
        plano_conta_selecionado = st.selectbox('Plano de Contas', st.session_state['planos_contas'].keys())
        sub_plano_contas = st.session_state['planos_contas'].get(plano_conta_selecionado, [])
        sub_plano_selecionado = st.selectbox('Sub Plano de Contas', sub_plano_contas)
        valor = st.number_input('Valor', min_value=0.01)
        descricao = st.text_area('Descrição')
        forma_pagamento = st.selectbox('Forma de Pagamento', ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'Transferência Bancária', 'PIX', 'Boleto'])
        status = st.selectbox('Status', ['Pendente', 'Concluído', 'Cancelado'])
        
        submitted = st.form_submit_button("Salvar Lançamento")
        if submitted:
            novo_lancamento = {
                'Data': data,
                'Plano de Contas': plano_conta_selecionado,
                'Sub Plano de Contas': sub_plano_selecionado,
                'Valor': valor if tipo_mov == 'Entrada (Receita)' else -valor,
                'Descrição': descricao,
                'Forma de Pagamento': forma_pagamento,
                'Status': status,
                'ID': len(st.session_state['movimentacoes']) + 1
            }
            novo_df = pd.DataFrame([novo_lancamento])
            st.session_state['movimentacoes'] = pd.concat([st.session_state['movimentacoes'], novo_df], ignore_index=True)
            st.success('Lançamento salvo com sucesso!')
            st.experimental_rerun()
    
    st.markdown("---")
    
    # ---
    # Sub-Módulo de Importação de OFX
    # ---
    st.subheader('Importar Arquivo OFX')
    st.info("A importação de OFX simplifica o registro de transações bancárias, evitando a digitação manual.")
    
    uploaded_file = st.file_uploader("Escolha um arquivo OFX", type="ofx")
    
    if uploaded_file:
        try:
            # Lógica para parsing de OFX
            # Nota: A biblioteca 'ofxtools' é recomendada, mas precisaria ser instalada
            # e configurada no ambiente do Abacus.AI. Este é um exemplo conceitual.
            # import ofxtools
            # ofx = ofxtools.parse(uploaded_file)
            # transactions = ofx.statements[0].transactions
            
            # --- Simulação de dados OFX para demonstração ---
            st.warning("Simulando a importação do arquivo OFX.")
            
            ofx_data = [
                {'Data': '2025-09-10', 'Descricao': 'Supermercado XYZ', 'Valor': -250.75},
                {'Data': '2025-09-11', 'Descricao': 'Salário Mensal', 'Valor': 5000.00},
                {'Data': '2025-09-12', 'Descricao': 'Conta de Luz', 'Valor': -180.50}
            ]
            
            df_ofx = pd.DataFrame(ofx_data)
            st.write("Dados extraídos do OFX:")
            st.dataframe(df_ofx)
            
            st.success("Arquivo OFX processado. Use a IA para categorizar os lançamentos!")
            
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

# ---
# Módulo de Resultados e Análises
# ---
elif page == "Resultados e Análises":
    st.header('Análise de Resultados')
    st.markdown("---")
    
    if st.session_state['movimentacoes'].empty:
        st.info("Não há lançamentos para exibir. Adicione movimentações para ver os resultados.")
    else:
        df = st.session_state['movimentacoes'].copy()
        df['Data'] = pd.to_datetime(df['Data'])
        df['Mês/Ano'] = df['Data'].dt.strftime('%Y-%m')

        # Filtros
        st.subheader('Filtros')
        col1, col2, col3 = st.columns(3)
        with col1:
            data_inicio = st.date_input('Data de Início', df['Data'].min())
        with col2:
            data_fim = st.date_input('Data de Fim', df['Data'].max())
        with col3:
            filtros_selecionados = st.multiselect(
                'Filtrar por', 
                options=['Plano de Contas', 'Forma de Pagamento', 'Status']
            )

        # Aplica os filtros de data
        df_filtrado = df[(df['Data'].dt.date >= data_inicio) & (df['Data'].dt.date <= data_fim)]

        # Filtros dinâmicos
        if 'Plano de Contas' in filtros_selecionados:
            plano_selecionado = st.selectbox('Selecione o Plano de Contas', df_filtrado['Plano de Contas'].unique())
            df_filtrado = df_filtrado[df_filtrado['Plano de Contas'] == plano_selecionado]
        
        if 'Forma de Pagamento' in filtros_selecionados:
            forma_pag_selecionada = st.selectbox('Selecione a Forma de Pagamento', df_filtrado['Forma de Pagamento'].unique())
            df_filtrado = df_filtrado[df_filtrado['Forma de Pagamento'] == forma_pag_selecionada]
        
        if 'Status' in filtros_selecionados:
            status_selecionado = st.selectbox('Selecione o Status', df_filtrado['Status'].unique())
            df_filtrado = df_filtrado[df_filtrado['Status'] == status_selecionado]

        st.markdown("---")
        
        # ---
        # Gráficos e Insights
        # ---
        st.subheader('Gráficos de Análise')
        
        if not df_filtrado.empty:
            # Gráfico de Receitas vs. Despesas por Mês
            df_agregado = df_filtrado.groupby(['Mês/Ano', 'Plano de Contas']).agg(
                Total=('Valor', 'sum')
            ).reset_index()

            fig_bar = px.bar(
                df_agregado,
                x='Mês/Ano',
                y='Total',
                color='Plano de Contas',
                title='Movimentação Financeira por Mês',
                labels={'Total': 'Valor (R$)', 'Mês/Ano': 'Período'},
                text='Total'
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)

            # Gráfico de Pizza por Plano de Contas
            st.markdown("---")
            st.subheader('Distribuição por Plano de Contas')
            df_pizza = df_filtrado.groupby('Plano de Contas').agg(
                Total=('Valor', 'sum')
            ).reset_index()

            fig_pie = px.pie(
                df_pizza,
                values='Total',
                names='Plano de Contas',
                title='Distribuição de Receitas/Despesas',
                hole=0.4 # Gráfico de rosca
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Tabela detalhada dos lançamentos
            st.markdown("---")
            st.subheader('Detalhes dos Lançamentos')
            st.dataframe(df_filtrado.sort_values(by='Data', ascending=False))

        else:
            st.info("Nenhum dado encontrado para os filtros selecionados.")
