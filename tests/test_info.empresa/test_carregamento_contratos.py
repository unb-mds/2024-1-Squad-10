import pytest
import json
from Dados.info_empresa import carregar_dados_json

def test_carregar_dados_json(tmp_path):
    # Cria um conteúdo JSON de teste
    dados_teste = [
        {"Código": "123", "Empresas Contratadas": {"Empresa Contratada -1": "Empresa A", "CNPJ -1": "00.000.000/0001-00"}}
    ]

#Cria um arquivo JSON temporário usando pytest
    caminho_arquivo_json = tmp_path / "contratos_teste.json"
    with caminho_arquivo_json.open("w", encoding="utf-8") as file:
        json.dump(dados_teste, file)

#Executa a função e verifica se os dados carregados são os esperados
    dados_carregados = carregar_dados_json(caminho_arquivo_json)
    assert dados_carregados == dados_teste

    # Testa se uma exceção é levantada ao tentar carregar um arquivo inexistente
   # with pytest.raises(FileNotFoundError):
    #    carregar_dados_json("caminho_inexistente.json")