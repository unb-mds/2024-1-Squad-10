# test_coleta_api.py
import pytest
import requests
from unittest.mock import patch
from coleta_api import get_resultados  # Supondo que o nome do arquivo com a função seja coleta_api.py

# Mock para simular a resposta da API
def mock_get_request(url, headers):
    mock_response = requests.Response()
    mock_response.status_code = 200
    if 'quantidade' in url:
        mock_response._content = b'2'  # Simulando resposta para quantidade de itens
    else:
        mock_response._content = b'[{"nomeRazaoSocialFornecedor": "Empresa A", "niFornecedor": "123456789", "valorTotalHomologado": 1000.0}]'
    return mock_response

@pytest.mark.parametrize('contrato, expected_result', [
    ({'numeroControlePNCP': '123-2023/456', 'anoCompra': 2023, 'numeroControlePNCP': '456'}, 
     {'Empresa Contratada -1': 'Empresa A', 'CNPJ -1': '123456789', 'Valor Recebido -1': 1000.0}),
])
@patch('requests.get', side_effect=mock_get_request)
def test_get_resultados(mock_get, contrato, expected_result):
    result = get_resultados(contrato)
    assert result == expected_result
