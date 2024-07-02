import streamlit as st

def main():
    # Incorporando o CSS principal (style.css)
    try:
        with open('css/style1.css', 'r', encoding='utf-8') as file:
            style_css = file.read()
        st.markdown(f'<style>{style_css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'style1.css' não encontrado!")

    # Incorporando o CSS de responsividade (responsividade.css)
    try:
        with open('css/responsividade.css', 'r', encoding='utf-8') as file:
            responsividade_css = file.read()
        st.markdown(f'<style>{responsividade_css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'responsividade.css' não encontrado!")

    # Carregando e exibindo o conteúdo do index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            index_html = file.read()
        st.markdown(index_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'index.html' não encontrado!")

    # Carregando e exibindo o conteúdo do about.html
    try:
        with open('about.html', 'r', encoding='utf-8') as file:
            about_html = file.read()
        st.markdown(about_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'about.html' não encontrado!")

    # Exemplo de continuação do seu aplicativo Streamlit
    st.title('Meu Aplicativo Streamlit')
    st.write('Aqui vai o conteúdo do seu aplicativo...')

    # Exemplo de uso de widgets no Streamlit
    st.subheader('Exemplo de Widget:')
    user_input = st.text_input('Digite algo aqui:')
    st.write('Você digitou:', user_input)

if __name__ == '__main__':
    main()
