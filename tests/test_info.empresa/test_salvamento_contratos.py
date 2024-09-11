import pytest
import os
import pandas as pd
from Dados.info_empresa import salvar_em_csv


def test_salvar_em_csv(tmp_path):
    # Dados fictícios para simular a entrada
    dados_teste = [
        {
            "Código": "123456",
            "Empresa Contratada": "Empresa Teste A",
            "CNPJ": "12.345.678/0001-00",
            "Valor Recebido": "10000.00",
            "Descrição": "Serviços prestados",
        },
        {
            "Código": "789101",
            "Empresa Contratada": "Empresa Teste B",
            "CNPJ": "98.765.432/0001-99",
            "Valor Recebido": "20000.00",
            "Descrição": "Fornecimento de produtos",
        },
    ]

    # Define o caminho do arquivo CSV temporário
    caminho_arquivo_csv = tmp_path / "empresas_contratadas_teste.csv"

    # Chama a função para salvar o CSV
    caminho_absoluto_csv = salvar_em_csv(dados_teste, caminho_arquivo_csv)

    # Verifica se o arquivo foi criado
    assert os.path.exists(caminho_absoluto_csv)

    # Carrega o CSV gerado especificando os tipos de dados
    df = pd.read_csv(caminho_absoluto_csv, dtype={"Código": str, "Valor Recebido": str})

    # Verifica se os dados no CSV são os esperados
    df_esperado = pd.DataFrame(dados_teste)

    pd.testing.assert_frame_equal(df, df_esperado)


# Novos testes para aumentar a cobertura


def test_salvar_em_csv_sem_dados(tmp_path):
    # Testa o salvamento com uma lista vazia de dados
    dados_teste = []

    caminho_arquivo_csv = tmp_path / "empresas_contratadas_vazio.csv"
    caminho_absoluto_csv = salvar_em_csv(dados_teste, caminho_arquivo_csv)

    assert os.path.exists(caminho_absoluto_csv)

    # Verifica se o arquivo CSV gerado está vazio
    with open(caminho_absoluto_csv, "r") as file:
        conteudo = file.read()
        assert conteudo.strip() == ""  # O arquivo deve estar vazio


@pytest.mark.filterwarnings(
    "ignore:Mismatched null-like values nan and None found:FutureWarning"
)
def test_salvar_em_csv_dados_nulos(tmp_path):
    # Testa o salvamento com dados contendo valores nulos
    dados_teste = [
        {
            "Código": "123456",
            "Empresa Contratada": "Empresa Teste A",
            "CNPJ": None,
            "Valor Recebido": "10000.00",
            "Descrição": None,
        }
    ]

    caminho_arquivo_csv = tmp_path / "empresas_contratadas_nulos.csv"
    caminho_absoluto_csv = salvar_em_csv(dados_teste, caminho_arquivo_csv)

    assert os.path.exists(caminho_absoluto_csv)

    # Carrega o CSV e força o tipo 'object' para todas as colunas
    df = pd.read_csv(caminho_absoluto_csv, dtype=str)

    # Converte a coluna CNPJ e Descrição para 'object' explicitamente
    df_esperado = pd.DataFrame(dados_teste).astype(
        {"CNPJ": "object", "Descrição": "object"}
    )

    pd.testing.assert_frame_equal(df, df_esperado)


def test_salvar_em_csv_tipo_incorreto(tmp_path):
    # Testa o salvamento com um dado do tipo incorreto
    dados_teste = [
        {
            "Código": 123456,  # Código como inteiro ao invés de string
            "Empresa Contratada": "Empresa Teste A",
            "CNPJ": "12.345.678/0001-00",
            "Valor Recebido": "10000.00",
            "Descrição": "Serviços prestados",
        }
    ]

    caminho_arquivo_csv = tmp_path / "empresas_contratadas_tipo_incorreto.csv"
    caminho_absoluto_csv = salvar_em_csv(dados_teste, caminho_arquivo_csv)

    assert os.path.exists(caminho_absoluto_csv)

    # Verifica se os dados no CSV são os esperados, corrigindo automaticamente o tipo de "Código"
    df = pd.read_csv(caminho_absoluto_csv, dtype={"Código": str, "Valor Recebido": str})

    # Corrige o tipo de dado esperado para a comparação
    df_esperado = pd.DataFrame(dados_teste)
    df_esperado["Código"] = df_esperado["Código"].astype(str)

    pd.testing.assert_frame_equal(df, df_esperado)


def test_salvar_em_csv_permissoes_arquivo(tmp_path):
    # Testa o comportamento quando o arquivo CSV não pode ser escrito devido a permissões
    dados_teste = [
        {
            "Código": "123456",
            "Empresa Contratada": "Empresa Teste A",
            "CNPJ": "12.345.678/0001-00",
            "Valor Recebido": "10000.00",
            "Descrição": "Serviços prestados",
        }
    ]

    # Cria um arquivo e remove permissões de escrita
    caminho_arquivo_csv = tmp_path / "empresas_contratadas_sem_permissao.csv"
    caminho_arquivo_csv.touch(0o444)  # Permissões de leitura somente

    # Tenta salvar no arquivo sem permissões e verifica se uma exceção é lançada
    with pytest.raises(PermissionError):
        salvar_em_csv(dados_teste, caminho_arquivo_csv)
