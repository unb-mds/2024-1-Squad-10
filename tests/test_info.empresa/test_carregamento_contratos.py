import pytest
import json
import os
import platform
from unittest import mock
from Dados.info_empresa import carregar_dados_json


def test_carregar_dados_json_valido(tmp_path):
    dados_teste = [
        {"Código": "123", "Empresas Contratadas": {"Empresa Contratada -1": "Empresa A", "CNPJ -1": "00.000.000/0001-00"}}
    ]
    caminho_arquivo_json = tmp_path / "contratos_teste.json"
    with caminho_arquivo_json.open("w", encoding="utf-8") as file:
        json.dump(dados_teste, file)

    dados_carregados = carregar_dados_json(caminho_arquivo_json)
    assert dados_carregados == dados_teste

def test_carregar_dados_json_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        carregar_dados_json("caminho_inexistente.json")

def test_carregar_dados_json_malformado(tmp_path):
    caminho_arquivo_json = tmp_path / "contratos_malformado.json"
    with caminho_arquivo_json.open("w", encoding="utf-8") as file:
        file.write("{'Código': '123', 'Empresas Contratadas': 'Empresa A'}")

    with pytest.raises(json.JSONDecodeError):
        carregar_dados_json(caminho_arquivo_json)

def test_carregar_dados_json_vazio(tmp_path):
    caminho_arquivo_json = tmp_path / "contratos_vazio.json"
    caminho_arquivo_json.touch()  # Cria um arquivo vazio

    with pytest.raises(json.JSONDecodeError):
        carregar_dados_json(caminho_arquivo_json)

def test_carregar_dados_json_estrutura_incorreta(tmp_path):
    dados_teste = {"Código": "123"}  # Estrutura inesperada (falta chave "Empresas Contratadas")
    caminho_arquivo_json = tmp_path / "contratos_incorreto.json"
    with caminho_arquivo_json.open("w", encoding="utf-8") as file:
        json.dump(dados_teste, file)

    dados_carregados = carregar_dados_json(caminho_arquivo_json)
    assert dados_carregados == dados_teste  # Pode mudar dependendo do que a função deve fazer

def test_carregar_dados_json_permissao_negada(tmp_path):
    dados_teste = [{"Código": "123"}]
    caminho_arquivo_json = tmp_path / "contratos_permissao.json"
    with caminho_arquivo_json.open("w", encoding="utf-8") as file:
        json.dump(dados_teste, file)

    # Simula o PermissionError usando mock na função open
    with mock.patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            carregar_dados_json(caminho_arquivo_json)

def test_carregar_dados_json_none():
    with pytest.raises(TypeError):
        carregar_dados_json(None)

def test_carregar_dados_json_codificacao_diferente(tmp_path):
    dados_teste = [
        {"Código": "123", "Empresas Contratadas": {"Empresa Contratada -1": "Empresa A", "CNPJ -1": "00.000.000/0001-00"}}
    ]
    caminho_arquivo_json = tmp_path / "contratos_utf16.json"
    with caminho_arquivo_json.open("w", encoding="utf-16") as file:
        json.dump(dados_teste, file)

    with pytest.raises(UnicodeDecodeError):
        carregar_dados_json(caminho_arquivo_json)
