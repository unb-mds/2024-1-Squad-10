# DOCUMENTO DE ARQUITETURA DO PROJETO DE SOFTWARE

## 1. Visão Geral
Este documento descreve a arquitetura do projeto de software desenvolvido em Python, cujo objetivo é analisar os dados de dispensa de licitação do Distrito Federal, identificar as empresas mais beneficiadas e os órgãos públicos mais investidores. A coleta e a análise dos dados são realizadas através de diversas bibliotecas e ferramentas, com atualizações automatizadas semanalmente.

## 2. Objetivos
- Analisar dados de dispensa de licitação no Distrito Federal.
- Identificar as empresas mais beneficiadas e os órgãos públicos mais investidores.
- Fornecer visualizações claras e intuitivas dos dados coletados.

## 3. Arquitetura Geral

### 3.1. Fluxo de Trabalho
- **1) Extração e Coleta dos Dados**
     - **Coleta dos Contratos:** 
        * Feita através de requisições ao Portal Nacional de Contratações Públicas (PNCP) utilizando a biblioteca requests. 
        * Os dados são salvos em um arquivo JSON (contratos_OFICIAL.json).
        * Erros de requisição são registrados em arquivos de log para tentativas subsequentes.
     - **Coleta das Empresas:**
        * Com base nos dados dos contratos, são realizadas requisições a uma API específica de empresas para coletar informações adicionais. 
        * Os dados são salvos em um arquivo JSON (infos_cnpjs_OFICIAL.json).

- **2) Salvamento dos Dados**
     * Dados dos contratos salvos em contratos_OFICIAL.json.
     * Dados das empresas salvos em infos_cnpjs_OFICIAL.json.

- **3) Manipulação dos Dados**
     * Geração de um arquivo CSV (x_empresas_contratadas.csv) a partir dos dados dos contratos para facilitar a leitura dos dados das empresas contratadas.
     * Criação de um arquivo CSV (contratos_ordenados_completos.csv) que combina os dados dos contratos e das empresas, utilizando a biblioteca pandas.

- **4) Leitura dos Dados**
     * Leitura dos arquivos CSV gerados para análise e visualização dos dados.

- **5) Análise e Visualização dos Dados**
     * Utilização do streamlit para criar dashboards e gráficos.
     * Outras bibliotecas utilizadas incluem altair e plotly_express para visualizações adicionais.

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

## 7. Automação e Atualização de Dados

- **GitHub Actions:** Arquivos `.yml` configurados para executar scripts de coleta e atualização de dados semanalmente, garantindo que as informações estejam sempre atualizadas.

Este documento detalha a arquitetura do projeto, incluindo o fluxo de trabalho, a estrutura de diretórios e scripts, além das bibliotecas e ferramentas utilizadas para alcançar os objetivos estabelecidos.