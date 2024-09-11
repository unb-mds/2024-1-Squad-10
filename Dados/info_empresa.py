"""
Script para processar dados de contratos de um arquivo JSON e salvar em um arquivo CSV.
"""

import json
import os
import pandas as pd


def carregar_dados_json(caminho_arquivo_json):
    """Carrega e retorna os dados de um arquivo JSON."""
    with open(caminho_arquivo_json, "r", encoding="utf-8") as file:
        dados = json.load(file)
    return dados


def processar_contratos(dados):
    """Processa os dados dos contratos para extrair a estrutura desejada."""
    nova_estrutura = []

    for contrato in dados:
        codigo = contrato["Código"]
        empresas_contratadas = contrato["Empresas Contratadas"]

        for chave in empresas_contratadas:
            if chave.startswith("Empresa Contratada"):
                indice = chave.split(" -")[-1]

                novo_dict = {
                    "Código": codigo,
                    "Empresa Contratada": empresas_contratadas[
                        f"Empresa Contratada -{indice}"
                    ],
                    "CNPJ": empresas_contratadas[f"CNPJ -{indice}"],
                    "Valor Recebido": empresas_contratadas[f"Valor Recebido -{indice}"],
                    "Descrição": empresas_contratadas[f"Descrição -{indice}"],
                }

                nova_estrutura.append(novo_dict)

    return nova_estrutura


def salvar_em_csv(dados, caminho_arquivo_csv):
    """Salva os dados processados em um arquivo CSV."""
    df = pd.DataFrame(dados)
    df.to_csv(caminho_arquivo_csv, index=False, encoding="utf-8")
    return os.path.abspath(caminho_arquivo_csv)


def main():
    """Função principal que coordena o carregamento, processamento e salvamento dos dados."""
    caminho_arquivo_json = "frontend/contratos_OFICIAL.json"
    caminho_arquivo_csv = "frontend/x_empresas_contratadas.csv"

    # Carrega os dados do arquivo JSON
    dados = carregar_dados_json(caminho_arquivo_json)

    # Processa os dados dos contratos
    nova_estrutura = processar_contratos(dados)

    # Salva os dados processados em um arquivo CSV
    caminho_absoluto_csv = salvar_em_csv(nova_estrutura, caminho_arquivo_csv)

    print(f"O arquivo foi salvo em: {caminho_absoluto_csv}")
    print("Arquivo CSV criado com sucesso!")


if __name__ == "__main__":
    main()
