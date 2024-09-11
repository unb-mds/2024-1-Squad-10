import pytest
import pandas as pd
from Dados.ordenacao_dados import (
    replace_semicolon,
    expand_contracts,
    read_file_contratos,
    merge,
    remove_duplicadas,
    arredonda_valores,
)


def test_replace_semicolon():
    test_input = {
        "key1": "value;with;semicolon",
        "key2": ["another;value", "test;value"],
    }
    expected_output = {
        "key1": "value/with/semicolon",
        "key2": ["another/value", "test/value"],
    }
    result = replace_semicolon(test_input)
    assert result == expected_output


def test_expand_contracts():
    test_input = [
        {
            "Modalidade": "Modalidade 1",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa A",
                "CNPJ -1": "12345678000195",
                "Valor Recebido -1": 1000,
                "Descrição -1": "Descrição A",
            },
        },
        {
            "Modalidade": "Modalidade 2",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa B",
                "CNPJ -1": "98765432000196",
                "Valor Recebido -1": 1500,
                "Descrição -1": "Descrição B",
                "Empresa Contratada -2": "Empresa C",
                "CNPJ -2": "12345678000197",
                "Valor Recebido -2": 2000,
                "Descrição -2": "Descrição C",
            },
        },
    ]
    expected_output = [
        {
            "Modalidade": "Modalidade 1",
            "Empresa Contratada": "Empresa A",
            "CNPJ": "12345678000195",
            "Valor Recebido": 1000,
            "Descrição": "Descrição A",
        },
        {
            "Modalidade": "Modalidade 2",
            "Empresa Contratada": "Empresa B",
            "CNPJ": "98765432000196",
            "Valor Recebido": 1500,
            "Descrição": "Descrição B",
        },
        {
            "Modalidade": "Modalidade 2",
            "Empresa Contratada": "Empresa C",
            "CNPJ": "12345678000197",
            "Valor Recebido": 2000,
            "Descrição": "Descrição C",
        },
    ]
    result = expand_contracts(test_input)
    assert result == expected_output


@pytest.fixture
def test_df():
    return pd.DataFrame(
        {
            "Modalidade": ["Modalidade 1"],
            "Código": ["123"],
            "UF": ["SP"],
            "Órgão Entidade": ["Entidade A"],
            "Objeto da Compra": ["Objeto A"],
            "Ano da Compra": [2023],
            "Valor Total Estimado": [5000],
            "Valor Total Homologado": [4500],
            "Empresa Contratada": ["Empresa A"],
            "CNPJ": ["12345678000195"],
            "Valor Recebido": [4000],
            "Descrição": ["Descrição A"],
        }
    )


def test_read_file_contratos(test_df):
    expected_output_columns = [
        "Modalidade",
        "Código",
        "UF",
        "Órgão Entidade",
        "Objeto da Compra",
        "Ano da Compra",
        "Valor Total Estimado",
        "Valor Total Homologado",
        "Empresa Contratada",
        "CNPJ",
        "Valor Recebido",
        "Descrição",
    ]
    result = read_file_contratos(test_df)
    assert all(col in result.columns for col in expected_output_columns)


def test_merge():
    contratos_fila = pd.DataFrame(
        {
            "CNPJ": ["12345678000195"],
            "Modalidade": ["Modalidade 1"],
            "Valor Recebido": [4000],
        }
    )

    contratos_cnpj = pd.DataFrame(
        {
            "CNPJ": ["12345678000195", "98765432000196"],
            "Nome": ["Empresa A", "Empresa B"],
        }
    )

    expected_output = pd.DataFrame(
        {
            "CNPJ": ["12345678000195"],
            "Modalidade": ["Modalidade 1"],
            "Valor Recebido": [4000],
            "Nome": ["Empresa A"],
        }
    )
    result = merge(contratos_fila, contratos_cnpj)
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_output.reset_index(drop=True)
    )


def test_remove_duplicadas():
    test_df = pd.DataFrame(
        {
            "Código": ["A", "A", "B"],
            "Órgão Entidade": ["Entidade A", "Entidade A", "Entidade B"],
            "Objeto da Compra": ["Objeto A", "Objeto A", "Objeto B"],
            "Ano da Compra": [2023, 2023, 2023],
            "Valor Total Homologado": [5000, 5000, 3000],
            "Empresa Contratada": ["Empresa A", "Empresa A", "Empresa B"],
        }
    )

    expected_output = pd.DataFrame(
        {
            "Código": ["A", "B"],
            "Órgão Entidade": ["Entidade A", "Entidade B"],
            "Objeto da Compra": ["Objeto A", "Objeto B"],
            "Ano da Compra": [2023, 2023],
            "Valor Total Homologado": [5000, 3000],
            "Empresa Contratada": ["Empresa A", "Empresa B"],
        }
    )
    result = remove_duplicadas(test_df)
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_output.reset_index(drop=True)
    )


def test_arredonda_valores():
    test_df = pd.DataFrame(
        {
            "Valor Total Estimado": [1234.567, 9876.543],
            "Valor Total Homologado": [2345.678, 8765.432],
            "Valor Recebido": [3456.789, 7654.321],
        }
    )

    expected_output = pd.DataFrame(
        {
            "Valor Total Estimado": [1234.57, 9876.54],
            "Valor Total Homologado": [2345.68, 8765.43],
            "Valor Recebido": [3456.79, 7654.32],
        }
    )
    result = arredonda_valores(test_df)
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected_output.reset_index(drop=True)
    )
