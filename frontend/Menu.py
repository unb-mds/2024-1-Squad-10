"""
Este módulo utiliza a biblioteca Streamlit para criar uma interface de 
usuário interativa com navegação entre páginas.
"""

import base64  # Importação da biblioteca padrão
import streamlit as st  # Importação de bibliotecas de terceiros
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page  # pylint: disable=import-error


st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

# Função para carregar o conteúdo do arquivo
def load_file(file_path):
    """
    Carrega o conteúdo de um arquivo dado o caminho especificado.

    Args:
        file_path (str): O caminho para o arquivo que será carregado.

    Returns:
        str: O conteúdo do arquivo como uma string.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Função para carregar uma imagem e convertê-la para base64
def load_image_base64(image_path):
    """
    Carrega uma imagem do caminho especificado e a codifica em uma string base64.

    Args:
        image_path (str): O caminho para o arquivo da imagem a ser carregada.

    Returns:
        str: A imagem codificada em base64 como uma string.
    """
    # Código principal aqui

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
html_content = html_content.replace(
    'images/licitacao.png',
    f'data:image/png;base64,{licitacao_base64}'
)


# Injetar o CSS no HTML
html_with_css = f"""
    <style>
    {css_content}
    </style>
    {html_content}
"""

# Crie as colunas
col ,col1, col2, col3, col4 = st.columns(5)

# Manipula os cliques nos botões
with col1:
    if st.button("Menu"):
        st.write("Página Menu")

with col2:
    if st.button("Ranking Empresas"):
        switch_page("rank_empresas")
with col3:
    if st.button("Ranking Órgãos"):
        switch_page("Rank_dos_órgãos")

with col4:
    if st.button("Contato"):
        switch_page("contato")

# Exibir o HTML com CSS no Streamlit
components.html(html_with_css, height=800, scrolling=False)
