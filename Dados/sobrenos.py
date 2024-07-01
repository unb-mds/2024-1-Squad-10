import streamlit as st

def apply_dark_mode_css():
    st.markdown("""
        <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
            color: white;
        }
        .stMarkdown, .stMarkdown p, .stHeader, .stText, .stTitle, .stSubtitle, .stImage, .caption {
            color: white;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

apply_dark_mode_css()

st.header('Sobre nós')
st.write("""
    O projeto tem como objetivo principal garantir a transparência nos gastos públicos, proporcionando acesso fácil e compreensível às informações sobre contratos de dispensas de licitação do governo com empresas. Por meio da coleta de dados da API do Portal Nacional de Contratações Públicas ([PNCP](https://www.gov.br/pncp/pt-br)), o projeto visa criar rankings e dashboards que evidenciem quais empresas recebem mais recursos por meio dessa modalidade e quais órgãos públicos são os maiores investidores.

    Este projeto é desenvolvido como parte da disciplina Métodos de Desenvolvimento de Software ([MDS](https://mds.lappis.rocks/)) da Universidade de Brasília ([UnB](https://www.unb.br/)), proporcionando aos alunos a oportunidade de aplicar os conhecimentos adquiridos em um contexto real e de relevância social.
""")
st.header('Participantes')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(r'C:\Users\olavo\OneDrive\Pictures\Screenshots\Mateus.png', caption='Mateus de Castro', width=150)

with col2:
    st.image(r'C:\Users\olavo\OneDrive\Pictures\Screenshots\Rômulo.png', caption='Rômulo de Araújo', width=150)

with col3:
    st.image(r'C:\Users\olavo\OneDrive\Pictures\Screenshots\Davi.png', caption='Davi de Aguiar', width=150)

with col4:
    st.image(r'C:\Users\olavo\Downloads\henrique.jpeg', caption='Henrique Carvalho', width=150)

col5, col6, col7 = st.columns(3)

with col5:
    st.image(r'C:\Users\olavo\OneDrive\Pictures\Screenshots\Rafael.png', caption='Rafael Melo', width=150)

with col6:
    st.image(r'C:\Users\olavo\Downloads\Lock.jpeg', caption='Pedro Lock', width=150)

with col7:
    st.image(r'C:\Users\olavo\OneDrive\Pictures\Screenshots\clara.png', caption='Maria Clara', width=150)
