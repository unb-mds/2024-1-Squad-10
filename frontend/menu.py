import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
# Função para carregar o conteúdo do arquivo
def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Carregar o HTML, CSS e JavaScript
html_content = load_file('index.html')
css_content = load_file('style.css')
js_content = load_file('script.js')

# Injetar o CSS e JavaScript no HTML
html_with_css_js = f"""
    <style>
    {css_content}
    </style>
    {html_content}
    <script>
    {js_content}
    </script>
"""

# Exibir o HTML com CSS e JavaScript no Streamlit
components.html(html_with_css_js, height=800, scrolling=True)