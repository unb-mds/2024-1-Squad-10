# ARQUIVO REFATORADO

import json
import csv
import requests
import time
import sys

# Cria a lista dos cnpjs, tira os repetidos e coloca em ordem crescente
def lista_cnpjs (arquivo):
    with open(arquivo,'r',encoding='utf-8') as file:
        dados_json = csv.reader(file)
        lista = [linha[-3] for linha in dados_json if (linha[-3].isnumeric() and len(linha[-3])==14)] # faz uma lista com o elemento -3, que corresponde ao cnpj
        lista_oficial = list(set(lista)) # retira os cnpjs duplicados
        lista_oficial.sort() # ordena em ordem crescente
    return lista_oficial

# Pega a lista e divide em 3 listas de tamanhos iguais
def lista_3_listas(lista):
    tamanho = len(lista) // 3
    return [lista[i * tamanho: (i + 1) * tamanho] for i in range(3)] # cria uma lista contendo 3 listas (cada uma com tamanhos semelhantes)


# retorna a lista das empresas contratadas
CNPJs = lista_cnpjs("frontend/x_empresas_contratadas.csv") # inicializa a primeira função
listas_cnpjs = lista_3_listas(CNPJs) # inicializa a segunda função

wait_time = 1
posicao = int(sys.argv[1])

print(len(listas_cnpjs[posicao])) # printa o tamanho da lista que iremos percorrer

with open('frontend/infos_cnpj_OFICIAL1.json', sys.argv[2], encoding='utf-8') as f:
    f.write(sys.argv[3])
    for index,cnpj in enumerate(listas_cnpjs[posicao]):
        wait_time =1
        time.sleep(5)

        for tentativa in range(5):
            try:
                # Tenta obter os dados do CNPJ
                url = f'https://api.cnpjs.dev/v1/{cnpj}'
                response = requests.get(url)
                response.raise_for_status()
                
                
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
                print(f"{nCNPJ} coletado com sucesso. Posição na fila: {index+1}")
                json.dump(informations, f, ensure_ascii=False, indent=4)
                if (cnpj == lista_cnpjs[posicao][-1]):
                    f.write(sys.argv[4])
                else:
                    f.write(',\n')
                break

            except:
                if (tentativa < 4):
                    time.sleep(wait_time) # Espera o wait time para fazer a próxima requisição
                    wait_time *= 2 # Dobra o tempo de espera para a próxima tentativa de requisição (caso exista)
                    print(f"Tentativa numero {tentativa} do CNPJ {cnpj}")
                else:
                    print(f"erro ao coletar dados do cnpj {cnpj}")


# Entrada no terminal: 
# python coleta_cnpj.py "0" "w" "[\n" ","
# python coleta_cnpj.py "1" "a" "\n" ","
# python coleta_cnpj.py "2" "a" "\n" "\n]"


