import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

# Criando listas de 1 até 144
empresas = [f"Empresas Contratadas.Empresa Contratada -{i}" for i in range(1, 145)] 
cnpj = [f"Empresas Contratadas.CNPJ -{i}" for i in range(1, 145)]
valor = [f"Empresas Contratadas.Valor Recebido -{i}" for i in range(1, 145)]
desc = [f"Empresas Contratadas.Descrição -{i}" for i in range(1, 145)]

tipos_de_dados = {
    "Modalidade": str,
    "Código":str,
    "UF":str,
    "Órgão Entidade":str,
    "Objeto da Compra":str,
    "Ano da Compra":int,
    "Valor Total Estimado":float,
    "Valor Total Homologado":float,
}

# Defini os tipos de dados para cada elemento de todas as listas
for i in range(144): 
    tipos_de_dados[empresas[i]] = str
    tipos_de_dados[cnpj[i]] = str
    tipos_de_dados[valor[i]] = float
    tipos_de_dados[desc[i]] = str

@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("contratos_oficial.csv", dtype=tipos_de_dados)
    tabela = tabela.sort_values(by="Valor Total Homologado", ascending=False).reset_index()
    tabela = tabela.drop("index", axis=1)
    return tabela

st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')

with st.container():
    st.subheader("RANKING DOS GASTOS GOVERNAMENTAIS COM DISPENSA DE LICITAÇÃO")
    st.write('Informações sobre contratos')
    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
    st.write('---')
    dados = carregar_dados()
    

anos_unicos = sorted(dados['Ano da Compra'].unique()) #Quando utilizamos o unique, criamos um objeto do tipo numpy.ndarray
anos_unicos = ['Todos'] + list(anos_unicos)  # Adicionando a opção "Todos" à lista de anos únicos

ano = st.sidebar.selectbox("Ano da Dispensa", anos_unicos)

if ano != 'Todos':
    df_filtered = dados[dados['Ano da Compra'] == ano]
else:
    df_filtered = dados.copy()  # Se 'Todos' for selecionado, mostra todos os dados

orgao_unico = sorted(df_filtered['Órgão Entidade'].unique())
orgao_unico = ['Todos'] + list(orgao_unico)

orgao = st.sidebar.selectbox("Órgão Emissor", orgao_unico)

if orgao != 'Todos':
    df_filtered_1 = df_filtered[df_filtered["Órgão Entidade"].astype(str) == str(orgao)]
else:
    df_filtered_1 = df_filtered.copy()


palavra_filtro = st.sidebar.text_input("Filtrar por item da compra")

# Filtrar colunas que começam com "Empresas Contratadas.Descrição"
colunas_filtradas = df_filtered_1.filter(regex='^Empresas Contratadas.Descrição')

# Inicializar boolean_series como uma série de False
boolean_series = pd.Series([False] * len(df_filtered_1))

# Para cada coluna filtrada, verifique a existência de 'x'
for coluna in colunas_filtradas:
    boolean_series = boolean_series | df_filtered_1[coluna].str.contains(palavra_filtro, case=False)

boolean_final = (df_filtered_1["Objeto da Compra"].str.contains(palavra_filtro,case=False)) | boolean_series

if palavra_filtro:
    df_filtred_2 = df_filtered_1[boolean_final]
else:
    df_filtred_2 = df_filtered_1.copy()

st.write(df_filtred_2)



#ano = str(input("Digite o valor do ano:"))

#tabela_ano = dados[dados['Ano da Compra'].astype(str) == ano]
#tabela_ano.to_csv("resultadoAnoCompra.csv", index=False)

