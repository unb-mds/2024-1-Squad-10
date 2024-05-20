import pandas as pd
import json

# Carregar o arquivo JSON
with open('contratos_OFICIAL.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Função para transformar contratos com múltiplas empresas contratadas em várias entradas
def expand_contracts(data):
    expanded_data = []
    for entry in data:
        base_contract = {key: value for key, value in entry.items() if key != 'Empresas Contratadas'}
        empresas_contratadas = entry.get('Empresas Contratadas', {})
        
        # Iterar sobre as empresas contratadas
        i = 1
        while f'Empresa Contratada -{i}' in empresas_contratadas:
            empresa_info = {
                'Empresa Contratada': empresas_contratadas.get(f'Empresa Contratada -{i}'),
                'CNPJ': empresas_contratadas.get(f'CNPJ -{i}'),
                'Valor Recebido': empresas_contratadas.get(f'Valor Recebido -{i}'),
                'Descrição': empresas_contratadas.get(f'Descrição -{i}')
            }
            contract_entry = {**base_contract, **empresa_info}
            expanded_data.append(contract_entry)
            i += 1
            
    return expanded_data

# Expandir os contratos
expanded_data = expand_contracts(data)

# Converter a lista expandida em um DataFrame do Pandas
df = pd.DataFrame(expanded_data)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('contratos_final.csv', index=False, encoding='utf-8')

print("Arquivo CSV gerado com sucesso!")
