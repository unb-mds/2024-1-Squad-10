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

#comentário



##############################


#import streamlit as st
#import pandas as pd
#import plotly.express as px#

#st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')#

#with st.container():
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
#    st.write('---')#

#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)#

## Adicionando um filtro para selecionar a quantidade de órgãos a serem exibidos
#num_opcoes = st.sidebar.selectbox("Quantidade de Órgãos a Exibir", [20, 50, 100, 'Mais #de 100'], index=0)#

#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)#

#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
#else:
#    df_filtered = df_ordenado.copy()#

#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)#

#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]#

#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Código', 'Objeto da #Compra'])['Valor Total Homologado'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Total #Homologado', ascending=False)#

#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da #Compra'")#

#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro, case=False)]#

#orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Código'].unique())#

#contrato_orgao_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nº do Contrato", #contrato_orgao_opcoes)
#if contrato_orgao_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Código'] == contrato_orgao_opcoes_filtro]#

#valor_min = int(df_filtered_gov_ordenado['Valor Total Homologado'].min())
#valor_max = int(df_filtered_gov_ordenado['Valor Total Homologado'].max())#

#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', valor_min, valor_max, (valor_min, valor_max), step=100000)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Total Homologado'] >= valor_intervalo[0]) &
#                                                        (df_filtered_gov_ordenado['Valor Total Homologado'] <= valor_intervalo[1])]#

## Limitando a quantidade de órgãos a serem exibidos
#if num_opcoes != 'Mais de 100':
#    num_opcoes = int(num_opcoes)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado.head(num_opcoes)#

#col1 = st.columns(1)[0]#

#fig_orgao = px.bar(df_filtered_gov_ordenado, x='Órgão Entidade', y='Valor Total #Homologado', color='Código', title='Órgão Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)#

#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')



############# versão 04 ###############
#import streamlit as st
#import pandas as pd
#import plotly.express as px
#
#st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')
#
#with st.container():
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE #LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
#    st.write('---')
#
#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv')
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)
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
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Código', 'Objeto da #Compra'])['Valor Total Homologado'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Total #Homologado', ascending=False)
#
#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da #Compra'")
#
#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado#['Objeto da Compra'].str.contains(palavra_filtro, case=False)]
#
#orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Código'].unique())
#
#contrato_orgao_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nº do Contrato", #contrato_orgao_opcoes)
#if contrato_orgao_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado#['Código'] == contrato_orgao_opcoes_filtro]
#
#valor_min = int(df_filtered_gov_ordenado['Valor Total Homologado'].min())
#valor_max = int(df_filtered_gov_ordenado['Valor Total Homologado'].max())
#
#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', #valor_min, valor_max, (valor_min, valor_max), step=100000)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado#['Valor Total Homologado'] >= valor_intervalo[0]) &
#                                                        (df_filtered_gov_ordenado#['Valor Total Homologado'] <= #valor_intervalo[1])]
#
## Adicionando um filtro para selecionar a quantidade de órgãos a serem exibidos
#num_opcoes = st.sidebar.selectbox("Quantidade de Órgãos a Exibir", [20, 50, 100, 'Mais #de 100'], index=0)
#
## Limitando a quantidade de órgãos a serem exibidos
#if num_opcoes != 'Mais de 100':
#    num_opcoes = int(num_opcoes)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado.head(num_opcoes)
#
#col1 = st.columns(1)[0]
#
#fig_orgao = px.bar(df_filtered_gov_ordenado, x='Órgão Entidade', y='Valor Total #Homologado', color='Código', title='Órgão Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#
#

############# versão 03.02 
#
#import streamlit as st
#import pandas as pd
#import plotly.express as px
#
#st.set_page_config(page_title="Queridinhas da Licitação", #layout='wide')
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
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS #GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique #aqui](www.unb.br)")
#    st.write('---')
#
#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
#
#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] #== ano]
#else:
#    df_filtered = df_ordenado.copy()
#
#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão #Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", #orgaos_unicos_lista)
#
#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão #Entidade'] == orgaos_unicos]
#
#palavra_filtro = st.sidebar.text_input("Filtrar por #Palavra na Coluna 'Objeto da Compra'")
#
#if palavra_filtro:
#    df_filtered = df_filtered[df_filtered['Objeto da #Compra'].str.contains(palavra_filtro, case=False)]
#
#orgao_opcoes = ['Todos'] + list(df_filtered['Órgão #Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered#['Código'].unique())
#
#contrato_orgao_opcoes_filtro = st.sidebar.selectbox#("Filtrar pelo nº do Contrato", contrato_orgao_opcoes)
#if contrato_orgao_opcoes_filtro != 'Todos':
#    df_filtered = df_filtered[df_filtered['Código'] == #contrato_orgao_opcoes_filtro]
#
#valor_min = int(df_filtered['Valor Total Homologado'].min#())
#valor_max = int(df_filtered['Valor Total Homologado'].max#())
#
#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa #de valores recebidos', valor_min, valor_max, #(valor_min, valor_max), step=100000)
#    df_filtered = df_filtered[(df_filtered['Valor Total #Homologado'] >= valor_intervalo[0]) & (df_filtered#['Valor Total Homologado'] <= valor_intervalo[1])]
#
## Agrupando por Órgão Entidade e Código para somar os #valores
#df_grouped = df_filtered.groupby(['Órgão Entidade', #'Código'])['Valor Total Homologado'].sum().reset_index()
#
## Agrupando por Órgão Entidade para obter o valor total #por órgão
#df_aggregated = df_grouped.groupby('Órgão Entidade')#['Valor Total Homologado'].sum().reset_index()
#
## Ordenando de forma decrescente pelo valor total #homologado
#df_aggregated = df_aggregated.sort_values(by='Valor Total #Homologado', ascending=False)
#
## Controle de paginação
#total_barras = len(df_aggregated)
#barras_por_pagina = 10
#num_paginas = total_barras // barras_por_pagina + #(total_barras % barras_por_pagina > 0)
#
#pagina = st.sidebar.number_input("Página", min_value=1, #max_value=num_paginas, value=1)
#
#inicio = (pagina - 1) * barras_por_pagina
#fim = inicio + barras_por_pagina
#
#df_paginado = df_grouped[df_grouped['Órgão Entidade'].isin#(df_aggregated.iloc[inicio:fim]['Órgão Entidade'])]
#
#col1 = st.columns(1)[0]
#
#fig_orgao = px.bar(df_paginado, x='Órgão Entidade', #y='Valor Total Homologado', color='Código', title='Órgão #Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com #Dispensas de Licitação')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered)
#    st.write('---')
#





########################### versão 03 .01 

#import streamlit as st
#import pandas as pd
#import plotly.express as px
#
#st.set_page_config(page_title=" Licitação", layout='wide')
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
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS #GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique #aqui](www.unb.br)")
#    st.write('---')
#
#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)
#
#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] #== ano]
#else:
#    df_filtered = df_ordenado.copy()
#
#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão #Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", #orgaos_unicos_lista)
#
#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão #Entidade'] == orgaos_unicos]
#
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão #Entidade', 'Código', 'Objeto da Compra'])['Valor Total #Homologado'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.#sort_values(by='Valor Total Homologado', ascending=False)
#
#palavra_filtro = st.sidebar.text_input("Filtrar por #Palavra na Coluna 'Objeto da Compra'")
#
#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado#[df_filtered_gov_ordenado['Objeto da Compra'].str.#contains(palavra_filtro, case=False)]
#
#orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado#['Órgão Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list#(df_filtered_gov_ordenado['Código'].unique())
#
#contrato_orgao_opcoes_filtro = st.sidebar.selectbox#("Filtrar pelo nº do Contrato", contrato_orgao_opcoes)
#if contrato_orgao_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado#[df_filtered_gov_ordenado['Código'] == #contrato_orgao_opcoes_filtro]
#
#valor_min = int(df_filtered_gov_ordenado['Valor Total #Homologado'].min())
#valor_max = int(df_filtered_gov_ordenado['Valor Total #Homologado'].max())
#
#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa #de valores recebidos', valor_min, valor_max, #(valor_min, valor_max), step=100000)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado#[(df_filtered_gov_ordenado['Valor Total Homologado'] #>= valor_intervalo[0]) & (df_filtered_gov_ordenado#['Valor Total Homologado'] <= valor_intervalo[1])]
#
## Controle de paginação
#total_barras = len(df_filtered_gov_ordenado)
#barras_por_pagina = 10
#num_paginas = total_barras // barras_por_pagina + #(total_barras % barras_por_pagina > 0)
#
#pagina = st.sidebar.number_input("Página", min_value=1, #max_value=num_paginas, value=1)
#
#inicio = (pagina - 1) * barras_por_pagina
#fim = inicio + barras_por_pagina
#
#df_paginado = df_filtered_gov_ordenado.iloc[inicio:fim]
#
#col1 = st.columns(1)[0]
#
#fig_orgao = px.bar(df_paginado, x='Órgão Entidade', #y='Valor Total Homologado', color='Código', title='Órgão #Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com #Dispensas de Licitação')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#


################ versao 02 ###################
#import streamlit as st
#import pandas as pd
#import plotly.express as px#

#st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')#

#@st.cache_data
#def load_data():
#    df = pd.read_csv('contratos_ordenados_completo.csv')
#    return df#

#df_ordenado = load_data()
#df_ordenado = df_ordenado.sort_values("Ano da Compra")
#anos_unicos = df_ordenado['Ano da Compra'].unique()
#anos_unicos = ['Todos'] + list(anos_unicos)#

#with st.container():
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
#    st.write('---')#

#ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)#

#if ano != 'Todos':
#    df_filtered = df_ordenado[df_ordenado['Ano da Compra'] == ano]
#else:
#    df_filtered = df_ordenado.copy()#

#orgaos_unicos_lista = ['Todos'] + list(df_filtered['Órgão Entidade'].unique())
#orgaos_unicos = st.sidebar.selectbox("Órgão Contratante", orgaos_unicos_lista)#

#if orgaos_unicos != 'Todos':
#    df_filtered = df_filtered[df_filtered['Órgão Entidade'] == orgaos_unicos]#

#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade', 'Código', 'Objeto da Compra'])['Valor Total Homologado'].sum().#reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Total Homologado', ascending=False)#

#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'")#

#if palavra_filtro:
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].str.contains(palavra_filtro,# case=False)]#

#orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Órgão Entidade'].unique())
#contrato_orgao_opcoes = ['Todos'] + list(df_filtered_gov_ordenado['Código'].unique())#

#contrato_orgao_opcoes_filtro = st.sidebar.selectbox("Filtrar pelo nº do Contrato", contrato_orgao_opcoes)
#if contrato_orgao_opcoes_filtro != 'Todos':
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Código'] == contrato_orgao_opcoes_filtro]#

#valor_min = int(df_filtered_gov_ordenado['Valor Total Homologado'].min())
#valor_max = int(df_filtered_gov_ordenado['Valor Total Homologado'].max())#

#if valor_min != valor_max:
#    valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', valor_min, valor_max, (valor_min, valor_max),# step=100000)
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Total Homologado'] >= valor_interval#o[0]) & (df_filtered_gov_ordenado['Valor Total Homologado'] <= valor_intervalo[1])]#

#col1 = st.columns(1)[0]#

#fig_orgao = px.bar(df_filtered_gov_ordenado, x='Órgão Entidade', y='Valor Total Homologado', color='Código', title='Órgão Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
#fig_orgao.update_layout(height=800)
#col1.plotly_chart(fig_orgao, use_container_width=True)#

#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')


##################### VERSAO 01 ##################################

#import streamlit as st
#import pandas as pd
#import plotly.express as px
#import numpy as np
#
#
#st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')
#
#
#
#with st.container():
#    st.subheader("PAINEL ITERATIVO SOBRE OS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
#    st.write('Informações sobre contratos')
#    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
#    st.write('---')
#
#df_ordenado = pd.read_csv('contratos_ordenados_completo.csv') #- verificar onde está o arquivo
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
#    df_filtered = df_ordenado.copy()  # Se 'Todos' for selecionado, mostra todos os dados
#
#anofundacao_unicos = ['Todos'] + list(df_filtered['Ano de Início da Atividade'].unique())  # #Adicionando a opção "Todos" à lista de anos de fundação únicos
#anofundacao = st.sidebar.selectbox("Ano de Fundação da Empresa Contratada", anofundacao_unicos)
#
#if anofundacao != 'Todos':
#    df_filtered = df_filtered[df_filtered['Ano de Início da Atividade'] == anofundacao]    
#
#df_filtered_sellers_grouped = df_filtered.groupby(['CNPJ','Empresa Contratada','Objeto da Compra'])#['Valor Recebido'].sum().reset_index()
#df_filtered_sellers_ordenado = df_filtered_sellers_grouped.sort_values(by='Valor Recebido', #ascending=False)
#
#df_filtered_gov_grouped = df_filtered.groupby(['Órgão Entidade','CNPJ','Objeto da Compra'])['Valor #Total Homologado'].sum().reset_index()
#df_filtered_gov_ordenado = df_filtered_gov_grouped.sort_values(by='Valor Total Homologado', #ascending=False)
#
## Adicionar campo de texto para filtrar por palavra na coluna 'Objeto da Compra'
#palavra_filtro = st.sidebar.text_input("Filtrar por Palavra na Coluna 'Objeto da Compra'")
#
## Filtrar o DataFrame se uma palavra foi digitada
#if palavra_filtro:
#    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['Objeto da #Compra'].str.contains(palavra_filtro, case=False)]
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Objeto da Compra'].#str.contains(palavra_filtro, case=False)]
#
## Adicionar filtros para 'Empresas Contratadas.Empresa Contratada' e 'Empresas Contratadas.CNPJ'
#razao_social_opcoes = ['Todos'] + list(df_filtered_sellers_ordenado['Empresa Contratada'].unique())
#razaosocial_fornecedor_opcoes = ['Todos'] + list(df_filtered_sellers_ordenado['CNPJ'].unique())
#
#razaosocial_filtro = st.sidebar.selectbox("Filtrar pelo Nome da Empresa Contratada", #razao_social_opcoes)
#if razaosocial_filtro != 'Todos':
#    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['Empresa #Contratada'] == razaosocial_filtro]
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['Empresa Contratada'] #== razaosocial_filtro]
#
#razaosocial_fornecedor_filtro = st.sidebar.selectbox("Filtrar pelo CNPJ da empresa contratada", #razaosocial_fornecedor_opcoes)
#if razaosocial_fornecedor_filtro != 'Todos':
#    df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[df_filtered_sellers_ordenado['CNPJ'] == #razaosocial_fornecedor_filtro]
#    df_filtered_gov_ordenado = df_filtered_gov_ordenado[df_filtered_gov_ordenado['CNPJ'] == #razaosocial_fornecedor_filtro]
#
## Adicionar um slider para filtrar por faixas de valores
#valor_min = int(df_filtered_sellers_ordenado['Valor Recebido'].min())
#valor_max = int(df_filtered_sellers_ordenado['Valor Recebido'].max())
#valor_intervalo = st.sidebar.slider('Selecionar faixa de valores recebidos', valor_min, valor_max, #(valor_min, valor_max), step=100000)
#
## Filtrar o DataFrame pelos valores selecionados no slider
#df_filtered_sellers_ordenado = df_filtered_sellers_ordenado[(df_filtered_sellers_ordenado['Valor #Recebido'] >= valor_intervalo[0]) &
#                                                            (df_filtered_sellers_ordenado['Valor #Recebido'] <= valor_intervalo[1])]
#
#df_filtered_gov_ordenado = df_filtered_gov_ordenado[(df_filtered_gov_ordenado['Valor Total Homologado'] #>= valor_intervalo[0]) &
#                                                    (df_filtered_gov_ordenado['Valor Total Homologado'] #<= valor_intervalo[1])]
#
#col1 = st.columns(1)[0]
#col3, col4, col5 = st.columns(3)
#
##fig_campea = px.bar(df_filtered_sellers_ordenado, x='CNPJ', y='Valor Recebido',color='Empresa #Contratada' ,title='Empresas campeãs')
##fig_campea.update_xaxes(title_text='Empresas Contratadas')
##fig_campea.update_yaxes(title_text='Valor Recebido')
##col1.plotly_chart(fig_campea, use_container_width=True)
#
#fig_orgao = px.bar(df_filtered_gov_ordenado, x='Órgão Entidade', y='Valor Total Homologado',#color='CNPJ',title='Órgão Campeão')
#fig_orgao.update_xaxes(title_text='Órgão Contratante')
#fig_orgao.update_yaxes(title_text='Valor pago com Dispensas de Licitação')
#fig_orgao.update_layout(height=800)  # Definindo a altura do gráfico
#col1.plotly_chart(fig_orgao, use_container_width=True)
#
##Gerar mapa das cidades que mais utilizaram
#
##coordenadas = {
##    'Brasil': {'lat': -14.25, 'lon': -54.40},
##    'Brasília': {'lat': -15.8267, 'lon': -47.9218},
##    'São Paulo': {'lat': -23.5505, 'lon': -46.6333},
##    'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729},
##    'Salvador': {'lat': -12.9714, 'lon': -38.5014},
##    'Manaus': {'lat': -3.1190, 'lon': -60.0217}
##}
##
### Função para gerar pontos aleatórios em torno de uma coordenada central
##def gerar_pontos_aleatorios(lat, lon, n_points=1000):
##    return pd.DataFrame(
##        np.random.randn(n_points, 2) / [500, 500] + [lat, lon],
##        columns=['lat', 'lon'])
##
### Criando um aplicativo Streamlit
##st.title('CIDADES DAS SEDES DAS EMPRESAS CONTRATADAS')
##
### Selecionando uma cidade para visualização
##cidade_selecionada = st.selectbox('Selecione uma cidade:', list(coordenadas.keys()))
##
### Gerando pontos aleatórios em torno da cidade selecionada
##location = gerar_pontos_aleatorios(coordenadas[cidade_selecionada]['lat'], coordenadas#[cidade_selecionada]['lon'])
##st.map(location)
#
#with st.container():
#    st.write('Dados Compilados')
#    st.write(df_filtered_sellers_ordenado)
#    st.write(df_filtered_gov_ordenado)
#    st.write('---')
#

