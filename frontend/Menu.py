import os
import base64
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

def initialize_page():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_image_base64(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def get_file_paths(base_dir):
    return {
        "html": os.path.join(base_dir, 'index.html'),
        "css": os.path.join(base_dir, 'style.css'),
        "logo_image": os.path.join(base_dir, 'images', 'licitanow.png'),
        "licitacao_image": os.path.join(base_dir, 'images', 'licitacao.png'),
    }

def generate_html_with_css(html_content, css_content, logo_base64, licitacao_base64):
    html_content = html_content.replace('images/licitanow.png', f'data:image/png;base64,{logo_base64}')
    html_content = html_content.replace('images/licitacao.png', f'data:image/png;base64,{licitacao_base64}')
    
    return f"""
        <style>
        {css_content}
        </style>
        {html_content}
    """

def handle_button_clicks():
    col, col1, col2, col3, col4 = st.columns(5)
    
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

def main(base_dir):
    initialize_page()

    paths = get_file_paths(base_dir)

    html_content = load_file(paths["html"])
    css_content = load_file(paths["css"])
    logo_base64 = load_image_base64(paths["logo_image"])
    licitacao_base64 = load_image_base64(paths["licitacao_image"])

    html_with_css = generate_html_with_css(html_content, css_content, logo_base64, licitacao_base64)

    handle_button_clicks()

    components.html(html_with_css, height=800, scrolling=False)

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    main(current_dir)