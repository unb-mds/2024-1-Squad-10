import pytest
from Dados.info_empresa import processar_contratos


def test_processar_contratos_dados_incompletos():
    # Testa com dados incompletos, onde o CNPJ está faltando
    dados_teste = [
        {
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                # "CNPJ -1" está faltando
                "Valor Recebido -1": "10000.00",
                "Descrição -1": "Serviços prestados",
            },
        }
    ]
    # Verifica se um KeyError é levantado quando o CNPJ está faltando
    with pytest.raises(KeyError, match="CNPJ -1"):
        processar_contratos(dados_teste)


def test_processar_contratos_formato_incorreto():
    # Testa com dados em formato incorreto para o Valor Recebido
    dados_teste = [
        {
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                "CNPJ -1": "12.345.678/0001-00",
                "Valor Recebido -1": "dez mil",  # Formato incorreto
                "Descrição -1": "Serviços prestados",
            },
        }
    ]

    # Tenta processar os contratos e verifica se o valor recebido está em formato incorreto
    resultado_obtido = processar_contratos(dados_teste)

    # Verifica se ocorre um ValueError quando o valor recebido não pode ser convertido para float
    for item in resultado_obtido:
        with pytest.raises(
            ValueError, match="could not convert string to float: 'dez mil'"
        ):
            float(item["Valor Recebido"])


def test_processar_contratos_valor_recebido_faltando():
    # Testa com dados onde o Valor Recebido está faltando
    dados_teste = [
        {
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                "CNPJ -1": "12.345.678/0001-00",
                # "Valor Recebido -1" está faltando
                "Descrição -1": "Serviços prestados",
            },
        }
    ]
    # Verifica se um KeyError é levantado quando o Valor Recebido está faltando
    with pytest.raises(KeyError, match="Valor Recebido -1"):
        processar_contratos(dados_teste)


def test_processar_contratos_descricao_faltando():
    # Testa com dados onde a Descrição está faltando
    dados_teste = [
        {
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                "CNPJ -1": "12.345.678/0001-00",
                "Valor Recebido -1": "10000.00",
                # "Descrição -1" está faltando
            },
        }
    ]
    # Verifica se um KeyError é levantado quando a Descrição está faltando
    with pytest.raises(KeyError, match="Descrição -1"):
        processar_contratos(dados_teste)


def test_processar_contratos_valores_numericos():
    # Testa com dados onde os valores são numericamente corretos
    dados_teste = [
        {
            "Código": "123456",
            "Empresas Contratadas": {
                "Empresa Contratada -1": "Empresa Teste A",
                "CNPJ -1": "12.345.678/0001-00",
                "Valor Recebido -1": "10000.00",
                "Descrição -1": "Serviços prestados",
            },
        }
    ]
    # Processa os contratos e verifica se os valores numéricos estão corretos
    resultado_obtido = processar_contratos(dados_teste)

    # Converte os valores recebidos para float e verifica se não ocorre erro
    for item in resultado_obtido:
        assert float(item["Valor Recebido"]) == 10000.00
