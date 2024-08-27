import streamlit as st
from PIL import Image, ImageOps
import os

def apply_dark_mode_css():
    st.markdown("""
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
        """, unsafe_allow_html=True)

def resize_image(image_path, size=(150, 150)):
    img = Image.open(image_path)
    img = ImageOps.fit(img, size, Image.LANCZOS)
    return img

#apply_dark_mode_css()

st.header('Sobre nós')
st.write("""
    O projeto tem como objetivo principal garantir a transparência nos gastos públicos, proporcionando acesso fácil e compreensível às informações sobre contratos de dispensas de licitação do governo com empresas no Distrito Federal. Por meio da coleta de dados da API do Portal Nacional de Contratações Públicas ([PNCP](https://www.gov.br/pncp/pt-br)), o projeto visa criar rankings e dashboards que evidenciem quais empresas recebem mais recursos por meio dessa modalidade e quais órgãos públicos são os maiores investidores.

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
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

