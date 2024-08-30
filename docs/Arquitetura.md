# Arquitetura

## 1. Visão Geral

Este documento descreve a arquitetura do projeto de software desenvolvido em Python, cujo objetivo é analisar os dados de dispensa de licitação do Distrito Federal, identificar as empresas mais beneficiadas e os órgãos públicos mais investidores. A coleta e a análise dos dados são realizadas através de diversas bibliotecas e ferramentas, com atualizações automatizadas semanalmente.

## 2. Objetivos

- Analisar dados de dispensa de licitação no Distrito Federal.
- Identificar as empresas mais beneficiadas e os órgãos públicos mais investidores.
- Fornecer visualizações claras e intuitivas dos dados coletados.

## 3. Arquitetura Geral

### 3.1. Fluxo de Trabalho

#### 1) Extração e Coleta dos Dados

- **Coleta dos Contratos:**
- Feita através de requisições ao Portal Nacional de Contratações Públicas (PNCP) utilizando a biblioteca requests.
- Os dados são salvos em um arquivo JSON (contratos_OFICIAL.json).
- Erros de requisição são registrados em arquivos de log para tentativas subsequentes.
- **Coleta das Empresas:**
- Com base nos dados dos contratos, são realizadas requisições a uma API específica de empresas para coletar informações adicionais.
- Os dados são salvos em um arquivo JSON (infos_cnpjs_OFICIAL.json).

#### 2) Salvamento dos Dados

- Dados dos contratos salvos em contratos_OFICIAL.json.
- Dados das empresas salvos em infos_cnpjs_OFICIAL.json.

#### 3) Manipulação dos Dados

- Geração de um arquivo CSV (x_empresas_contratadas.csv) a partir dos dados dos contratos para facilitar a leitura dos dados das empresas contratadas.
- Criação de um arquivo CSV (contratos_ordenados_completos.csv) que combina os dados dos contratos e das empresas, utilizando a biblioteca pandas.

#### 4) Leitura dos Dados

- Leitura dos arquivos CSV gerados para análise e visualização dos dados.

#### 5) Análise e Visualização dos Dados

- Utilização do streamlit para criar dashboards e gráficos.
- Outras bibliotecas utilizadas incluem altair e plotly_express para visualizações adicionais.

### 3.2. Automação

- **GitHub Actions:** Automação semanal para atualização dos dados. Scripts definidos em arquivos .yml no GitHub.

## 4. Estrutura do Projeto

```
├── Dados
│   ├── Coleta_dados
│   │   ├── coleta_api.py
│   │   ├── coleta_cnpjs.py
│   │   ├── coleta_contratosERRO.py
│   │   ├── info.log
│   │   ├── info_erros.log
│   │   └── logging_config.py
│   ├── info_empresa.py
│   └── ordenacao_dados.py
└── frontend
    ├── Menu.py
    └── pages
        ├── 01_Rank_empresas.py
        ├── 02_Rank_dos_órgãos.py
        ├── 03_Contato.py
        └── 04_Sobre.py
```

## 5. Detalhamento dos Componentes

### 5.1 Coleta de Dados

- **coleta_api.py:** Script responsável por fazer as requisições ao PNCP e salvar os dados dos contratos em `contratos_OFICIAL.json`.
- **coleta_cnpjs.py:** Script que coleta informações adicionais das empresas a partir da API específica e salva os dados em `infos_cnpjs_OFICIAL.json`.
- **coleta_contratosERRO.py:** Script que reexecuta requisições que falharam, baseando-se nos logs de erros (`info_erros.log`).
- **logging_config.py:** Configuração de logs para registrar atividades e erros durante a coleta de dados.
- **info.log:** Arquivo de log para registros de atividades normais.
- **info_erros.log:** Arquivo de log para registros de erros.

### 5.2. Manipulação de Dados

- **info_empresa.py:** Script que manipula os dados das empresas.
- **ordenacao_dados.py:** Script que gera o arquivo `contratos_ordenados_completos.csv` combinando dados dos contratos e das empresas.

### 5.3. Frontend

- **Menu.py:** Script que define a página inicial de menu do dashboard.
- **pages/**
- **01_Rank_empresas.py:** Página que exibe o ranking das empresas mais beneficiadas.
- **02_Rank_dos_órgãos.py:** Página que exibe o ranking dos órgãos públicos mais investidores.
- **03_Contato.py:** Página de contato.
- **04_Sobre.py:** Página com informações sobre o projeto.

## 6. Bibliotecas Utilizadas

- **requests:** Para fazer requisições HTTP e coletar dados.
- **pandas:** Para manipulação e análise dos dados.
- **streamlit:** Para criação de dashboards interativos.
- **altair:** Para visualização de dados.
- **plotly_express:** Para visualização de dados.
- **json:** Para manipulação de arquivos JSON.
- **unidecode:** Para normalização de texto.

### Introdução

O projeto LicitaNow visa verificar e mostrar aos usuários os gastos públicos do Distrito Federal na modalidade dispensa de licitação. Tendo como objetivo apresentar, de forma organizada, quais empresas recebem mais dinheiro e quais são os órgãos públicos que gastam mais.

### Diagrama de arquitetura

![image](https://github.com/user-attachments/assets/b7bcae6a-868b-4908-982a-758a2fc08d1a)

### Front-End

#### HTML, CSS e JavaScript

- *Estrutura e Estilo:* Para criar a interface inicial do nosso projeto, utilizamos HTML para estruturar o conteúdo e CSS para estilizar os elementos. Além disso, utilizamos JavaScript para adicionar interatividade à página.
- *Conteúdo Principal:* O HTML define a estrutura básica da página, incluindo cabeçalho, seções de conteúdo, e rodapé. O CSS é responsável pela aparência visual, incluindo cores, espaçamentos, e fontes. O JavaScript adiciona comportamento dinâmico, como animações e reações a eventos de usuário.

#### Integração com Streamlit

- *Incorporação de HTML/CSS/JS no Streamlit:* Utilizamos a biblioteca streamlit.components.v1 para incorporar o nosso código HTML, CSS e JavaScript dentro do aplicativo Streamlit. Isso nos permitiu combinar a flexibilidade do desenvolvimento web tradicional com a simplicidade e o poder do Streamlit.
- *Código de Integração:* O código abaixo demonstra como carregamos e incorporamos os arquivos HTML, CSS e JavaScript no Streamlit:

        import streamlit as st
        import streamlit.components.v1 as components

        st.set_page_config(layout="wide")

        # Função para carregar o conteúdo do arquivo
        def load_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        # Carregar o HTML, CSS e JavaScript
        html_content = load_file('index.html')
        css_content = load_file('style.css')
        js_content = load_file('script.js')

        # Injetar o CSS e JavaScript no HTML
        html_with_css_js = f"""
            <style>
            html, body, [class*="css"]  {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }}
            {css_content}
            </style>
            <div style="width:100vw; height:100vh; overflow: hidden;">
                {html_content}
            </div>
            <script>
            {js_content}
            </script>
        # Exibir o HTML com CSS e JavaScript no Streamlit
        components.html(html_with_css_js, height=1000, scrolling=True)

### Back-End

#### Biblioteca Streamlit

- *Criação de Interfaces Interativas:* Utilizamos a biblioteca Streamlit para desenvolver o restante da interface do usuário e das funcionalidades interativas. Streamlit é uma ferramenta poderosa para criar dashboards e aplicativos de dados de maneira rápida e eficiente.
- *Funcionalidades:* Com Streamlit, implementamos funcionalidades como carregamento e visualização de dados, gráficos interativos, e controle de entradas do usuário (como sliders e botões).

#### Fluxo de Trabalho

- *Entrada de dados:* Os dados são carregados a partir de fontes especificadas (arquivos, APIs, etc.).
- *Processamento e Análise:* Os dados são processados e analisados em tempo real, utilizando bibliotecas de manipulação de dados.
- *Visualização:* Os resultados são apresentados de forma intuitiva através de gráficos, tabelas e outras visualizações interativas.

### Conclusão

A combinação de HTML, CSS e JavaScript para a estrutura e estilo inicial, junto com a biblioteca Streamlit para funcionalidades interativas e visualizações de dados, nos permitiu criar uma aplicação robusta e fácil de usar. Esta abordagem nos permitiu oferecer uma melhor combinação entre: a flexibilidade e personalização do desenvolvimento web tradicional, e a simplicidade e eficiência do Streamlit para análise de dados.

## 7. Automação e Atualização de Dados

- **GitHub Actions:** Arquivos `.yml` configurados para executar scripts de coleta e atualização de dados semanalmente, garantindo que as informações estejam sempre atualizadas.

Este documento detalha a arquitetura do projeto, incluindo o fluxo de trabalho, a estrutura de diretórios e scripts, além das bibliotecas e ferramentas utilizadas para alcançar os objetivos estabelecidos.

## Índice de Arquivos

### coleta_api.py

Faz buscas no API do PNCP, como resultado, ele gera um arquivo Json

#### coleta_cnpj.py

Faz buscas do cadastro de CNPJ na [API](https://api.cnpjs.dev/v1) utilizando o arquivo 'contratos_OFICIAL.json' e adiciona a ele o resultado das buscas.

#### ordenacao_dados.py

Organiza o arquivo Json para que possa ser lido pelo dashboard, consolida com as informações do arquivo "contrato_final1.xlsx", além de possíbilitar ao usuário que o baixe para trabalhá-lo em planilha Excel > Gera o arquivo "contratos_ordenados_completo.csv"

#### info_empresa.py

Verificar a necessidade de manter este arquivo, pois parece que não tem mais utilidade para o projeto

- Lê o arquivo"x_empresas_contratadas.json" e gera o arquivo 'x_empresas_contratadas.csv'

#### Rank_empresas.py

Página de arquivos do ranking das empresas

#### Rank_dos_órgãos.py

Página de arquivos do ranking dos órgãos conntratantes

#### Contato.py

Contato do organização do projeto

#### Sobre.py

Sobre nós

#### Menu.py

Menu do Dashboard Interativo
