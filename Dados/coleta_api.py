import requests
import json

def get_resultados(contrato):
    empresasContratadas = {}

    codigo = contrato['numeroControlePNCP'].split('-')[0]
    ano = contrato['anoCompra']
    sequencial = contrato['numeroControlePNCP'].split('-')[2].split('/')[0]

    # Abaixo fiz o request para saber o número de itens de cada contratação (quantas empresas e serviços diferentes foram contratados dentro do mesmo contrato)
    link_nItem = 'https://pncp.gov.br/api/pncp/v1/orgaos/'+codigo+'/compras/'+str(ano)+'/'+sequencial+'/itens/quantidade'
    requestItem = requests.get(link_nItem, headers={'accept': '*/*'})
    nItens = requestItem.json()

    if (requestItem.status_code ==200) and (nItens != 0):
        for i in range(1, (nItens+1)):

            # Vou fazer o request para pegar os resultados de cada item (contém informações como CNPJ da empresa, qual o nome da empresa contratada e o valor recebido)
            url = 'https://pncp.gov.br/api/pncp/v1/orgaos/'+codigo+'/compras/'+str(ano)+'/'+sequencial+'/itens/'+str(i)+'/resultados'
            response = requests.get(url, headers={'accept': '*/*'})

            # Abaixo fiz o request para pegar outros detalhes da contratação. No caso, iremos adicionar apenas a descrição do que a empresa está fornecendo
            url_descricao = 'https://pncp.gov.br/api/pncp/v1/orgaos/'+codigo+'/compras/'+str(ano)+'/'+sequencial+'/itens/'+str(i)+''
            request_descricao = requests.get(url_descricao, headers={'accept': '*/*'})

            if (response.status_code == 200) and (request_descricao.status_code == 200):
                data = response.json() # JSON dos resultados do item escolhido
                resultadoItem = data[0]
                data_descricao = request_descricao.json() # JSON da descrição do serviço, com base no item
                empresasContratadas['Empresa Contratada -'+str(i)] = resultadoItem['nomeRazaoSocialFornecedor']
                empresasContratadas['CNPJ -'+str(i)] = resultadoItem["niFornecedor"]
                empresasContratadas['Valor Recebido -'+str(i)] = resultadoItem["valorTotalHomologado"]
                empresasContratadas['Descrição -' + str(i)] = data_descricao["descricao"]
            else:
                return None
            
        return empresasContratadas   
      
    else:
        return None

pag =1
diaDt = 2
anoDt = 2021
ano_Dt=2022
mes = 1

dtInicial = str(anoDt) + '0'+ str(mes)+'0'+ str(diaDt)
dtFinal = str(ano_Dt) + '0'+ str(mes)+'0'+ str(diaDt-1)

with open('contratos_OFICIAL.json', 'w', encoding='utf-8') as f:
    f.write('[\n')

    while ano_Dt <= 2025:
        url = 'https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao'
        params = {
            'dataInicial': dtInicial,
            'dataFinal': dtFinal,
            'codigoModalidadeContratacao': '8',
            'uf' : 'df',
            'pagina': str(pag)
            }

        response = requests.get(url, params=params)
   

        if response.status_code == 200:
            dados = response.json()

        
            for contrato in dados['data']:
                if contrato['valorTotalHomologado'] is not None:
                    empresasContratadas = get_resultados(contrato)

                    if empresasContratadas:
                        

                        contrato_data = {
                            "Modalidade" : contrato["modalidadeNome"],
                            "Código" : contrato["numeroControlePNCP"],
                            "UF" : contrato["unidadeOrgao"]["ufNome"],
                            "Órgão Entidade": contrato['orgaoEntidade']['razaoSocial'],
                            "Objeto da Compra": contrato['objetoCompra'],
                            "Ano da Compra": contrato['anoCompra'],
                            "Valor Total Estimado": contrato['valorTotalEstimado'],
                            "Valor Total Homologado": contrato['valorTotalHomologado'],
                            "Empresas Contratadas" : empresasContratadas
                        }
                        numeroControlePNCP = contrato["numeroControlePNCP"]
                        print(numeroControlePNCP)
                        json.dump(contrato_data, f, ensure_ascii=False, indent=4)
                        f.write(',\n')                        
                
            pag +=1
        else:
            pag = 1
            anoDt = ano_Dt
            ano_Dt += 1
            dtInicial = str(anoDt) + '0'+ str(mes)+'0'+ str(diaDt)
            dtFinal = str(ano_Dt) + '0'+ str(mes)+'0'+ str(diaDt-1)
    f.seek(f.tell() - 3)  # Move o cursor de escrita de volta 3 caracteres
    f.truncate()  # Remove o último caractere (a vírgula)
    f.write('\n]')  # Escreve o fechamento da lista
    
