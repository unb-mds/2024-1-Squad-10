import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Queridinhas da Licitação", layout='wide')

tipos_de_dados = {
    "Código": str,
    "Empresa Contratada": str,
    "CNPJ": str,
    "Valor Recebido": float,
    "Descrição": str
}

@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("x_empresas_contratadas.csv", dtype=tipos_de_dados)
    tabela = tabela.sort_values(by="Valor Recebido", ascending=False).reset_index()
    tabela = tabela.drop("index", axis=1)
    return tabela

@st.cache_data
def carregar_dados1():
    tabela = pd.read_json("contratos_OFICIAL.json")
    tabela = tabela.drop("Empresas Contratadas", axis=1)
    return tabela

# Função para inicializar o estado da sessão
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = 0

# Inicializando o estado da sessão
init_session_state()

# Função para resetar a paginação
def reset_pagination():
    st.session_state.page = 0

with st.container():
    st.subheader("RANKING DAS EMPRESAS MAIS BENEFICIADAS POR DISPENSA DE LICITAÇÃO")
    st.write('Informações sobre contratos')
    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
    st.write('---')
    data = carregar_dados()
    data1 = carregar_dados1()

# Sidebar para selecionar a quantidade de empresas e o intervalo de valores recebidos
N = st.sidebar.selectbox("Selecione a quantidade de empresas", [5, 10, 15, 20, 25, 30, 40], on_change=reset_pagination)
min_value = st.sidebar.number_input("Digite o valor mínimo recebido", min_value=0, max_value=6000000000, value=0, on_change=reset_pagination)
max_value = st.sidebar.number_input("Digite o valor máximo recebido", min_value=0, max_value=6000000000, value=6000000000, on_change=reset_pagination)

# Garantir que o valor máximo é sempre maior ou igual ao valor mínimo
if min_value > max_value:
    st.sidebar.error("O valor máximo deve ser maior ou igual ao valor mínimo.")

# Função para ajustar a página ao clicar nos botões
def change_page(change):
    st.session_state.page += change
    st.experimental_rerun()

# Filtrando os dados com base no intervalo de valores recebidos
df = data[["Código", "Empresa Contratada", "Valor Recebido"]]
df_group = df.groupby(by=["Empresa Contratada"])["Valor Recebido"].sum().reset_index()
df_group = df_group[(df_group["Valor Recebido"] >= min_value) & (df_group["Valor Recebido"] <= max_value)]
df_group = df_group.sort_values(by="Valor Recebido", ascending=False)

# Implementação da paginação
start_idx = st.session_state.page * N
end_idx = start_idx + N
df_page = df_group.iloc[start_idx:end_idx]
df_group_list = df_page["Empresa Contratada"].tolist()

df_grafico = df[df["Empresa Contratada"].isin(df_group_list)]

altura_grafico = max(400, len(df_group_list) * 35)  # Ajusta a altura conforme a lista for aumentando

# Criando o gráfico de barras empilhadas
chart = alt.Chart(df_grafico).mark_bar().encode(
    x=alt.X('sum(Valor Recebido):Q', title='Valor Total Recebido ($)'),
    y=alt.Y('Empresa Contratada:N', sort=df_group_list, title='Empresas Contratadas por Dispensa de Licitação', axis=alt.Axis(labelLimit=170)),
    color=alt.Color('Código:N', legend=None),  # legend=alt.Legend(title="Contratos")
    order=alt.Order('Código:N', sort='ascending')
).properties(
    title=alt.TitleParams(
        text='Soma dos Valores Recebidos por Contrato',
        anchor="middle",
        color='rgba(255, 255, 255, 0.5)',
        fontSize=20,
        fontStyle='oblique',
    ),
    height=altura_grafico  # Define a altura do gráfico
)

st.altair_chart(chart, use_container_width=True)

# Adiciona os botões de paginação
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Página anterior"):
        if st.session_state.page > 0:
            change_page(-1)
with col2:
    if st.button("Próxima página"):
        if end_idx < len(df_group):
            change_page(1)
