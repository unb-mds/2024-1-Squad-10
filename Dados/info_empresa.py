import json
import pandas as pd

# Carrega o arquivo JSON original
with open('frontend/contratos_OFICIAL.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Lista para armazenar os novos dicionários
nova_estrutura = []

# Processa cada contrato no arquivo original
for contrato in dados:
    codigo = contrato["Código"]
    empresas_contratadas = contrato["Empresas Contratadas"]
    
    # Itera sobre as chaves de 'Empresas Contratadas'
    for chave in empresas_contratadas:
        if chave.startswith("Empresa Contratada"):
            indice = chave.split(" -")[-1]  # Descobre o índice da chave
            
            novo_dict = {
                "Código": codigo,
                "Empresa Contratada": empresas_contratadas[f"Empresa Contratada -{indice}"],
                "CNPJ": empresas_contratadas[f"CNPJ -{indice}"],
                "Valor Recebido": empresas_contratadas[f"Valor Recebido -{indice}"],
                "Descrição": empresas_contratadas[f"Descrição -{indice}"]
            }
            
            # Adiciona o novo dicionário à lista
            nova_estrutura.append(novo_dict)

df = pd.DataFrame(nova_estrutura)

df.to_csv('x_empresas_contratadas.csv', index=False, encoding='utf-8')
import os
print(f"O arquivo foi salvo em: {os.path.abspath('x_empresas_contratadas.csv')}")

print("Arquivo CSV criado com sucesso!")

# Salva a nova estrutura em um novo arquivo JSON
with open('x_empresas_contratadas.json', 'w', encoding='utf-8') as outfile:
    json.dump(nova_estrutura, outfile,ensure_ascii=False, indent=4)

print("Novo arquivo JSON criado com sucesso!")
