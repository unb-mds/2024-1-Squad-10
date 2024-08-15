import pytest
from Dados.info_empresa import processar_contratos

def test_processar_contratos():
    # Dados fictícios para simular a entrada
    dados_teste = [
        {   
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                "CNPJ -1": "12.345.678/0001-00",
                "Valor Recebido -1": "10000.00",
                "Descrição -1": "Serviços prestados",
                "Empresa Contratada -2": "Empresa Teste B",
                "CNPJ -2": "98.765.432/0001-99",
                "Valor Recebido -2": "20000.00",
                "Descrição -2": "Fornecimento de produtos"
            }
        }
    ]
    
    # Resultado esperado após processar os contratos
    resultado_esperado = [
        {
            "Código": "123456",
            "Empresa Contratada": "Empresa Teste A",
            "CNPJ": "12.345.678/0001-00",
            "Valor Recebido": "10000.00",
            "Descrição": "Serviços prestados"
        },
        {
            "Código": "123456",
            "Empresa Contratada": "Empresa Teste B",
            "CNPJ": "98.765.432/0001-99",
            "Valor Recebido": "20000.00",
            "Descrição": "Fornecimento de produtos"
        }
    ]
    
    # Executa a função
    resultado_obtido = processar_contratos(dados_teste)
    
    # Verifica se o resultado obtido é igual ao esperado
    assert resultado_obtido == resultado_esperado
