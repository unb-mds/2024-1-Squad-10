# Como Executar 

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