import requests
import json

url = 'https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao'
params = {
    'dataInicial': '20220101',
    'dataFinal': '20230101',
    'codigoModalidadeContratacao': '8',
    'pagina': '1'
}

response = requests.get(url, params=params)
dados = response.json()


with open('contratos1.json', 'w', encoding='utf-8') as f:
    f.write('[\n')
    for i, contrato in enumerate(dados['data']):
        contrato_data = {
            "cnpj": contrato['orgaoEntidade']['cnpj'],
            "razaoSocial": contrato['orgaoEntidade']['razaoSocial'],
            "objetoCompra": contrato['objetoCompra'],
            "anoCompra": contrato['anoCompra'],
            "valorTotalEstimado": contrato['valorTotalEstimado'],
            "valorTotalHomologado": contrato['valorTotalHomologado']
        }
        json.dump(contrato_data, f, ensure_ascii=False, indent=4)
        if i < len(dados['data']) - 1:
            f.write(',\n')
    f.write('\n]')
