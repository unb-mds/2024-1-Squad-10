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
            "Descrição": "Serviços prestados"
        },
        {
            "Código": "789101",
            "Empresa Contratada": "Empresa Teste B",
            "CNPJ": "98.765.432/0001-99",
            "Valor Recebido": "20000.00",
            "Descrição": "Fornecimento de produtos"
        }
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