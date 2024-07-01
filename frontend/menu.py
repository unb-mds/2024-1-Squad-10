import streamlit as st
import streamlit.components.v1 as components
import base64
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")

# Função para carregar o conteúdo do arquivo
def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Função para carregar uma imagem e convertê-la para base64
def load_image_base64(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Carregar o HTML e CSS
html_content = load_file('index.html')
css_content = load_file('style.css')

# Carregar e codificar as imagens
logo_base64 = load_image_base64('images/licitanow.png')
licitacao_base64 = load_image_base64('images/licitacao.png')

# Atualizar o HTML com as imagens base64
html_content = html_content.replace('images/licitanow.png', f'data:image/png;base64,{logo_base64}')
html_content = html_content.replace('images/licitacao.png', f'data:image/png;base64,{licitacao_base64}')

# Injetar o CSS no HTML
html_with_css = f"""
    <style>
    {css_content}
    </style>
    {html_content}
"""

# Crie as colunas
col1, col2, col3, col4 = st.columns(4)

# Manipula os cliques nos botões
with col1:
    if st.button("Home"):
        st.write("Página Home")

with col2:
    if st.button("Ranking Empresas"):
        switch_page("rank_empresas")
with col3:
    if st.button("Serviços"):
        st.write("Página Serviços")

with col4:
    if st.button("Contato"):
        switch_page("contato")

# Exibir o HTML com CSS no Streamlit
components.html(html_with_css, height=800, scrolling=False)
