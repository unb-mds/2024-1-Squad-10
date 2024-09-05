import streamlit as st
import pandas as pd
import altair as alt
import plotly_express as px
import os

st.set_page_config(page_title="Queridinhas da Licitação", layout="wide")

tipos_de_dados = {
    "Código": str,
    "Empresa Contratada": str,
    "CNPJ": str,
    "Valor Recebido": float,
    "Descrição": str,
}

caminho_arquivo = os.path.join(
    os.path.dirname(__file__), "..", "x_empresas_contratadas.csv"
)
caminho_arquivo1 = os.path.join(
    os.path.dirname(__file__), "..", "contratos_OFICIAL.json"
)
caminho_arquivo2 = os.path.join(
    os.path.dirname(__file__), "..", "infos_cnpj_OFICIAL.json"
)


@st.cache_data
def carregar_dados():
    tabela = pd.read_csv(caminho_arquivo, dtype=tipos_de_dados)
    tabela = tabela.sort_values(by="Valor Recebido", ascending=False).reset_index()
    tabela = tabela.drop("index", axis=1)
    return tabela


@st.cache_data
def carregar_dados1():
    tabela = pd.read_json(caminho_arquivo1)
    tabela = tabela.drop("Empresas Contratadas", axis=1)
    return tabela


@st.cache_data
def carregar_dados2():
    tabela = pd.read_json(caminho_arquivo2, encoding="utf-8")
    return tabela


# Função para inicializar o estado da sessão
def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = 0
    # if "selected_empresa" not in st.session_state:
    #    st.session_state.selected_empresa = None


# Inicializando o estado da sessão
init_session_state()


# Função para resetar a paginação
def reset_pagination():
    st.session_state.page = 0


with st.container():
    st.subheader("RANKING DAS EMPRESAS MAIS BENFICIADAS POR DISPENSA DE LICITAÇÃO")
    st.write(
        "Quer saber mais sobre nosso projeto? [clique aqui](https://unb-mds.github.io/2024-1-Squad-10/)"
    )
    st.write(
        "Abaixo, o gráfico de barras laterais mostra o Ranking das empresas mais beneficiadas por dispensa de licitação no Distrito Federal. Cada cor dentro das barras laterais indica um contrato diferente que a empresa participou, e a barra inteira é o valor total que ela recebeu somando todos os contratos que participou"
    )
    st.write("---")
    data = carregar_dados()
    data1 = carregar_dados1()
    data2 = carregar_dados2()

# Sidebar para selecionar a quantidade de empresas e o intervalo de valores recebidos
N = st.sidebar.selectbox(
    "Selecione a quantidade de empresas",
    [5, 10, 15, 20, 25, 30, 40],
    on_change=reset_pagination,
)
min_value = st.sidebar.number_input(
    "Digite o valor mínimo recebido",
    min_value=0,
    max_value=6000000000,
    value=0,
    on_change=reset_pagination,
)
max_value = st.sidebar.number_input(
    "Digite o valor máximo recebido",
    min_value=0,
    max_value=6000000000,
    value=6000000000,
    on_change=reset_pagination,
)

# Garantir que o valor máximo é sempre maior ou igual ao valor mínimo
if min_value > max_value:
    st.sidebar.error("O valor máximo deve ser maior ou igual ao valor mínimo.")


# Função para ajustar a página ao clicar nos botões
def change_page(change):
    st.session_state.page += change
    st.rerun()


def colunas_dataFrame(data_frame, *colunas):
    """
    Essa função transforma um dataframe em um novo dataframe filtrado apenas com as colunas desejadas.

    - param data_frame: dataframe que iremos utilizar para filtrar colunas
    - param colunas: Insira no mínimo 2 colunas e no máximo 5
    """
    if len(colunas) < 2 or len(colunas) > 5:
        raise ValueError("Insira no mínimo duas colunas e no máximo cinco")

    return data_frame[list(colunas)]


# Filtrando os dados com base no intervalo de valores recebidos
# df = data[["Código", "Empresa Contratada", "Valor Recebido"]]
df = colunas_dataFrame(data, "Código", "Empresa Contratada", "Valor Recebido")
df_group = df.groupby(by=["Empresa Contratada"])["Valor Recebido"].sum().reset_index()
df_group = df_group[
    (df_group["Valor Recebido"] >= min_value)
    & (df_group["Valor Recebido"] <= max_value)
]
df_group = df_group.sort_values(by="Valor Recebido", ascending=False)

# Implementação da paginação
start_idx = st.session_state.page * N
end_idx = start_idx + N
df_page = df_group.iloc[start_idx:end_idx]
df_group_list = df_page["Empresa Contratada"].tolist()

df_grafico = df[df["Empresa Contratada"].isin(df_group_list)]

altura_grafico = max(
    400, len(df_group_list) * 35
)  # Ajusta a altura conforme a lista for aumentando


# Criando o gráfico de barras empilhadas
def criar_grafico_barra(
    df_grafico,
    df_group_list,
    altura_grafico,
    titulo_grafico="Soma dos Valores Recebidos por Contrato",
    cor_texto="rgba(255, 255, 255, 0.5)",
    tamanho_fonte=20,
):
    """
    Essa função cria o gráfico de barras laterais em que será mostrado a quantidade de contratos que cada em presa tem.

    - param df_grafico: dataframe contendo as empresas, o id dos contratos e os valores recebidos
    - param df_group_list: lista das empresas que serão mostradas no eixo Y com base na paginação
    - param altura_grafico: altura em pixels, já definida
    - param titulo_grafico (OPCIONAL): título, já está pré-definido, mas pode ser alterado
    - param cor_texto (OPCIONAL): cor em rgb do título
    - param tamanho_fonte (OPCIONAL): tamanho da fonte do título, já está pré-definido, mas pode ser alterado

    """
    chart = (
        alt.Chart(df_grafico)
        .mark_bar()
        .encode(
            x=alt.X("sum(Valor Recebido):Q", title="Valor Total Recebido ($)"),
            y=alt.Y(
                "Empresa Contratada:N",
                sort=df_group_list,
                title="Empresas Contratadas por Dispensa de Licitação",
                axis=alt.Axis(labelLimit=170),
            ),
            color=alt.Color("Código:N", legend=None),
            order=alt.Order("Código:N", sort="ascending"),
        )
        .properties(
            title=alt.TitleParams(
                text=titulo_grafico,
                anchor="middle",
                color=cor_texto,
                fontSize=tamanho_fonte,
                fontStyle="oblique",
            )
        )
        .properties(height=altura_grafico)  # Define a altura do gráfico
    )

    return chart


grafico = criar_grafico_barra(df_grafico, df_group_list, altura_grafico)
st.altair_chart(grafico, use_container_width=True)

# Adiciona o botão "Próxima página" abaixo do gráfico
col1, col2, col3, col4, col5 = st.columns(5)
with col2:
    if st.button("empresas anteriores"):
        if st.session_state.page > 0:
            change_page(-1)

with col5:
    if st.button("próximas empresas"):
        change_page(1)

st.write(" ")
st.write(" ")
st.write(" ")


# Função que irá fazer o gráfico da pizza
def grafico_pie(dataframe):
    # Criando o gráfico de rosca com Plotly Express
    fig = px.pie(
        dataframe,
        values="Valor Recebido",
        names="Empresa Contratada",
        title="Distribuição do Contrato",
        hole=0.55,  # Define o tamanho do buraco no meio (0.55 = 55%)
        labels={"Valor Recebido": "Valor", "Empresa Contratada": "Empresa"},
        hover_data={"Valor Recebido": True, "Empresa Contratada": True},
    )

    # Atualizar as fatias do gráfico para mostrar porcentagem e rótulo
    fig.update_traces(textposition="inside", textinfo="percent")

    # Personalizar o hovertemplate
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percent}"
    )

    fig.update_layout(title_x=0.2)  # Centralizar o título

    return fig


df_filtro = (
    df.groupby(by=["Código", "Empresa Contratada"])["Valor Recebido"]
    .sum()
    .reset_index()
)
df_filtro_empresas = df_filtro[
    "Empresa Contratada"
].reset_index()  # Apenas coluna das empresas do df_filtro


def detalhes_contratos(empresa):
    contratos = df_filtro["Código"][
        df_filtro["Empresa Contratada"] == empresa
    ].to_list()
    for i, contrato in enumerate(contratos):
        df_filtro1 = df_filtro[
            df_filtro["Código"] == contrato
        ]  # Aqui teremos a lista das empresas contratadas dentro desse contrato específico
        df_filtro1 = df_filtro1[
            ["Empresa Contratada", "Valor Recebido"]
        ]  # Estamos deixando o dataframe apenas com essas duas colunas
        orgao = data1["Órgão Entidade"][data1["Código"] == contrato].iloc[0]
        data_compra = data1["Ano da Compra"][data1["Código"] == contrato].iloc[0]
        objeto = data1["Objeto da Compra"][data1["Código"] == contrato].iloc[0]
        valor = data1["Valor Total Homologado"][data1["Código"] == contrato].iloc[0]
        valor_formatado = (
            f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        col1, col2 = st.columns([3, 2])  # define a proporção das colunas

        with col1:
            if i == 0:
                st.write(" ")
            st.markdown(
                f"<p><span style='color:red;'>Contrato n° {i+1}:</span> <span '>{contrato}</span></p>",
                unsafe_allow_html=True,
            )
            # st.write(f"Contrato n° {i+1}: {contrato}")
            st.markdown(
                f"<p><span style='border-bottom: 2px solid red;'>Ano da compra</span>: {data_compra}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p><span style='border-bottom: 2px solid red;'>Órgão Responsável</span>: {orgao}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p><span style='border-bottom: 2px solid red;'>Objeto da compra do contrato</span>: {objeto}</p>",
                unsafe_allow_html=True,
            )
            # st.write(f"Objeto da compra do contrato: {objeto}")
            st.markdown(
                f"<p><span style='border-bottom: 2px solid red;'>Valor Total Homologado</span>: {valor_formatado}</p>",
                unsafe_allow_html=True,
            )
            st.write(" ")
            st.write(" ")

            code = contrato.split("-")[0]
            year = contrato.split("/")[1]
            sequencial = contrato.split("/")[0].split("-")[2]
            st.write(
                f"Para mais informações [clique aqui](https://pncp.gov.br/app/editais/{code}/{year}/{sequencial})"
            )

        with col2:
            pie = grafico_pie(df_filtro1)  # Adicionando o gráfico pie
            st.plotly_chart(pie)

        st.write("----")
    return contratos


def exibir_detalhes_empresa(df, empresa):
    if empresa in df["Razão social"].unique():
        empresa_info = df[df["Razão social"] == empresa].iloc[0]
        st.write("---")
        st.subheader(
            f"Detalhes da Empresa: {empresa_info['Razão social']} ({empresa_info['CNPJ']})"
        )

        col1, col2 = st.columns(2)

        with col1:
            if "Nome Fantasia" in empresa_info:
                st.write(f"**Nome Fantasia:** {empresa_info['Nome Fantasia']}")
            if "Situação Cadastral" in empresa_info:
                st.write(
                    f"**Situação Cadastral:** {empresa_info['Situação Cadastral']}"
                )
            if "Data da Situação Cadastral" in empresa_info:
                st.write(
                    f"**Data da Situação Cadastral:** {empresa_info['Data da Situação Cadastral']}"
                )
            if "Endereço UF" in empresa_info and "Endereço Município" in empresa_info:
                endereco = (
                    empresa_info.get("Endereço Município", "")
                    + ", "
                    + empresa_info.get("Endereço UF", "")
                )
                st.write(f"**Endereço:** {endereco}")
            if "Data de Início da Atividade" in empresa_info:
                st.write(
                    f"**Data de Início da Atividade:** {empresa_info['Data de Início da Atividade']}"
                )
            if (
                "CNAE fiscal principal" in empresa_info
                and "nome" in empresa_info["CNAE fiscal principal"]
            ):
                cnae_nome = empresa_info["CNAE fiscal principal"]["nome"]
                st.write(f"**CNAE Principal (Nome):** {cnae_nome}")

        with col2:
            if "Sócios" in empresa_info:
                socios = empresa_info.get("Sócios", [])
                if socios:
                    expander = st.expander(
                        "Sócios", expanded=False
                    )  # Definindo como fechado por padrão
                    for socio in socios:
                        with expander:
                            st.write(f"**{socio['nome']}** ({socio['tipo']})")
                            st.write(
                                f"   - **Documento:** {socio.get('doc', 'Não informado')}"
                            )
                            st.write(
                                f"   - **Data de entrada:** {socio.get('data_entrada', 'Não informada')}"
                            )
            else:
                st.write("**Sócios:** Não disponível")

    else:
        st.write("Empresa não encontrada.")


st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

coluna1, coluna2 = st.columns(2)
escolha = ["Escolha sua empresa"] + df_group_list
with coluna1:
    empresa_selecionada = st.selectbox(
        "Selecione a Empresa para ver detalhes dos contratos que ela participou: ",
        escolha,
    )
    # if empresa_selecionada != "Escolha sua empresa":
    #        st.session_state.empresa_nome = None  # Limpa a variável se a empresa selecionada foi alterada
    if empresa_selecionada == "Escolha sua empresa":
        with coluna2:
            empresa_nome = st.text_input("Digite o nome da empresa:")
            # if empresa_nome:
            #    empresa_selecionada = "Escolha sua empresa"  # Limpa a variável se o nome da empresa foi inserido

if empresa_selecionada != "Escolha sua empresa":
    exibir_detalhes_empresa(data2, empresa_selecionada)
    st.write("---")
    st.write("---")
    contratos = detalhes_contratos(empresa_selecionada)

elif empresa_nome:
    filtrando = df_filtro_empresas.drop_duplicates(
        subset="Empresa Contratada"
    )  # Retirando empresas Duplicadas, pois uma mesma empresa pode estar em vaários contratos, então ao buscar o nome dela, ela apareceria com se fossem diferentes
    filtrando = filtrando[
        filtrando["Empresa Contratada"].str.contains(
            empresa_nome, case=False, regex=True
        )
    ]
    lista_filtro = filtrando["Empresa Contratada"].tolist()

    if lista_filtro:
        st.write(" ")
        st.write(" ")
        st.write("Empresas encontradas:")
        for idx, empresa in enumerate(lista_filtro):
            but = st.button(empresa, key=f"btn_{idx}")
            if but:
                exibir_detalhes_empresa(data2, empresa)
                st.write(" ")
                st.write("---")
                contratos = detalhes_contratos(empresa)


def apply_dark_mode_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #0E1117;
            color: white;
        }
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        .stMarkdown, .stMarkdown p, .stHeader, .stText, .stTitle, .stSubtitle, .stImage, .caption {
            color: white;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# apply_dark_mode_css()
