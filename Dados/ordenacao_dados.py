# lê os arquivos ('infos_cnpj_OFICIAL.json')
# ('contratos_OFICIAL.json', 'r', encoding='utf-8') 

# segrega cada item por fornecedor e salva arquivo csv para que possa ser trabalhado depois em 
#salva contratos_merged.to_csv('contratos_ordenados_completo.csv', index=False) 


import pandas as pd
import json

# Função para substituir ';' por '/' em todas as strings do dicionário
def replace_semicolon(data):
    if isinstance(data, dict):
        return {key: replace_semicolon(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_semicolon(item) for item in data]
    elif isinstance(data, str):
        return data.replace(';', '/')
    else:
        return data

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

def read_file_contratos(df):
    # Lista das colunas que precisam ser replicadas
    replicated_cols = ['Modalidade', 'Código', 'UF', 'Órgão Entidade', 'Objeto da Compra', 'Ano da Compra', 'Valor Total Estimado', 'Valor Total Homologado']

    # Lista para armazenar as novas linhas
    new_rows = []

    # Processar cada linha do DataFrame original
    for _, row in df.iterrows():
        # Dicionário para a nova linha
        new_row = row[replicated_cols].to_dict()
        new_row.update({
            'Empresa Contratada': row['Empresa Contratada'],
            'CNPJ': str(row['CNPJ']).split('.')[0] if '.' in str(row['CNPJ']) else str(row['CNPJ']),
            'Valor Recebido': row['Valor Recebido'],
            'Descrição': row['Descrição']
        })
        new_rows.append(new_row)

    # Criar o DataFrame resultante de uma vez
    contratos_fila = pd.DataFrame(new_rows)

    # Salvar o DataFrame resultante em um novo arquivo CSV
    # Parece que pode ser excluído
    # contratos_fila.to_csv('output_arquivo_json.csv', index=False)

    # Retornar o DataFrame resultante
    return contratos_fila

def read_file_cnpj():
    #cnpj= pd.read_json('infos_cnpj_OFICIAL.json')
    #cadastros_cnpj = pd.read_csv('cnpj_oficial.csv', encoding='utf-8')
    cadastros_cnpj= pd.read_json('frontend/infos_cnpj_OFICIAL.json')
    cadastros_cnpj['Data de Início da Atividade'] = pd.to_datetime(cadastros_cnpj['Data de Início da Atividade'])

    # Extrair o ano e inserir a nova coluna imediatamente após 'Data de Início da Atividade'
    cadastros_cnpj.insert(cadastros_cnpj.columns.get_loc('Data de Início da Atividade') + 1, 'Ano de Início da Atividade', cadastros_cnpj['Data de Início da Atividade'].dt.year)

    # Retornar o DataFrame resultante
    return cadastros_cnpj

def merge(contratos_fila, contratos_cnpj):
    # Converter a coluna CNPJ em contratos_cnpj para string
    contratos_cnpj['CNPJ'] = contratos_cnpj['CNPJ'].astype(str)
    
    # Combinar os DataFrames com base na coluna CNPJ
    contratos_merged = pd.merge(contratos_fila, contratos_cnpj, on='CNPJ', how='left') 
    
    # Retornar o DataFrame resultante
    return contratos_merged

def verificar_diferenca(df):
    # Criar colunas para armazenar os valores ajustados
    contratos_fila=df
    contratos_fila['Valor Total Homologado Ajustado'] = contratos_fila['Valor Total Homologado'].astype(float)
    contratos_fila['Valor Total Estimado Ajustado'] = contratos_fila['Valor Total Estimado']

    # Processar cada 'Código' para manter o primeiro valor e definir os subsequentes para zero
    for code in contratos_fila['Código'].unique():
        mask = contratos_fila['Código'] == code
        first_index = contratos_fila[mask].index[0]
        contratos_fila.loc[mask, 'Valor Total Estimado Ajustado'] = 0
        contratos_fila.loc[mask, 'Valor Total Homologado Ajustado'] = 0
        contratos_fila.loc[first_index, 'Valor Total Estimado Ajustado'] = contratos_fila.loc[first_index, 'Valor Total Estimado']
        contratos_fila.loc[first_index, 'Valor Total Homologado Ajustado'] = contratos_fila.loc[first_index, 'Valor Total Homologado']

    # Remover as colunas originais e renomear as ajustadas
    contratos_fila = contratos_fila.drop(columns=['Valor Total Estimado', 'Valor Total Homologado'])
    contratos_fila = contratos_fila.rename(columns={
        'Valor Total Estimado Ajustado': 'Valor Total Estimado',
        'Valor Total Homologado Ajustado': 'Valor Total Homologado'
    })

    # Remover valores duplicados de Valor Total Homologado mantendo o primeiro e definindo os demais como zero
    contratos_fila['Valor Total Homologado Ajustado'] = contratos_fila.groupby('Código')['Valor Total Homologado'].transform(lambda x: x.where(x.index == x.idxmax(), 0))

    # Calcular a soma dos valores recebidos por Código
    soma_valor_recebido = contratos_fila.groupby('Código')['Valor Recebido'].sum().reset_index()
    soma_valor_recebido['Valor Recebido_Soma'] = soma_valor_recebido['Valor Recebido']

    # Juntar a soma dos valores recebidos com o DataFrame original
    contratos_fila = contratos_fila.merge(soma_valor_recebido[['Código', 'Valor Recebido_Soma']], on='Código', how='left')

    # Calcular a diferença entre o Valor Total Homologado e a soma dos Valores Recebidos
    contratos_fila['Diferença'] = (contratos_fila['Valor Total Homologado'] - contratos_fila['Valor Recebido_Soma']).round(2)

    # Remover duplicatas baseadas na coluna 'Código', mantendo apenas a primeira ocorrência
    resultado_final = contratos_fila.drop_duplicates(subset='Código', keep='first')

    # Salvar o DataFrame resultante em um novo arquivo CSV
    #resultado_final.to_csv('resultado_final_output2_diferenca limpo.csv', index=False)
    return resultado_final


def remove_duplicadas(df):
    # Remover duplicatas com base nas colunas especificadas
    df_sem_duplicatas = df.drop_duplicates(subset=['Código', 'Órgão Entidade', 'Objeto da Compra', 'Ano da Compra', 'Valor Total Homologado', 'Empresa Contratada'], keep='first')
    
    return df_sem_duplicatas

def arredonda_valores(df):
    # Remover duplicatas com base nas colunas especificadas
    df_arredondados = df.copy()  # Criar uma cópia do DataFrame original
    df_arredondados[['Valor Total Estimado', 'Valor Total Homologado', 'Valor Recebido']] = df_arredondados[['Valor Total Estimado', 'Valor Total Homologado', 'Valor Recebido']].round(2)
    
    return df_arredondados


# Carregar o arquivo JSON
with open('frontend/contratos_OFICIAL.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Substituir ';' por '/'
data = replace_semicolon(data)

# Expandir os contratos
expanded_data = expand_contracts(data)

# Converter a lista expandida em um DataFrame do Pandas
df = pd.DataFrame(expanded_data)
df.columns
# Salvar o DataFrame em um arquivo CSV
#df.to_csv('1contratos_ordenados_completo.csv', index=False, encoding='utf-8')

#print("Arquivo CSV gerado com sucesso!")

# Chamar as funções e usar o resultado
contratos_fila = read_file_contratos(df)
contratos_cnpj = read_file_cnpj()
contratos_merged = merge(contratos_fila, contratos_cnpj) #avaliar a necessidade de puxar o cadastro das empresas
#contratos_merged=remove_duplicadas(contratos_merged) # desativado pq troquei no dash valor homologado por valor recebido
contratos_merged= arredonda_valores(contratos_merged)

# Salvar a base de dados combinada
contratos_merged.to_csv('contratos_ordenados_completo.csv', index=False) # ajustei estava ('contratos_ordenados_completos.csv')

# Verificar diferenças
diferencas = verificar_diferenca(contratos_merged)

# Salvar a base de dados resultante das diferenças - usado para ratrear 
#diferencas.to_csv('resultado_final_output2_diferenca.csv', index=False)

print("ordenado com sucesso")


