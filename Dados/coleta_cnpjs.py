#Faz buscas no API do CNPJ <https://api.cnpjs.dev>, como resultado, ele gera um arquivo "frontend\infos_CNPJ_OFICIAL.json"


import json
import requests

# Caminho do arquivo JSON
with open('infos_cnpj_OFICIAL.json', 'w', encoding='utf-8') as f:
    f.write('[\n')
    # Abre o arquivo JSON para leitura
    with open('contratos_OFICIAL.json', 'r', encoding='utf-8') as arquivo:
        # Carrega o conteúdo do arquivo como um objeto Python
        dados_json = json.load(arquivo)

        # Conjunto para armazenar CNPJs já processados
        cnpjs_processados = set()

        # Itera sobre cada item do arquivo JSON
        for item in dados_json:
            for chave, valor in item['Empresas Contratadas'].items():
                # Verifica se a chave começa com "CNPJ"
                if chave.startswith('CNPJ'):
                    if valor not in cnpjs_processados:
                        try:
                            # Tenta obter os dados do CNPJ
                            url = 'https://api.cnpjs.dev/v1/'+str(valor)
                            response = requests.get(url)

                            if response.status_code == 200:
                                data = response.json()
                                # Verifica se o CNPJ já foi processado antes                            
                                
                                informations = {
                                    "CNPJ" : data["cnpj"],
                                    "Razão social" : data["razao_social"],
                                    "Porte" : data["porte"],
                                    "Nome Fantasia" : data["nome_fantasia"],
                                    "Situação Cadastral" : data["situacao_cadastral"],
                                    "Data da Situação Cadastral" : data["data_situacao_cadastral"],
                                    "CNAE fiscal principal": data["cnae_fiscal_principal"],
                                    "Endereço UF" : data["endereco"]["uf"],
                                    "Endereço Município" : data["endereco"]["municipio"],
                                    "Data de Início da Atividade" : data["data_inicio_atividade"],
                                    "Sócios" : data["socios"]
                                }
                                nCNPJ = data["cnpj"]
                                print(nCNPJ)
                                json.dump(informations, f, ensure_ascii=False, indent=4)
                                f.write(',\n')
                                # Adiciona o CNPJ ao conjunto de CNPJs processados
                                cnpjs_processados.add(valor)
                        except KeyError:
                            # Se a chave 'cnpj' não for encontrada, continue para o próximo loop
                            continue
        f.seek(f.tell() - 3)  # Move o cursor de escrita de volta 3 caracteres
        f.truncate()  # Remove o último caractere (a vírgula)
        f.write('\n]')  # Escreve o fechamento da lista
