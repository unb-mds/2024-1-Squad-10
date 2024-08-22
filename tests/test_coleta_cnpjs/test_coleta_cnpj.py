import pytest
import csv
from unittest.mock import mock_open,patch

# Importe a função que você deseja testar
from Dados.Coleta_dados.coleta_cnpjs import lista_cnpjs
from Dados.Coleta_dados.coleta_cnpjs import lista_3_listas


@pytest.fixture
def csv_content_valid():
    return (
        "Código,Empresa Contratada,CNPJ,Valor Recebido,Descrição\n"
        "00123456000189,Company A,12345678901234,1000.0,Service A\n"
        "00123456000190,Company B,98765432109876,2000.0,Service B\n"
        "00123456000191,Company C,12345678901234,1500.0,Service C\n"
    )

@pytest.fixture
def csv_content_invalid_cnpj():
    return (
        "Código,Empresa Contratada,CNPJ,Valor Recebido,Descrição\n"
        "00123456000189,Company A,abc,1000.0,Service A\n"
        "00123456000190,Company B,123,2000.0,Service B\n"
        "00123456000191,Company C,12345678901234,1500.0,Service C\n"
    )

@pytest.fixture
def csv_content_empty():
    return "Código,Empresa Contratada,CNPJ,Valor Recebido,Descrição\n"

@pytest.fixture
def lista ():
    return [1,2,3,4,5,6,7,8,9]

@pytest.fixture
def csv_content_varied_length():
    return (
        "Código,Empresa Contratada,CNPJ,Valor Recebido,Descrição\n"
        "00123456000192,Company D,123456789012,3000.0,Service D\n"
        "00123456000193,Company E,1234567890123456,4000.0,Service E\n"
        "00123456000194,Company F,12345678901234,2500.0,Service F\n"
    )

def test_lista_cnpjs_valid(csv_content_valid):
    with patch("builtins.open", mock_open(read_data=csv_content_valid)):
        result = lista_cnpjs("mock_file.csv")
        expected_result = ["12345678901234", "98765432109876"]
        assert result == expected_result


def test_lista_cnpjs_invalid_cnpj(csv_content_invalid_cnpj):
    with patch("builtins.open", mock_open(read_data=csv_content_invalid_cnpj)):
        result = lista_cnpjs("mock_file.csv")
        expected_result = ["12345678901234"]
        assert result == expected_result

def test_lista_cnpjs_empty(csv_content_empty):
    with patch("builtins.open", mock_open(read_data=csv_content_empty)):
        result = lista_cnpjs("mock_file.csv")
        expected_result = []
        assert result == expected_result

def test_lista_cnpjs_varied_length(csv_content_varied_length):
    with patch("builtins.open", mock_open(read_data=csv_content_varied_length)):
        result = lista_cnpjs("mock_file.csv")
        expected_result = ["12345678901234"]
        assert result == expected_result


def test_lista_divisivel_por_3():
    lista = [1, 2, 3, 4, 5, 6]
    resultado = lista_3_listas(lista)
    assert resultado == [[1, 2], [3, 4], [5, 6]]

def test_lista_nao_divisivel_por_3():
    lista = [1, 2, 3, 4, 5, 6, 7]
    resultado = lista_3_listas(lista)
    assert resultado == [[1, 2], [3, 4], [5, 6]]

def test_lista_vazia():
    lista = []
    resultado = lista_3_listas(lista)
    assert resultado == [[], [], []]

def test_lista_um_elemento():
    lista = [1]
    resultado = lista_3_listas(lista)
    assert resultado == [[], [], []]

def test_lista_dois_elementos():
    lista = [1, 2]
    resultado = lista_3_listas(lista)
    assert resultado == [[], [], []]
