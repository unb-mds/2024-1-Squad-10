# LicitaNow

## Sobre o projeto:
<p>O projeto tem como objetivo principal garantir a transparência nos gastos públicos, proporcionando acesso fácil e compreensível às informações sobre contratos de dispensas de licitação do governo com empresas no Distrito Federal. Por meio da coleta de dados da API do Portal Nacional de Contratações Públicas (PNCP), o projeto visa criar rankings e dashboards que evidenciem quais empresas recebem mais recursos por meio dessa modalidade e quais órgãos públicos são os maiores investidores.</p>

<hr/>

>  Este projeto é desenvolvido como parte da disciplina Métodos de Desenvolvimento de Software (MDS) da Universidade de Brasília (UnB), proporcionando aos alunos a oportunidade de aplicar os conhecimentos adquiridos em um contexto real e de relevância social.

## Funcionalidades 

- **1:** Rank das empresas: Dashboard das empresas que mais receberam por meio de dispensa de licitação, incluindo detalhes de quais foram os contratos que saomdos resultaram no valor total recebido por cada empresa.
- **2:** Rank dos órgãos: Dashboard dos órgãos que mais gastaram com dispensa de licitação, incluindo possibilidades de filtragem por objeto da compra, ano, nome do órgão e informações dos contratos campeões de cada órgão.
- **3:** Visualização dos contratos: com base no rank das empresas, o usuário tem a possibilidade de verificar os contratos que a empresa participou e ver detalher como distribuição do contrato, objeto da compra do contrato, o órgão que emitiu a dispensa e outras informações
- **4:** Informações detalhadas das empresas: ao selecionar uma empresa o usuário tem consegue ver qual o nome fantasia dessa empresa, quais são seus respectivos sócios, qual a data da situação cadastral, qual a data de fundação da empresa, CNAE da empresa, entre outros.
- **5:** Contato: possibilidade do usuário enviar mensagens para os contribuidores do projeto por meio do email.

## Documentação:
<p>Para acessar a documentação completa do projeto. <a href="https://unb-mds.github.io/2024-1-Squad-10/">Clique aqui.</a></p>

## Tecnologias Utilizadas

- **Linguagem de Programação:** Javascript, Python, HTML e CSS.
- **Prototipação:** Figma.
- **Framework Web:** Streamlit.
- **Banco de Dados:** Armazenamos os dados apenas em arquivos CSV/JSON.

## Clonar o Repositório

Para clonar o repositório do projeto, utilize o seguinte comando:

```bash
git clone https://github.com/unb-mds/2024-1-Squad-10.git
```

## Dependências do Projeto

Para rodar o projeto, você precisará das seguintes dependências:

- **Python**: v3.10.12 (ou superior)
- **Pip**: v22.0.2 (ou superior)

#### Bibliotecas

- **Streamlit**: v1.34.0
- **Streamlit-Extras**: v0.4.3
- **Pandas**: v2.2.2 (ou superior)
- **Plotly Express**: v0.4.1 (ou superior)
- **Plotly**: v5.22.0 (ou superior)
- **Altair**: v5.3.0 (ou superior)

## Instalação das Dependências

Para instalar as dependências do projeto, utilize o seguinte comando:

```bash
pip install -r requirements.txt
```

Certifique-se de que o arquivo `requirements.txt` contenha as seguintes linhas:

```
streamlit==1.34.0
streamlit-extras==0.4.3
pandas>=2.2.2
plotly-express>=0.4.1
plotly>=5.22.0
altair>=5.3.0
```

## Executando o Projeto

Para executar o projeto, navegue até a pasta `frontend` e utilize o comando:

```bash
streamlit run Meny.py
```

## Estrutura do Projeto

- **frontend/**: Contém os arquivos relacionados à interface criada com Streamlit.
  - `Meny.py`: Script principal do Streamlit que carrega e visualiza os dados.

- **data/**: Contém os arquivos CSV e JSON com os dados de dispensa de licitação.

## Integração com HTML/CSS/JS

O Streamlit permite a incorporação de código HTML, CSS e JavaScript diretamente nos scripts Python. Isso possibilita uma maior personalização da interface e a adição de funcionalidades avançadas que não são nativamente suportadas pelo Streamlit.

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou encontrar problemas, por favor, abra uma issue ou envie um pull request.


## Diagrama de Arquitetura: 
![image](https://github.com/unb-mds/2024-1-Squad-10/assets/145598542/4850441c-f750-410b-a8d8-c478e8ece700)

<p>Clique <a href="https://www.figma.com/board/NBvsCarJ03JDQZUAZ24csy/Diagrama-de-Arquitetura?node-id=0-1&t=O5K8SFcl7e9Cseye-0">aqui</a> para acessar o diagrama de arquitetura do projeto.

## 🗺 Story Map

Para entender melhor o fluxo do projeto e seu desenvolvimento, acesse o nosso story map [aqui](https://www.canva.com/design/DAGDRLpXv2w/ICrDLJTkKSMOxNdR-kHDwQ/view?utm_content=DAGDRLpXv2w&utm_campaign=designshare&utm_medium=link&utm_source=editor).

## 🖼 Protótipo

O protótipo da página web pode ser visualizado [aqui](https://www.figma.com/proto/Z24Pysy6Zc8B9sEKRKZV0C/TELA-DE-LOGIN-SIMPLES?type=design&node-id=9-73&t=vp5l9rFdzZuA5h6D-1&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=9%3A73).

## Equipe

| Nome                           |                           GitHub                           |
| :----------------------------- | :--------------------------------------------------------: |
| Davi Aguiar                    |[@davi-aguiar-vieira](https://github.com/davi-aguiar-vieira)|
| Henrique Carvalho              |[@henriquecarv3](https://github.com/henriquecarv3)          |
| Mateus de Castro               |[@mat054](https://github.com/mat054)                        |
| Maria Clara Alves              |[@alvezclari](https://github.com/alvezclari)                |
| Pedro Lock                     |[@PedroLock](https://github.com/PedroLock)                  |
| Rafael Matuda                  |[@9livesgod](https://github.com/9livesgod)                  |
| Romulo Reis                    |[@romuloreisdev](https://github.com/romuloreisdev)          |
