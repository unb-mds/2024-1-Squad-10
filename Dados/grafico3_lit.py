import streamlit as st
import pandas as pd
import altair as alt
import plotly_express as px

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
    #if "selected_empresa" not in st.session_state:
    #    st.session_state.selected_empresa = None

# Inicializando o estado da sessão
init_session_state()

# Função para resetar a paginação
def reset_pagination():
    st.session_state.page = 0

with st.container():
    st.subheader("RANKING DAS EMPRESAS MAIS BENFICIADAS POR DISPENSA DE LICITAÇÃO")
    st.write('Informações sobre contratos')
    st.write("Quer saber mais sobre nosso projeto? [clique aqui](www.unb.br)")
    st.write('---')
    data = carregar_dados()
    data1= carregar_dados1()

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
    st.rerun()

#def selecionar_empresa(event,altair_event):
#    st.session_state.selected_empresa = altair_event['Empresa Contratada']
#    st.rerun()

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

altura_grafico = max(400, len(df_group_list) * 35)  #Ajusta a altura conforme a lista for aumentando

# Criando o gráfico de barras empilhadas
chart = alt.Chart(df_grafico).mark_bar().encode(
    x=alt.X('sum(Valor Recebido):Q', title='Valor Total Recebido ($)'),
    y=alt.Y('Empresa Contratada:N', sort=df_group_list, title='Empresas Contratadas por Dispensa de Licitação', axis=alt.Axis(labelLimit=170)),
    color=alt.Color('Código:N', legend=None), # legend=alt.Legend(title="Contratos")
    order=alt.Order('Código:N', sort='ascending')
).properties(
    title= alt.TitleParams(
        text='Soma dos Valores Recebidos por Contrato',
        anchor= "middle", 
        color = 'rgba(255, 255, 255, 0.5)' , 
        fontSize=20, 
        fontStyle='oblique',
    )
).properties(
    height=altura_grafico  # Define a altura do gráfico
)

st.altair_chart(chart, use_container_width=True)

# Adiciona o botão "Próxima página" abaixo do gráfico
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Página anterior"):
        if st.session_state.page > 0:
            change_page(-1)

with col2:
    if st.button("Próxima página"):
        change_page(1)
    
st.write(" ")
st.write(" ")
st.write(" ")

#Função que irá fazer o gráfico da pizza
def grafico_pie(dataframe):
    # Criando o gráfico de rosca com Plotly Express
    fig = px.pie(dataframe, values='Valor Recebido', names='Empresa Contratada', title='Distribuição do Contrato',
                hole=0.55,  # Define o tamanho do buraco no meio (0.4 = 40%)
                labels={'Valor Recebido':'Valor', 'Empresa Contratada':'Empresa'},
                hover_data={'Valor Recebido': True, 'Empresa Contratada': True})

    # Atualizar as fatias do gráfico para mostrar porcentagem e rótulo
    fig.update_traces(textposition='inside', textinfo='percent')

    # Personalizar o hovertemplate
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percent}")

    fig.update_layout(
        
        title_x=0.2  # Centralizar o título
    )

    return fig


df_filtro = df.groupby(by=["Código", "Empresa Contratada"])["Valor Recebido"].sum().reset_index()

def detalhes_contratos(empresa):
    contratos = df_filtro["Código"][df_filtro["Empresa Contratada"]== empresa].to_list()
    for i,contrato in enumerate(contratos):
        df_filtro1 = df_filtro[df_filtro["Código"] == contrato] #Aqui teremos a lista das empresas contratadas dentro desse contrato específico
        df_filtro1 = df_filtro1[["Empresa Contratada", "Valor Recebido"]] #Estamos deixando o dataframe apenas com essas duas colunas
        orgao = data1["Órgão Entidade"][data1["Código"]== contrato].iloc[0]
        data_compra = data1["Ano da Compra"][data1["Código"]== contrato].iloc[0]
        objeto = data1["Objeto da Compra"][data1["Código"]== contrato].iloc[0]
        valor = data1["Valor Total Homologado"][data1["Código"]== contrato].iloc[0]
        valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        col1,col2 = st.columns([3,2]) #define a proporção das colunas

        with col1:
            if i==0:
                st.write(" ")
            st.markdown(f"<p><span style='color:red;'>Contrato n° {i+1}:</span> <span '>{contrato}</span></p>", unsafe_allow_html=True)
            #st.write(f"Contrato n° {i+1}: {contrato}")
            st.markdown(f"<p><span style='border-bottom: 2px solid red;'>Ano da compra</span>: {data_compra}</p>", unsafe_allow_html=True)        
            st.markdown(f"<p><span style='border-bottom: 2px solid red;'>Órgão Responsável</span>: {orgao}</p>", unsafe_allow_html=True)        
            st.markdown(f"<p><span style='border-bottom: 2px solid red;'>Objeto da compra do contrato</span>: {objeto}</p>", unsafe_allow_html=True)        
            #st.write(f"Objeto da compra do contrato: {objeto}")
            st.markdown(f"<p><span style='border-bottom: 2px solid red;'>Valor Total Homologado</span>: {valor_formatado}</p>", unsafe_allow_html=True)  

        with col2:
            pie = grafico_pie(df_filtro1) #Adicionando o gráfico pie
            st.plotly_chart(pie)

        st.write("----")
    return contratos

escolha = ["Escolha sua empresa"] + df_group_list
empresa_selecionada = st.selectbox("Selecione a Empresa para ver detalhes dos contratos que ela participou: ", escolha)

if empresa_selecionada != "Escolha sua empresa":
    contratos = detalhes_contratos(empresa_selecionada)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    selecao_contratos = st.selectbox("Selecione o contrato que deseja: ", contratos)