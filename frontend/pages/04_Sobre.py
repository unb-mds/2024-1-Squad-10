import streamlit as st
from PIL import Image, ImageOps
import os

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

def resize_image(image_path, size=(150, 150)):
    img = Image.open(image_path)
    img = ImageOps.fit(img, size, Image.ANTIALIAS)
    return img

apply_dark_mode_css()

st.header('Sobre nós')
st.write("""
    O projeto tem como objetivo principal garantir a transparência nos gastos públicos, proporcionando acesso fácil e compreensível às informações sobre contratos de dispensas de licitação do governo com empresas. Por meio da coleta de dados da API do Portal Nacional de Contratações Públicas ([PNCP](https://www.gov.br/pncp/pt-br)), o projeto visa criar rankings e dashboards que evidenciem quais empresas recebem mais recursos por meio dessa modalidade e quais órgãos públicos são os maiores investidores.

    Este projeto é desenvolvido como parte da disciplina Métodos de Desenvolvimento de Software ([MDS](https://mds.lappis.rocks/)) da Universidade de Brasília ([UnB](https://www.unb.br/)), proporcionando aos alunos a oportunidade de aplicar os conhecimentos adquiridos em um contexto real e de relevância social.
""")
st.header('Participantes')

# Defina o caminho absoluto para a pasta de imagens
image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/imagens'))

def get_image_path(image_name):
    return os.path.join(image_folder, image_name)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(resize_image(get_image_path('mateus.png')), caption='Mateus de Castro')

with col2:
    st.image(resize_image(get_image_path('romulo.png')), caption='Rômulo de Araújo')

with col3:
    st.image(resize_image(get_image_path('lindo.png')), caption='Davi de Aguiar')

with col4:
    st.image(resize_image(get_image_path('henrique.jpeg')), caption='Henrique Carvalho')

col5, col6, col7 = st.columns(3)

with col5:
    st.image(resize_image(get_image_path('rafa.png')), caption='Rafael Melo')

with col6:
    st.image(resize_image(get_image_path('Pedrolock.jpeg')), caption='Pedro Lock')

with col7:
    st.image(resize_image(get_image_path('clara.jpeg')), caption='Maria Clara')
