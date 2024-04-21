#https://www.youtube.com/watch?v=P6E_Kts9pxE - ajuda

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

df_ordenado = pd.read_csv('contratos_ordenados.csv')
df_ordenado = df_ordenado.sort_values("anoCompra")
anos_unicos = df_ordenado['anoCompra'].unique()
anos_unicos = ['Todos'] + list(anos_unicos)  # Adicionando a opção "Todos" à lista de anos únicos

ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)

if ano != 'Todos':
    df_filtered = df_ordenado[df_ordenado['anoCompra'] == ano]
else:
    df_filtered = df_ordenado.copy()  # Se 'Todos' for selecionado, mostra todos os dados

anofundacao_unicos = ['Todos'] + list(df_filtered['anodefundacao'].unique())  # Adicionando a opção "Todos" à lista de anos de fundação únicos
anofundacao = st.sidebar.selectbox("Ano de Fundação", anofundacao_unicos)

if anofundacao != 'Todos':
    df_filtered = df_filtered[df_filtered['anodefundacao'] == anofundacao]    

df_filtered_sellers_grouped = df_filtered.groupby(['razaosocialFornecedor','razaoSocial','objetoCompra'])['valorTotalHomologado'].sum().reset_index()
df_filtered_sellers_ordenado = df_filtered_sellers_grouped.sort_values(by='valorTotalHomologado', ascending=False)

df_filtered_gov_grouped = df_filtered.groupby(['razaoSocial','razaosocialFornecedor','objetoCompra'])['valorTotalHomologado'].sum().reset_index()
df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='valorTotalHomologado', ascending=False)

# Adicionar campo de texto para filtrar por palavra na coluna 'objetoCompra'
palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'objetoCompra'")

# Filtrar o DataFrame se uma palavra foi digitada
if palavra_filtro:
    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['objetoCompra'].str.contains(palavra_filtro, case=False)]
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['objetoCompra'].str.contains(palavra_filtro, case=False)]

# Adicionar filtros para 'razaoSocial' e 'razaosocialFornecedor'
razao_social_opcoes = ['Todos'] + list(df_filtered_sellers_ordenado['razaoSocial'].unique())
razaosocial_fornecedor_opcoes = ['Todos'] + list(df_filtered_sellers_ordenado['razaosocialFornecedor'].unique())

razaosocial_filtro = st.sidebar.selectbox("Filtrar por 'razaoSocial'", razao_social_opcoes)
if razaosocial_filtro != 'Todos':
    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['razaoSocial'] == razaosocial_filtro]
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['razaoSocial'] == razaosocial_filtro]

razaosocial_fornecedor_filtro = st.sidebar.selectbox("Filtrar por 'razaosocialFornecedor'", razaosocial_fornecedor_opcoes)
if razaosocial_fornecedor_filtro != 'Todos':
    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['razaosocialFornecedor'] == razaosocial_fornecedor_filtro]
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['razaosocialFornecedor'] == razaosocial_fornecedor_filtro]

col1 = st.columns(1)[0]
col3, col4, col5 = st.columns(3)

fig_campea = px.bar(df_filtered_sellers_ordenado, x='razaosocialFornecedor', y='valorTotalHomologado',color='razaoSocial' ,title='Empresas campeãs')
col1.plotly_chart(fig_campea,use_container_width=True)

fig_orgao = px.bar(df_filtered_gov_ordenado, x='razaoSocial', y='valorTotalHomologado',color='razaosocialFornecedor',title='Órgão Campeão',)
fig_orgao.update_layout(height=800)  # Definindo a altura do gráfico
col1.plotly_chart(fig_orgao,use_container_width=True)

st.write(df_filtered_sellers_ordenado)
st.write(df_filtered_gov_ordenado)




