import streamlit as st
import pandas as pd
import plotly.express as px
import json
import unidecode
import locale

# Configura a localização para 'pt_BR' para utilizar o formato de números brasileiros
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title="Gastos de Dispensa por Órgão", layout='wide')

@st.cache_data
def load_csv_data():
    df = pd.read_csv('contratos_ordenados_completo.csv')
    df_sem_duplicatas = df.drop_duplicates()
    df = df_sem_duplicatas.sort_values("Valor Total Homologado",ascending=False)
    return df

@st.cache_data
def load_json_data():
    with open('contratos_OFICIAL.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    rows = [
        {
            "Ano da Compra": entry.get("Ano da Compra"),
            "Órgão Entidade": entry.get("Órgão Entidade"),
            "Valor Total Homologado": entry.get("Valor Total Homologado", 0)
        }
        for entry in data
    ]
    df = pd.DataFrame(rows)
    df['Órgão Entidade Normalizado'] = df['Órgão Entidade'].apply(lambda x: unidecode.unidecode(x).lower())
    return df

df_ordenado = load_csv_data()
anos_unicos = ['Todos'] + list(df_ordenado['Ano da Compra'].unique())

# Layout e filtros
with st.container():
    st.subheader("PAINEL INTERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
    st.write('Informações sobre contratos de Dispensa de Licitação')
    st.write("Quer saber mais sobre nosso projeto? [clique aqui](https://unb-mds.github.io/2024-1-Squad-10/)")
    st.write('---')

#filtra por ano
ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano] if ano != 'Todos' else df_ordenado

#Filtra por órgão
orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)

if orgaos_unicos != 'Todos':
    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]

#Filtra por palavra no objeto da compra
palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'. Ex: coffee break, lanche, abastecimento e etc.")
if palavra_filtro:
    df_filtered = df_filtered[df_filtered['Objeto da Compra'].str.contains(palavra_filtro, case=False)]


#Filtra pelo nome da empresa contratada
empresa_opcoes = ['Todos'] + list(df_filtered['Empresa Contratada'].unique())
contrato_empresa_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nome da Empresa Contratada", empresa_opcoes)
if contrato_empresa_opcoes_filtro != 'Todos':
    df_filtered = df_filtered[df_filtered['Empresa Contratada'] == contrato_empresa_opcoes_filtro]


#Filtra pelo valor da compra
valor_min = 0
valor_max = int(df_filtered['Valor Recebido'].max() + 1000000)
valor_min_selecionado = st.sidebar.number_input('De:', min_value=valor_min, max_value=valor_max, value=valor_min)
valor_max_selecionado = st.sidebar.number_input('Até:', min_value=valor_min, max_value=valor_max, value=valor_max)  # Formata como número inteiro)

df_filtered = df_filtered[(df_filtered['Valor Recebido'] >= valor_min_selecionado) & (df_filtered['Valor Recebido'] <= valor_max_selecionado)]

# Controle de paginação
total_barras = len(df_filtered)
barras_por_pagina = 40
num_paginas = total_barras // barras_por_pagina + (total_barras % barras_por_pagina > 0)
pagina = st.sidebar.number_input(f"Página ... de {num_paginas}", min_value=1, max_value=num_paginas, value=1)

inicio = (pagina - 1) * barras_por_pagina
fim = inicio + barras_por_pagina
df_paginado = df_filtered.iloc[inicio:fim].sort_values(by='Valor Recebido', ascending=False)

# Adicionar a coluna 'Órgão Entidade + Código' para o gráfico
df_paginado['Órgão Entidade + Código'] = df_paginado['Órgão Entidade'] + ' ' + df_paginado['Código']

# Gráficos
col2 = st.columns(1)[0]
col1 = st.columns(1)[0]
#col1, col2 = st.columns(2)

# Gráfico 1

df_paginado_sorted = df_paginado.sort_values(by='Valor Recebido', ascending=False)

fig_orgao = px.bar(
    df_paginado_sorted,
    x='Órgão Entidade + Código',
    #x='Órgão Entidade',
    y='Valor Recebido',
    color='Código',
    title='Contratos Campeões'
)
fig_orgao.update_xaxes(title_text='Órgão Contratante e Contrato')
fig_orgao.update_yaxes(title_text='Valores pagos por órgão e Contrato')
fig_orgao.update_layout(height=800)
col1.plotly_chart(fig_orgao, use_container_width=True)



# Gráfico 2
df_grouped_chart2 = df_filtered.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index().sort_values(by='Valor Recebido', ascending=False)
# Selecionar apenas os 20 primeiros
df_grouped_chart2_top20 = df_grouped_chart2.head(15)
fig_orgao2 = px.bar(df_grouped_chart2_top20, x='Órgão Entidade', y='Valor Recebido', color='Órgão Entidade', title='Órgãos Campeões')
fig_orgao2.update_xaxes(title_text='Órgão Contratante')
fig_orgao2.update_yaxes(title_text='Valores pagos por órgão')
fig_orgao2.update_layout(height=800)
col2.plotly_chart(fig_orgao2, use_container_width=True)

# Dados filtrados
with st.container():
    st.write('Dados Compilados')
    st.write(df_filtered)
    st.write('---')

# Dados JSON
df_json = load_json_data()
search_term = st.text_input("Digite o nome do Órgão")

if search_term:
    search_term_normalized = unidecode.unidecode(search_term).lower()
    matched_organs = df_json[df_json['Órgão Entidade Normalizado'].str.contains(search_term_normalized)]['Órgão Entidade'].unique()
    
    if matched_organs:
        selected_organ = st.selectbox("Selecione um órgão", matched_organs)
        if selected_organ:
            df_filtered_json = df_json[df_json['Órgão Entidade'] == selected_organ]
            df_grouped = df_filtered_json.groupby(['Ano da Compra', 'Órgão Entidade'])['Valor Total Homologado'].sum().reset_index()

            fig_timeline = px.line(df_grouped, x='Ano da Compra', y='Valor Total Homologado', color='Órgão Entidade', title='Evolução dos Gastos Anuais por Órgão')
            st.plotly_chart(fig_timeline, use_container_width=True)

            with st.container():
                st.write(f'<h3><u style="color:white;">Valor anual gasto em dispensa de licitação por:</u> {selected_organ}</h3>', unsafe_allow_html=True)
                for _, row in df_grouped.iterrows():
                    st.markdown(f"<p style='font-size:16px;'><u style='color:white;'>Ano {row['Ano da Compra']}:</u> R$ {row['Valor Total Homologado']:,.2f}</p>", unsafe_allow_html=True)
                st.write("A primeira versão do Portal Nacional de Contratações Públicas [(PNCP)](https://www.gov.br/pncp/pt-br) somente foi lançada em Agosto de 2021 portanto, os dados desse ano podem estar incompletos.")
                st.write('<hr>', unsafe_allow_html=True)
    else:
        st.write("Nenhum órgão encontrado com esse termo de pesquisa.")
else:
    st.write("Digite o nome de um órgão para começar a pesquisa.")


#### versão 02 
#'''
#import streamlit as st
#import pandas as pd
#import plotly.express as px
#import json
#import unidecode
#
#st.set_page_config(page_title="Gastos de Dispensa por Órgão", layout='wide')
#
#@st.cache_data
#def load_data():
#    df = pd.read_csv('contratos_ordenados_completo.csv')
#    return df
#
#df_ordenado = load_data()
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)
#
#with st.container():
#    st.subheader("PAINEL INTERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](https://unb-mds.github.io/2024-1-Squad-10/)")
#    st.write('---')
#
#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)  # Adicionando a opção "Todos" à lista de anos únicos
#
#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
#
#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
#else:
#    df_filtered = df_ordenado.copy()
#
#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)
#
#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]
#
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Código', 'Empresa Contratada', 'CNPJ', 'Objeto da Compra'])['Valor Recebido'].sum().reset_index()
#df_filtered_gov_grouped_chart2 = df_filtered.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Recebido', ascending=False)
#df_filtered_gov_grouped_chart2 = df_filtered_gov_grouped_chart2.sort_values(by='Valor Recebido', ascending=False)
#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'. Ex: coffee break, lanche, abastecimento, etc")
#
##adicionado para inserir uma segunda tabela ao final do dashboard - impacta o 2º container
#df_filtered_gov_ordenado1 = df_filtered_gov_ordenado
#
#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#    df_filtered_gov_ordenado1 = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes_chart = ['Todos'] + list(df_filtered_gov_grouped_chart2['Órgão Entidade'].unique())
#
#empresa_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Empresa Contratada'].unique())
#
#contrato_empresa_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nome da Empresa Contratada", empresa_opcoes)
#if contrato_empresa_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Empresa Contratada'] == contrato_empresa_opcoes_filtro]
#
#valor_min = 0
#valor_max = int(df_filtered_gov_grouped_chart2['Valor Recebido'].max() + 1000000)
#
## Criar caixas de entrada de números para os valores mínimo e máximo
#valor_min_selecionado = st.sidebar.number_input('De:', min_value=valor_min, max_value=valor_max, value=valor_min)
#valor_max_selecionado = st.sidebar.number_input('Até:', min_value=valor_min, max_value=valor_max, value=valor_max)
#
## Filtrar DataFrame com base nos valores selecionados
#df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Recebido'] >= valor_min_selecionado) & (df_filtered_gov_ordenado['Valor Recebido'] <= valor_max_selecionado)]
#df_filtered_gov_grouped_chart2 = df_filtered_gov_grouped_chart2[(df_filtered_gov_grouped_chart2['Valor Recebido'] >= valor_min_selecionado) & (df_filtered_gov_grouped_chart2['Valor Recebido'] <= valor_max_selecionado)]
#
## Controle de paginação
#total_barras = len(df_filtered_gov_ordenado)
#barras_por_pagina = 10
#num_paginas = total_barras // barras_por_pagina + (total_barras % barras_por_pagina > 0)
#
#pagina = st.sidebar.number_input("Página", min_value=1, max_value=num_paginas, value=1)
#
#inicio = (pagina - 1) * barras_por_pagina
#fim = inicio + barras_por_pagina
#
#df_paginado = df_filtered_gov_ordenado.iloc[inicio:fim]
#df_paginado = df_paginado.sort_values(by='Valor Recebido', ascending=False)
#
#df_paginado_chart2 = df_filtered_gov_grouped_chart2.iloc[inicio:fim]
#df_paginado_chart2 = df_paginado_chart2.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
#df_paginado_chart2 = df_paginado_chart2.sort_values(by='Valor Recebido', ascending=False)
#
#col2 = st.columns(1)[0]
#
#fig_orgao2 = px.bar(df_paginado_chart2, x='Órgão Entidade', y='Valor Recebido', color='Órgão Entidade', title='Órgão Campeão')
#fig_orgao2.update_xaxes(title_text='Órgão Contratante')
#fig_orgao2.update_yaxes(title_text='Valores pagos por órgão')
#fig_orgao2.update_layout(height=800)
#col2.plotly_chart(fig_orgao2, use_container_width=True)
#
#col1 = st.columns(1)[0]
#
#df_paginado['Órgão Entidade + Código'] = df_paginado['Órgão Entidade'] + ' ' + df_paginado['Código']
#
#fig_orgao = px.bar(
#    df_paginado,
#    x='Órgão Entidade + Código',
#    y='Valor Recebido',
#    color='Órgão Entidade',
#    title='Contratos Campeões'
#)
#
#fig_orgao.update_xaxes(title_text='Órgão Contratante e Contrato')
#fig_orgao.update_yaxes(title_text='Valores pagos por órgão e Contrato')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#
#st.subheader("Gasto anual em dispensa de licitação por órgão")
#
#@st.cache_data
#def load_data():
#    with open('contratos_OFICIAL.json', 'r', encoding='utf-8') as f:
#        data = json.load(f)
#    return data
#
#data = load_data()
#
## Transformar os dados em um DataFrame
#rows = []
#for entry in data:
#    ano = entry.get("Ano da Compra")
#    orgao = entry.get("Órgão Entidade")
#    valor_homologado = entry.get("Valor Total Homologado", 0)
#    
#    rows.append({
#        "Ano da Compra": ano,
#        "Órgão Entidade": orgao,
#        "Valor Total Homologado": valor_homologado
#    })
#
#df = pd.DataFrame(rows)
#
## Normalizar strings para facilitar a pesquisa
#df['Órgão Entidade Normalizado'] = df['Órgão Entidade'].apply(lambda x: unidecode.unidecode(x).lower())
#
## Campo de texto para pesquisa
#search_term = st.text_input("Digite o nome do Órgão")
#
#if search_term:
#    search_term_normalized = unidecode.unidecode(search_term).lower()
#    # Buscar órgãos que contenham o termo pesquisado
#    matched_organs = df[df['Órgão Entidade Normalizado'].str.contains(search_term_normalized)]['Órgão Entidade'].unique()
#    
#    if len(matched_organs) == 0:
#        st.write("Nenhum órgão encontrado com esse termo de pesquisa.")
#    else:
#        # Usar selectbox para permitir que o usuário selecione um órgão da lista encontrada
#        selected_organ = st.selectbox("Selecione um órgão", matched_organs)
#        
#        if selected_organ:
#            df_filtered = df[df['Órgão Entidade'] == selected_organ]
#            
#            # Agrupamento de dados por ano e órgão
#            df_grouped = df_filtered.groupby(['Ano da Compra', 'Órgão Entidade'])['Valor Total Homologado'].sum().reset_index()
#
#            # Criar gráfico de evolução temporal dos gastos
#            fig_timeline = px.line(df_grouped, x='Ano da Compra', y='Valor Total Homologado', color='Órgão Entidade', title='Evolução dos Gastos Anuais por Órgão')
#
#            # Mostrar gráfico na interface
#            st.plotly_chart(fig_timeline, use_container_width=True)
#
#            # Adicionar tabela de dados filtrados
#            with st.container():
#                st.write(f'<h3><u style="color:white;">Valor anual gasto em dispensa de licitação por:</u> {selected_organ}</h3>', unsafe_allow_html=True)
#                for _, row in df_grouped.iterrows():
#                    st.markdown(f"<p style='font-size:16px;'><u style='color:white;'>Ano {row['Ano da Compra']}:</u> R$ {row['Valor Total Homologado']:,.2f}</p>", unsafe_allow_html=True)
#                st.write("A primeria versão do Portal Nacional de Contratações Públicas [(PNCP)](https://www.gov.br/pncp/pt-br) somente foi lançada em Agosto de 2021 portanto, os dados desse ano podem estar incompletos.")
#                st.write('<hr>', unsafe_allow_html=True)
#                
#else:
#    st.write("Digite o nome de um órgão para começar a pesquisa.")
#'''
###################### v 01

#import streamlit as st
#import pandas as pd
#import plotly.express as px
#
#st.set_page_config(page_title="Gastos de Dispensa por Órgão", layout='wide')
#
#@st.cache_data
#def load_data():
#    df = pd.read_csv('contratos_ordenados_completo.csv')
#    return df
#
#df_ordenado = load_data()
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)
#
#with st.container():
#    st.subheader("PAINEL INTERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](https://unb-mds.github.io/2024-1-Squad-10/)")
#    st.write('---')
#
#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)  # Adicionando a opção "Todos" à lista de anos únicos
#
#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
#
#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
#else:
#    df_filtered = df_ordenado.copy()
#
#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)
#
#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]
#
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Código', 'Empresa Contratada', 'CNPJ', 'Objeto da Compra'])['Valor Recebido'].sum().reset_index()
#df_filtered_gov_grouped_chart2 = df_filtered.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Recebido', ascending=False)
#df_filtered_gov_grouped_chart2 = df_filtered_gov_grouped_chart2.sort_values(by='Valor Recebido', ascending=False)
#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'. Ex: coffee break, lanche, abastecimento, etc")
#
##adicionado para inserir uma segunda tabela ao final do dashboard - impacta o 2º container
#df_filtered_gov_ordenado1 = df_filtered_gov_ordenado
#
#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#    df_filtered_gov_ordenado1 = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes_chart = ['Todos'] + list(df_filtered_gov_grouped_chart2['Órgão Entidade'].unique())
#
#empresa_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Empresa Contratada'].unique())
#
#contrato_empresa_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nome da Empresa Contratada", empresa_opcoes)
#if contrato_empresa_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Empresa Contratada'] == contrato_empresa_opcoes_filtro]
#
#valor_min = 0
#valor_max = int(df_filtered_gov_grouped_chart2['Valor Recebido'].max() + 1000000)
#
## Obter lista de valores únicos recebidos
#valores_unicos = sorted(df_filtered_gov_grouped_chart2['Valor Recebido'].unique())
#valores_unicos = [0] + list(valores_unicos) + [valor_max]
#
## Criar caixas de seleção para os valores mínimo e máximo
#valor_min_selecionado = st.sidebar.selectbox('De:', valores_unicos, index=0)
#valor_max_selecionado = st.sidebar.selectbox('Até:', valores_unicos, index=len(valores_unicos)-1)
#
## Filtrar DataFrame com base nos valores selecionados
#df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Recebido'] >= valor_min_selecionado) & (df_filtered_gov_ordenado['Valor Recebido'] <= valor_max_selecionado)]
#df_filtered_gov_grouped_chart2 = df_filtered_gov_grouped_chart2[(df_filtered_gov_grouped_chart2['Valor Recebido'] >= valor_min_selecionado) & (df_filtered_gov_grouped_chart2['Valor Recebido'] <= valor_max_selecionado)]
#
## Controle de paginação
#total_barras = len(df_filtered_gov_ordenado)
#barras_por_pagina = 10
#num_paginas = total_barras // barras_por_pagina + (total_barras % barras_por_pagina > 0)
#
#pagina = st.sidebar.number_input("Página", min_value=1, max_value=num_paginas, value=1)
#
#inicio = (pagina - 1) * barras_por_pagina
#fim = inicio + barras_por_pagina
#
#df_paginado = df_filtered_gov_ordenado.iloc[inicio:fim]
#df_paginado = df_paginado.sort_values(by='Valor Recebido', ascending=False)
#
#df_paginado_chart2 = df_filtered_gov_grouped_chart2.iloc[inicio:fim]
#df_paginado_chart2 = df_paginado_chart2.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
#df_paginado_chart2 = df_paginado_chart2.sort_values(by='Valor Recebido', ascending=False)
#
#col2 = st.columns(1)[0]
#
#fig_orgao2 = px.bar(df_paginado_chart2, x='Órgão Entidade', y='Valor Recebido', color='Órgão Entidade', title='Órgão Campeão')
#fig_orgao2.update_xaxes(title_text='Órgão Contratante')
#fig_orgao2.update_yaxes(title_text='Valores pagos por órgão')
#fig_orgao2.update_layout(height=800)
#col2.plotly_chart(fig_orgao2, use_container_width=True)
#
#col1 = st.columns(1)[0]
#
#df_paginado['Órgão Entidade + Código'] = df_paginado['Órgão Entidade'] + ' ' + df_paginado['Código']
#
#fig_orgao = px.bar(
#    df_paginado,
#    x='Órgão Entidade + Código',
#    y='Valor Recebido',
#    color='Órgão Entidade',
#    title='Contratos Campeões'
#)
#
#fig_orgao.update_xaxes(title_text='Órgão Contratante e Contrato')
#fig_orgao.update_yaxes(title_text='Valores pagos por órgão e Contrato')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#


########################## vers 5
#import streamlit as st
#import pandas as pd
#import plotly.express as px
#
#st.set_page_config(page_title="Gastos de Dispensa por Órgão", layout='wide')
#
#@st.cache_data
#def load_data():
#    df = pd.read_csv('contratos_ordenados_completo.csv')
#    return df
#
#df_ordenado = load_data()
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)
#
#with st.container():
#    st.subheader("PAINEL INTERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](https://unb-mds.github.io/2024-1-Squad-10/)")
#    st.write('---')
#
##df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)  # Adicionando a opção "Todos" à lista de anos únicos
#
#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
#
#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
#else:
#    df_filtered = df_ordenado.copy()
#
#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)
#
#if orgaos_unicos != 'Todos':
#    
#    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]
#
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade','Código' ,'Empresa Contratada','CNPJ', 'Objeto da Compra'])['Valor Recebido'].sum().reset_index()
#df_filtered_gov_grouped_chart2 = df_filtered.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
##df_filtered_gov_grouped_chart21 = df_filtered_gov_grouped_chart2[df_filtered_gov_grouped_chart2['Órgão Entidade'] == 'MINISTERIO A #SAUDE']
#
##df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade',  'Objeto da Compra'])['Valor Total Homologado'].sum().reset_index)
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Recebido', ascending=False)
#df_filtered_gov_grouped_chart2=df_filtered_gov_grouped_chart2.sort_values(by='Valor Recebido', ascending=False)
#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'. Ex: coffee break, lanche, abastecimento, etc" )
#
##adicionado para inserir uma segunda tabela ao final do dashboard - impacta o 2º container
#df_filtered_gov_ordenado1=df_filtered_gov_ordenado
#
#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#    df_filtered_gov_ordenado1 = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#
##orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes_chart = ['Todos'] + list(df_filtered_gov_grouped_chart2['Órgão Entidade'].unique())
#
#empresa_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Empresa Contratada'].unique())
##empresa_opcoe_opcoes_chart = ['Todos'] + list(df_filtered_gov_grouped_chart2['Empresa Contratada'].unique())
#
#contrato_empresa_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nome da Empresa Contratada", empresa_opcoes)
#if contrato_empresa_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Empresa Contratada'] == contrato_empresa_opcoes_filtro]
#
##valor_min = int(df_filtered_gov_grouped_chart2['Valor Recebido'].min())
##valor_max = int(df_filtered_gov_grouped_chart2['Valor Recebido'].max()+1000000)
#valor_min = 0
#valor_max = int(df_filtered_gov_grouped_chart2['Valor Recebido'].max()+1000000)
#
#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', valor_min, valor_max, (valor_min, valor_max), step=100000)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Recebido'] >= valor_intervalo[0]) &      
# (df_filtered_gov_ordenado['Valor Recebido'] <= valor_intervalo[1])]
#    df_filtered_gov_grouped_chart2= df_filtered_gov_grouped_chart2[(df_filtered_gov_grouped_chart2['Valor Recebido'] >= valor_intervalo[0]) & (df_filtered_gov_grouped_chart2['Valor Recebido'] <= valor_intervalo[1])]
## Controle de paginação
#total_barras = len(df_filtered_gov_ordenado)
#barras_por_pagina = 10
#num_paginas = total_barras // barras_por_pagina + (total_barras % barras_por_pagina > 0)
#
#pagina = st.sidebar.number_input("Página", min_value=1, max_value=num_paginas, value=1)
#
#inicio = (pagina - 1) * barras_por_pagina
#fim = inicio + barras_por_pagina
#
#
#df_paginado = df_filtered_gov_ordenado.iloc[inicio:fim]
#df_paginado=df_paginado.sort_values(by='Valor Recebido', ascending=False)
##
#df_paginado_chart2=df_filtered_gov_grouped_chart2.iloc[inicio:fim]
#df_paginado_chart2 = df_paginado_chart2.groupby(['Órgão Entidade'])['Valor Recebido'].sum().reset_index()
#df_paginado_chart2=df_paginado_chart2.sort_values(by='Valor Recebido', ascending=False)
#
#col2 = st.columns(1)[0]
#
#fig_orgao2 = px.bar(df_paginado_chart2, x='Órgão Entidade', y='Valor Recebido',color='Órgão Entidade', title='Órgão Campeão')
#fig_orgao2.update_xaxes(title_text='Órgão Contratante')
#fig_orgao2.update_yaxes(title_text='Valores pagos por órgão')
#fig_orgao2.update_layout(height=800)
#col2.plotly_chart(fig_orgao2, use_container_width=True)
#
#col1 = st.columns(1)[0]
#
##fig_orgao = px.bar(df_paginado, x='Órgão Entidade', y='Valor Recebido', color='Empresa Contratada', title='Contrato Campeão')
##fig_orgao.update_xaxes(title_text='Contrato por Órgão Contratante')
##fig_orgao.update_yaxes(title_text='Valor pago por contrato')
##fig_orgao.update_layout(height=800)
##col1.plotly_chart(fig_orgao, use_container_width=True)
## Concatenar 'Órgão Entidade' e 'Código' no próprio DataFrame para o eixo x
#df_paginado['Órgão Entidade + Código'] = df_paginado['Órgão Entidade'] + ' ' + df_paginado['Código']
#
## Criar o gráfico de barras
#fig_orgao = px.bar(
#    df_paginado,
#    x='Órgão Entidade + Código',
#    y='Valor Recebido',
#    color='Órgão Entidade',
#    title='Contratos Campeões'
#)
#
## Atualizar títulos dos eixos e layout
#fig_orgao.update_xaxes(title_text='Órgão Contratante e Contrato')
#fig_orgao.update_yaxes(title_text='Valores pagos por órgão e Contrato')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#
##with st.container():
##    st.write('Dados Compilados1')
##    st.write(df_filtered_gov_ordenado1)
##    st.write('---')
#
#
#