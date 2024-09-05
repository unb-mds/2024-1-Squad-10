import streamlit as st
from PIL import Image, ImageOps
import os


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


def resize_image(image_path, size=(150, 150)):
    img = Image.open(image_path)
    img = ImageOps.fit(img, size, Image.LANCZOS)
    return img


# apply_dark_mode_css()

st.header("Sobre nós")
st.write(
    """
### LicitaNow


### Projeto de Transparência nos Gastos Públicos - MDS UnB


### Documento do Produto - Projeto de Transparência nos Gastos Públicos


#### Visão Geral do Produto
O projeto de Transparência nos Gastos Públicos tem como objetivo proporcionar um acesso claro, fácil e compreensível às informações relacionadas aos contratos de dispensas de licitação entre o governo do Distrito Federal e empresas. Por meio da coleta de dados da API do Portal Nacional de Contratações Públicas (PNCP), o projeto se concentra em criar uma plataforma que facilite a visualização e análise desses dados, promovendo uma maior transparência e fiscalização das ações governamentais.


#### Propósito
O propósito do projeto é democratizar o acesso às informações sobre os gastos públicos, permitindo que cidadãos, jornalistas, pesquisadores e demais interessados possam acompanhar e entender como os recursos públicos estão sendo aplicados. O foco principal está em evidenciar a utilização das dispensas de licitação, uma modalidade frequentemente utilizada em contratos governamentais, e como essa prática impacta a distribuição de recursos no Distrito Federal.


#### Funcionalidades Principais
1. **Coleta Automatizada de Dados:**
   
    - Integração com a API do Portal Nacional de Contratações Públicas (PNCP) para a extração contínua de dados atualizados sobre contratos de dispensas de licitação.
   
2. **Rankings de Empresas e Órgãos Públicos:**
   
    - Geração de rankings que destacam as empresas que mais recebem recursos através de dispensas de licitação.
    - Listagem dos órgãos públicos que mais investem nessa modalidade, permitindo a análise de padrões e tendências.


3. **Dashboards Interativos:**
   
    - Criação de dashboards visuais e interativos que permitem aos usuários filtrar e explorar os dados de forma intuitiva.
    - Ferramentas de comparação para análise detalhada entre diferentes empresas e órgãos públicos.


4. **Visualizações Gráficas:**
   
    - Gráficos dinâmicos que facilitam a compreensão dos dados financeiros, mostrando, por exemplo, a evolução dos valores contratados ao longo do tempo e a distribuição geográfica dos contratos.


5. **Exportação de Dados:**
   
    - Opção de exportar os dados para diferentes formatos (CSV, Excel, PDF), permitindo que usuários realizem análises independentes ou utilizem os dados em outras plataformas.


#### Benefícios para os Usuários
- **Transparência e Acesso à Informação:** O projeto empodera os cidadãos com acesso simplificado às informações sobre os gastos públicos, promovendo a transparência e a accountability do governo.


- **Facilidade de Uso:** A plataforma foi desenvolvida com uma interface amigável, permitindo que usuários de diferentes níveis de conhecimento técnico possam navegar e entender os dados sem dificuldades.


- **Ferramenta de Fiscalização e Pesquisa:** Jornalistas, pesquisadores e organizações da sociedade civil podem utilizar os rankings e dashboards para monitorar as práticas governamentais, identificar possíveis irregularidades e embasar reportagens ou estudos.


- **Tomada de Decisões Informadas:** Os dados disponibilizados pela plataforma permitem que tomadores de decisão, tanto no setor público quanto privado, realizem análises fundamentadas sobre os contratos de dispensas de licitação, influenciando políticas públicas e estratégias de negócios.
         
### FUNCIONAMENTO DA PÁGINA "RANK EMPRESAS" E "RANK DOS ÓRGÃOS"


### Como Funciona a Página "Rank Empresas"
A página "Rank Empresas" é uma ferramenta que mostra quais empresas mais receberam dinheiro do governo do Distrito Federal através de contratos sem licitação. Esses contratos são feitos diretamente, sem um processo competitivo de escolha (como acontece em uma licitação tradicional).


**O que você vê na página:**


- **Gráfico de Barras:** No gráfico à direita, você pode ver uma lista das empresas que mais receberam recursos. As barras coloridas mostram quanto cada empresa recebeu em contratos. Quanto maior a barra, mais dinheiro a empresa recebeu.


- **Filtros para Personalização:**
  - Você pode selecionar a quantidade de empresas que deseja ver no gráfico, por exemplo, as 5, 10, ou 20 empresas que mais receberam dinheiro.


  - Também é possível ajustar os valores mínimos e máximos recebidos, para focar em empresas que receberam mais ou menos do que um certo valor.


- **Escolha Detalhes Específicos:**
   - Na parte de baixo da página, você pode escolher uma empresa específica para ver mais detalhes sobre os contratos que ela participou. Basta selecionar a empresa ou digitar o nome dela no campo correspondente.


Essa página ajuda você a entender para onde vai o dinheiro público e quais empresas estão mais envolvidas com o governo em contratos diretos. É uma ferramenta poderosa para quem quer acompanhar e fiscalizar o uso dos recursos públicos.


### Como Funciona a Página "Rank dos Órgãos"
A página "Rank dos Órgãos" é parte do projeto de Transparência nos Gastos Públicos e foi projetada para ajudar você a entender quais órgãos do governo do Distrito Federal mais utilizam contratos por dispensa de licitação.


**Elementos da Página:**


1. **Gráfico dos "Órgãos Campeões":**


    - **O que é:** Este gráfico mostra quais órgãos governamentais mais gastaram em contratos sem licitação.
    - **Como usar:** As barras representam os valores gastos por cada órgão. As cores diferentes ajudam a identificar cada órgão listado na legenda ao lado do gráfico.


2. **Gráfico de "Contratos Campeões":**


    - **O que é:** Este gráfico exibe os contratos mais caros feitos por órgãos do governo, ajudando a identificar quais foram as maiores transações.
    - **Como usar:** Aqui, você pode ver quais contratos específicos tiveram os valores mais altos, proporcionando uma visão clara das grandes movimentações financeiras.


3. **Gráfico de "Gasto Anual em Dispensa de Licitação por Órgão":**


    - **O que é:** Este gráfico mostra quanto cada órgão gastou em dispensas de licitação ao longo dos anos.
    - **Como usar:** Para visualizar o gráfico, você precisa digitar o nome do órgão de interesse. Isso permite uma pesquisa direcionada, mostrando as tendências de gastos desse órgão ao longo do tempo.


4. **Tabela de "Dados Compilados":**


    - **O que é:** Esta tabela resume todas as informações relevantes sobre os contratos, incluindo valores, datas, empresas contratadas e os órgãos envolvidos.
    - **Como usar:** A tabela é uma ferramenta poderosa para quem precisa de uma visão detalhada e compilada dos dados. Você pode usar os filtros disponíveis para buscar informações específicas.


5. **Filtros Personalizáveis:**


    - **Ano da Dispensa:** Permite selecionar contratos de anos específicos.
    - **Órgão Contratante:** Filtra os dados por um órgão governamental específico.
    - **Palavra-Chave no Objeto da Compra:** Você pode filtrar contratos por palavras-chave que aparecem na descrição da compra, como "coffee break", "lanche", etc.
    - **Nome da Empresa Contratada:** Permite ver apenas os contratos de uma determinada empresa.


6. **Navegação entre Páginas:**
   
    - A interface permite que você navegue entre diferentes páginas de dados para visualizar mais informações detalhadas caso elas não caibam em uma única página.
    - A página "Rank dos Órgãos" é uma ferramenta interativa que te dá uma visão detalhada e filtrada dos gastos públicos por diferentes órgãos governamentais no Distrito Federal. Ela permite acompanhar quais órgãos gastam mais em dispensas de licitação, visualizar os contratos mais caros, e analisar como esses gastos se distribuem ao longo do tempo.


"""
)
st.header("Participantes")

# Defina o caminho absoluto para a pasta de imagens
image_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../docs/imagens")
)


def get_image_path(image_name):
    return os.path.join(image_folder, image_name)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(resize_image(get_image_path("mateus.png")), caption="Mateus de Castro")

with col2:
    st.image(resize_image(get_image_path("romulo.png")), caption="Rômulo de Araújo")

with col3:
    st.image(resize_image(get_image_path("lindo.png")), caption="Davi de Aguiar")

with col4:
    st.image(resize_image(get_image_path("henrique.jpeg")), caption="Henrique Carvalho")

col5, col6, col7 = st.columns(3)

with col5:
    st.image(resize_image(get_image_path("rafa.png")), caption="Rafael Melo")

with col6:
    st.image(resize_image(get_image_path("Pedrolock.jpeg")), caption="Pedro Lock")

with col7:
    st.image(resize_image(get_image_path("clara.jpeg")), caption="Maria Clara")

# Rodapé estilizado usando HTML
footer = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    .footer a {
        color: #18bc9c;
        text-decoration: none;
        margin: 0 10px;
    }
    .footer a:hover {
        color: #148f77;
    }
    .footer .fa {
        margin-right: 8px;
    }
    </style>
    <div class="footer">
        <p>Desenvolvido por <a href="https://github.com/unb-mds/2024-1-Squad-10" target="_blank"><i class="fab fa-github"></i> Squad 10</a> | <a href="https://unb-mds.github.io/2024-1-Squad-10/" target="_blank"><i class="fas fa-file-alt"></i> Documentação</a> | <a href="mailto:licitanow.unb@gmail.com"><i class="fas fa-envelope"></i> Envie um E-mail</a></p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Adicionar suporte a ícones da Font Awesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">',
    unsafe_allow_html=True,
)
