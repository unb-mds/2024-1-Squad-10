import requests
import json
import time
from logging_config import setup_logger_01

logger = setup_logger_01()  # Configura e obtém o logger

tentativas = 5
wait_time = 1


def get_resultados(contrato):
    tentativas = 5
    wait_time = 1
    tempo_espera = 1
    empresasContratadas = {}

    codigo = contrato["numeroControlePNCP"].split("-")[0]
    ano = contrato["anoCompra"]
    sequencial = contrato["numeroControlePNCP"].split("-")[2].split("/")[0]

    for tentativa in range(
        tentativas
    ):  # Ele irá tentar 5 vezes fazer o request novamente em caso de falha
        # Abaixo fiz o request para saber o número de itens de cada contratação (quantas empresas e serviços diferentes foram contratados dentro do mesmo contrato)
        try:
            link_nItem = (
                "https://pncp.gov.br/api/pncp/v1/orgaos/"
                + codigo
                + "/compras/"
                + str(ano)
                + "/"
                + sequencial
                + "/itens/quantidade"
            )
            requestItem = requests.get(link_nItem, headers={"accept": "*/*"})
            requestItem.raise_for_status()  # Levanta uma exceção para status de erro
            nItens = requestItem.json()

            if nItens != 0:
                for i in range(1, (nItens + 1)):
                    for tent in range(tentativas):
                        try:
                            # Vou fazer o request para pegar os resultados de cada item (contém informações como CNPJ da empresa, qual o nome da empresa contratada e o valor recebido)
                            url = (
                                "https://pncp.gov.br/api/pncp/v1/orgaos/"
                                + codigo
                                + "/compras/"
                                + str(ano)
                                + "/"
                                + sequencial
                                + "/itens/"
                                + str(i)
                                + "/resultados"
                            )
                            response = requests.get(url, headers={"accept": "*/*"})
                            response.raise_for_status()

                            # Abaixo fiz o request para pegar outros detalhes da contratação. No caso, iremos adicionar apenas a descrição do que a empresa está fornecendo
                            url_descricao = (
                                "https://pncp.gov.br/api/pncp/v1/orgaos/"
                                + codigo
                                + "/compras/"
                                + str(ano)
                                + "/"
                                + sequencial
                                + "/itens/"
                                + str(i)
                                + ""
                            )
                            request_descricao = requests.get(
                                url_descricao, headers={"accept": "*/*"}
                            )
                            request_descricao.raise_for_status()

                            data = (
                                response.json()
                            )  # JSON dos resultados do item escolhido
                            resultadoItem = data[0]
                            data_descricao = (
                                request_descricao.json()
                            )  # JSON da descrição do serviço, com base no item
                            empresasContratadas["Empresa Contratada -" + str(i)] = (
                                resultadoItem["nomeRazaoSocialFornecedor"]
                            )
                            empresasContratadas["CNPJ -" + str(i)] = resultadoItem[
                                "niFornecedor"
                            ]
                            empresasContratadas["Valor Recebido -" + str(i)] = (
                                resultadoItem["valorTotalHomologado"]
                            )
                            empresasContratadas["Descrição -" + str(i)] = (
                                data_descricao["descricao"]
                            )
                            break

                        except Exception as e:
                            if tent < tentativas - 1:
                                time.sleep(
                                    tempo_espera
                                )  # Espera o wait time para fazer a próxima requisição
                                tempo_espera *= 2  # Dobra o tempo de espera para a próxima tentativa de requisição (caso exista)
                                print(
                                    f"Quantidade de itens do contrato {contrato['numeroControlePNCP']} : {nItens}\nTentativa número {tent} do item numero {i} do request para pegar os resultados de cada item do contrato: {contrato['numeroControlePNCP']}"
                                )
                            else:
                                logger.error(
                                    f"Erro ao obter contrato: {contrato['numeroControlePNCP']} devido à inconsistência no item número {i}. Quantidade total de itens no contrato: {nItens}\nErro: {e}"
                                )
                                print(
                                    f"Erro ao obter contrato: {contrato['numeroControlePNCP']} \nErro: {e}"
                                )
                                return None

                return empresasContratadas

            else:
                return None
        except:
            if tentativa < tentativas - 1:
                time.sleep(
                    wait_time
                )  # Espera o wait time para fazer a próxima requisição
                wait_time *= 2  # Dobra o tempo de espera para a próxima tentativa de requisição (caso exista)
                print(
                    f"Tentativa número {tentativa} do request para saber o número de itens de cada contratação do contrato: {contrato['numeroControlePNCP']}"
                )
            else:
                print(f"Erro ao obter contrato: {contrato['numeroControlePNCP']}")
                return None


lista_contratos = []

with open("info01.log", "r") as arquivo_log:
    for linha in arquivo_log:
        parte_contrato = linha.split(":")[3]
        contract = parte_contrato.strip()
        lista_contratos.append(contract)

print(f"O tamanho da lista dos contratos é: {len(lista_contratos)}")
# lista_contratoss= ["00348003000110-1-000004/2021","00394452000103-1-000319/2021","00394452000103-1-000719/2021","33583550000130-1-000004/2021","08829974000194-1-000007/2021","00394452000103-1-001017/2021"]

with open("frontend/contratos_OFICIAL_versao3.json", "a", encoding="utf-8") as f:
    f.write("\n")
    for contrato in lista_contratos:
        cnpj = contrato.split("-")[0]
        ano = contrato.split("/")[1]
        sequencial = contrato.split("-")[2].split("/")[0]

        url = (
            f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}"
        )
        for tentativa in range(tentativas):
            try:
                response = requests.get(url, headers={"accept": "*/*"})
                response.raise_for_status()

                dados = response.json()

                if dados["valorTotalHomologado"] is not None:
                    empresasContratadas = get_resultados(dados)

                    if empresasContratadas:

                        contrato_data = {
                            "Modalidade": dados["modalidadeNome"],
                            "Código": dados["numeroControlePNCP"],
                            "UF": dados["unidadeOrgao"]["ufNome"],
                            "Órgão Entidade": dados["orgaoEntidade"]["razaoSocial"],
                            "Objeto da Compra": dados["objetoCompra"],
                            "Ano da Compra": dados["anoCompra"],
                            "Valor Total Estimado": dados["valorTotalEstimado"],
                            "Valor Total Homologado": dados["valorTotalHomologado"],
                            "Empresas Contratadas": empresasContratadas,
                        }
                        print(f"Novo contrato registrado com sucesso: {contrato}")
                        json.dump(contrato_data, f, ensure_ascii=False, indent=4)
                        f.write(",")
                break
            except:
                if tentativa < tentativas - 1:
                    time.sleep(
                        wait_time
                    )  # Espera o wait time para fazer a próxima requisição
                    wait_time *= 2  # Dobra o tempo de espera para a próxima tentativa de requisição (caso exista)
                    print(
                        f"Tentativa número {tentativa} do request inicial do contrato: {contrato}"
                    )
                else:
                    print(f"Nao foi possivel fazer o requeste do contrato: {contrato}")
