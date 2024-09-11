import pytest
import importlib

contato_module = importlib.import_module("frontend.pages.03_Contato")
is_valid_email = contato_module.is_valid_email
is_name_filled = contato_module.is_name_filled
is_message_filled = contato_module.is_message_filled
validate_form = contato_module.validate_form


# Teste para validar email
def test_is_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("invalid-email") == False


# Teste para verificar se o campo nome está preenchido
def test_is_name_filled():
    assert is_name_filled("John Doe") == True
    assert is_name_filled("") == False


# Teste para verificar se o campo mensagem está preenchido
def test_is_message_filled():
    assert is_message_filled("Hello, this is a message.") == True
    assert is_message_filled("") == False


# Teste para validar o formulário
def test_validate_form():
    errors = validate_form("John Doe", "test@example.com", "Subject", "Message")
    assert errors == {
        "name_error": False,
        "email_error": False,
        "message_error": False,
        "subject_error": False,
    }

    errors = validate_form("", "invalid-email", "", "")
    assert errors == {
        "name_error": True,
        "email_error": True,
        "message_error": True,
        "subject_error": True,
    }


if __name__ == "__main__":
    pytest.main()
