# Arquitetura da Pipeline

## Objetivo

O objetivo principal desta pipeline é automatizar as requisições para a API do Portal Nacional de Contratações Públicas (PNCP), a manipulação dos dados coletados, as requisições para a API de dados das empresas envolvidas, e a automação dos testes. A pipeline foi projetada para executar uma série de etapas que garantem a coleta eficiente dos dados, o tratamento de erros, e o processamento dessas informações de forma organizada e manipulável. Além disso, a pipeline incorpora práticas de CI/CD para assegurar a qualidade do código e a automação do deploy da documentação.

## Estrutura da Pipeline

### 1. Coleta de Dados do PNCP

A coleta dos dados do PNCP é realizada por meio de uma série de workflows, configurados para serem acionados mensalmente por uma escala cron. Devido à limitação de tempo de execução do GitHub Actions (máximo de 6 horas por workflow), a coleta foi dividida por anos para otimizar o processo e evitar interrupções.

**Workflows:**

- **`1contratos21_22.yml`**: Coleta dados referentes aos contratos dos anos de 2021 e 2022.
- **`2contratos22_23.yml`**: Coleta dados referentes aos contratos de 2022 a 2023.
- **`3contratos23_24_1.yml`**: Primeira parte da coleta dos dados de 2023 a 2024.
- **`4contratos23_24_2.yml`**: Segunda parte da coleta dos dados de 2023 a 2024.
- **`5contratos24_25.yml`**: Coleta dados referentes aos contratos de 2024 a 2025.
- **`6contratos25_26.yml`**: Coleta dados referentes aos contratos de 2025 a 2026.

### 2. Tratamento de Erros na Coleta

Após a conclusão dos workflows de coleta, um workflow adicional é acionado para tratar possíveis erros ocorridos durante as requisições à API do PNCP. Os erros são registrados em um arquivo de log e novas tentativas de requisição são feitas para corrigir os problemas.

**Workflow:**

- **`7contratos_erro.yml`**: Reprocessa as requisições que retornaram erro, e ao final, abre uma issue automática no GitHub para notificar os colaboradores sobre a necessidade de revisão do arquivo atualizado.

### 3. Revisão e Atualização do Arquivo Principal

Após a revisão do arquivo de erro pelos colaboradores, o próximo workflow é acionado manualmente para atualizar o arquivo principal com os dados corrigidos.

**Workflow:**

- **`8atualizar_principal.yml`**: Atualiza o arquivo principal com os dados coletados e corrigidos.

### 4. Processamento de Dados de Empresas

Com o arquivo principal atualizado, um novo workflow é acionado para filtrar os dados e gerar um arquivo mais simples e manipulável.

**Workflow:**

- **`9empresa.yml`**: Filtra os dados e gera um arquivo consolidado das empresas envolvidas nos contratos.

### 5. Requisição de Dados Complementares

Para enriquecer o conjunto de dados, um workflow adicional faz requisições a uma API aberta para obter informações detalhadas sobre as empresas envolvidas.

**Workflow:**

- **`10cnpj.yml`**: Faz requisições para obter dados adicionais das empresas utilizando o CNPJ.

### 6. Ordenação e Consolidação dos Dados

O último passo do processo dos dados é a ordenação dos dados coletados e sua consolidação em um arquivo final.

**Workflow:**

- **`11ordenacao.yml`**: Ordena e consolida todas as informações coletadas em um único arquivo.

## Workflows de Suporte

Além dos workflows principais para coleta e processamento dos dados, a pipeline inclui workflows adicionais para garantir a qualidade do código e o deploy da documentação.

### 1. Linter e Testes Automatizados

Sempre que há um pull request, dois workflows são acionados para verificar a qualidade do código e executar testes automatizados.

**Workflows:**

- **`linter.yml`**: Executa verificações estáticas de qualidade de código.
- **`pipeline.yml`**: Executa testes automatizados para garantir o funcionamento correto do código.

### 2. Deploy da Documentação

Sempre que há uma mudança nos arquivos da documentação que estão na pasta `docs`, o workflow de deploy é acionado para atualizar a documentação do projeto hospedada no GitHub Pages.

**Workflow:**

- **`ci.yml`**: Faz o deploy automático da página de documentação no GitHub Pages.

## Considerações Finais

Todos os workflows podem ser acionados manualmente, permitindo maior flexibilidade e controle pelos colaboradores do projeto. Essa arquitetura permite uma automação robusta, eficiente e monitorada, garantindo que os dados do PNCP sejam coletados, tratados e disponibilizados de forma correta e em tempo hábil.

A pipeline está estruturada para lidar com as limitações impostas pela API do PNCP e pelo GitHub Actions, garantindo a integridade e a qualidade dos dados ao longo de todo o processo.
