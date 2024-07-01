import streamlit as st
import requests
import re

# Função para validar email
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

# Função para enviar formulário ao Formspree
def send_formspree(name, email, subject, message):
    formspree_url = 'https://formspree.io/f/xvoenqdp'  # Endpoint do seu Formspree
    data = {  # Dicionário com a mensagem que será enviada para o formspree
        'NOME': name,
        'EMAIL': email,
        'ASSUNTO': subject,
        'MENSAGEM': message
    }
    response = requests.post(formspree_url, data=data)  # Envia uma solicitação POST para o endpoint do Formspree com os dados do formulário.
    return response.status_code == 200

# Função para verificar se o campo nome está preenchido
def is_name_filled(name):
    return bool(name)

# Função para verificar se o campo mensagem está preenchido
def is_message_filled(message):
    return bool(message)

st.title("Fale Conosco")
st.markdown("### Formulário")
st.markdown("Entre em contato com a equipe desenvolvedora desse projeto usando o formulário abaixo:")

with st.form(key='contact_form'):
    name = st.text_input("Nome")
    email = st.text_input("Email")
    subject = st.selectbox("Assunto", [
        "",  # Opção padrão
        "Suporte técnico",
        "Feedback sobre o site",
        "Sugestões de melhorias",
        "Dúvidas gerais",
        "Relatório de problemas/bugs",
        "Solicitação de funcionalidades",
        "Parcerias e colaborações",
        "Consultas sobre dados",
        "Outro"
    ])
    message = st.text_area("Mensagem")
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        name_filled = is_name_filled(name)
        email_valid = is_valid_email(email)
        message_filled = is_message_filled(message)
        subject_selected = subject != ""  # Verifica se um assunto válido foi selecionado

        if not name_filled:
            st.error("O campo Nome é obrigatório.")
        if not email_valid:
            st.error("E-mail inválido.")
        if not message_filled:
            st.error("O campo Mensagem é obrigatório.")
        if not subject_selected:
            st.error("Por favor, selecione um assunto.")

        if name_filled and email_valid and message_filled and subject_selected:
            if send_formspree(name, email, subject, message):
                st.success("Sua mensagem foi enviada com sucesso!")
            else:
                st.error("Ocorreu um erro ao enviar sua mensagem. Tente novamente.")

# Divisória para o rodapé
#st.write("---")

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
