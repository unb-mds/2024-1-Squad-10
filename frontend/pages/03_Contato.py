import re
import requests
import streamlit as st

# Função para validar email
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

# Função para enviar formulário ao Formspree
def send_formspree(name, email, subject, message, formspree_url):
    data = {
        'NOME': name,
        'EMAIL': email,
        'ASSUNTO': subject,
        'MENSAGEM': message
    }
    response = requests.post(formspree_url, data=data)
    return response.status_code == 200

# Função para verificar se o campo nome está preenchido
def is_name_filled(name):
    return bool(name)

# Função para verificar se o campo mensagem está preenchido
def is_message_filled(message):
    return bool(message)

# Função para validar todo o formulário
def validate_form(name, email, subject, message):
    name_filled = is_name_filled(name)
    email_valid = is_valid_email(email)
    message_filled = is_message_filled(message)
    subject_selected = subject != ""  # Verifica se um assunto válido foi selecionado

    errors = {
        "name_error": not name_filled,
        "email_error": not email_valid,
        "message_error": not message_filled,
        "subject_error": not subject_selected
    }

    return errors

# Função para processar o envio do formulário
def process_form_submission(name, email, subject, message, formspree_url):
    errors = validate_form(name, email, subject, message)

    if not any(errors.values()):  # Se não houver nenhum erro
        success = send_formspree(name, email, subject, message, formspree_url)
        return {"success": success, "errors": errors}

    return {"success": False, "errors": errors}

# Função para renderizar a interface do usuário
def render_form_ui():
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
            formspree_url = 'https://formspree.io/f/xvoenqdp'
            result = process_form_submission(name, email, subject, message, formspree_url)

            if result["errors"]["name_error"]:
                st.error("O campo Nome é obrigatório.")
            if result["errors"]["email_error"]:
                st.error("E-mail inválido.")
            if result["errors"]["message_error"]:
                st.error("O campo Mensagem é obrigatório.")
            if result["errors"]["subject_error"]:
                st.error("Por favor, selecione um assunto.")

            if result["success"]:
                st.success("Sua mensagem foi enviada com sucesso!")
            elif not any(result["errors"].values()):
                st.error("Ocorreu um erro ao enviar sua mensagem. Tente novamente.")

def render_footer():
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

    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

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

# Função principal para rodar a aplicação
def main():
    apply_dark_mode_css()
    render_form_ui()
    render_footer()

if __name__ == "__main__":
    main()