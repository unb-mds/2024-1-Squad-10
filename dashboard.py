



########################## vers 5
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('contratos_ordenados_completo.csv')
    return df

df_ordenado = load_data()
df_ordenado = df_ordenado.sort_values("Ano da Compra")
anos_unicos = df_ordenado['Ano da Compra'].unique()
anos_unicos = ['Todos'] + list(anos_unicos)

with st.container():
    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
    st.write('Informações sobre contratos')
    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
    st.write('---')

ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)

if ano != 'Todos':
    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
else:
    df_filtered = df_ordenado.copy()

orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)

if orgaos_unicos != 'Todos':
    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]

df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Empresa Contratada', 'Objeto da Compra'])['Valor Total Homologado'].sum().reset_index()
df_filtered_gov_grouped_chart2 = df_filtered.groupby(['Órgão Entidade'])['Valor Total Homologado'].sum().reset_index()

#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade',  'Objeto da Compra'])['Valor Total Homologado'].sum().reset_index()
df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Total Homologado', ascending=False)
df_filtered_gov_grouped_chart2=df_filtered_gov_grouped_chart2.sort_values(by='Valor Total Homologado', ascending=False)
palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'")

if palavra_filtro:
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]

orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
contrato_orgao_opcoes_chart = ['Todos'] + list(df_filtered_gov_grouped_chart2['Órgão Entidade'].unique())


contrato_orgao_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nome da Empresa Contratada", contrato_orgao_opcoes)
if contrato_orgao_opcoes_filtro != 'Todos':
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Empresa Contratada'] == contrato_orgao_opcoes_filtro]

valor_min = int(df_filtered_gov_ordenado['Valor Total Homologado'].min())
valor_max = int(df_filtered_gov_ordenado['Valor Total Homologado'].max())

if valor_min != valor_max:
    valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', valor_min, valor_max, (valor_min, valor_max), step=100000)
    df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Total Homologado'] >= valor_intervalo[0]) & (df_filtered_gov_ordenado['Valor Total Homologado'] <= valor_intervalo[1])]
    df_filtered_gov_grouped_chart2= df_filtered_gov_grouped_chart2[(df_filtered_gov_grouped_chart2['Valor Total Homologado'] >= valor_intervalo[0]) & (df_filtered_gov_grouped_chart2['Valor Total Homologado'] <= valor_intervalo[1])]
# Controle de paginação
total_barras = len(df_filtered_gov_ordenado)
barras_por_pagina = 10
num_paginas = total_barras // barras_por_pagina + (total_barras % barras_por_pagina > 0)

pagina = st.sidebar.number_input("Página", min_value=1, max_value=num_paginas, value=1)

inicio = (pagina - 1) * barras_por_pagina
fim = inicio + barras_por_pagina

df_paginado = df_filtered_gov_ordenado.iloc[inicio:fim]
df_paginado=df_paginado.sort_values(by='Valor Total Homologado', ascending=False)
#
df_paginado_chart2=df_filtered_gov_grouped_chart2.iloc[inicio:fim]
df_paginado_chart2 = df_paginado_chart2.groupby(['Órgão Entidade'])['Valor Total Homologado'].sum().reset_index()
df_paginado_chart2=df_paginado_chart2.sort_values(by='Valor Total Homologado', ascending=False)

col2 = st.columns(1)[0]

fig_orgao1 = px.bar(df_paginado_chart2, x='Órgão Entidade', y='Valor Total Homologado', title='Órgão Campeão')
fig_orgao1.update_xaxes(title_text='Órgão Contratante')
fig_orgao1.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
fig_orgao1.update_layout(height=800)
col2.plotly_chart(fig_orgao1, use_container_width=True)

col1 = st.columns(1)[0]

fig_orgao = px.bar(df_paginado, x='Órgão Entidade', y='Valor Total Homologado', color='Empresa Contratada', title='Contrato Campeão')
fig_orgao.update_xaxes(title_text='Órgão Contratante')
fig_orgao.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
fig_orgao.update_layout(height=800)
col1.plotly_chart(fig_orgao, use_container_width=True)



with st.container():
    st.write('Dados Compilados')
    st.write(df_filtered_gov_ordenado)
    st.write('---')


