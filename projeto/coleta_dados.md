
# Plano de Governança de Dados

Este documento detalha a estratégia de governança de dados para o projeto de ETL de dados financeiros. Ele estabelece uma estrutura de gerenciamento que abrange requisitos, procedimentos, funções e responsabilidades para todo o ciclo de vida dos dados.

## 1. Visão Geral e Objetivos

O objetivo principal deste projeto é coletar, processar e armazenar dados financeiros de diversas fontes para análise e geração de insights. A governança de dados é crucial para garantir a qualidade, a consistência, a segurança e a conformidade dos dados ao longo de todo o processo.

Os principais objetivos da governança de dados neste projeto são:

*   **Qualidade dos Dados:** Garantir que os dados sejam precisos, completos e atualizados.
*   **Consistência dos Dados:** Manter a uniformidade dos dados em todos os sistemas e processos.
*   **Segurança dos Dados:** Proteger os dados contra acesso não autorizado e uso indevido.
*   **Conformidade:** Assegurar que o tratamento dos dados esteja em conformidade com as regulamentações e políticas internas.
*   **Transparência:** Fornecer clareza sobre a origem, o processamento e o uso dos dados.

## 2. Ciclo de Vida dos Dados

O ciclo de vida dos dados neste projeto é composto pelas seguintes etapas:

1.  **Coleta:** Os dados são coletados de fontes externas, como a B3, o Yahoo Finance e o Banco Central do Brasil.
2.  **Processamento (ETL):** Os dados brutos passam por um processo de Extração, Transformação e Carga (ETL), onde são limpos, transformados e enriquecidos.
3.  **Armazenamento:** Os dados processados são armazenados em arquivos CSV no diretório `results`.
4.  **Análise:** Os dados armazenados são utilizados para análises e geração de relatórios.
5.  **Descarte:** Os dados brutos e intermediários podem ser descartados após o processamento, enquanto os dados finais são mantidos para análise histórica.

## 3. Modelo de Dados Inicial

Os dados são estruturados nos seguintes arquivos CSV:

*   `IBXLDia_DD-MM-YY.csv`: Contém a lista de ações do IBrX-50 para um determinado dia.
    *   **Código:** O ticker da ação (ex: PETR4).
    *   **Ação:** O nome da empresa.
    *   **Tipo:** O tipo da ação (ex: ON, PN).
    *   **Qtde. Teórica:** A quantidade teórica da ação no índice.
    *   **Part. (%):** A participação da ação no índice.
*   `historico_acoes.csv`: Contém o histórico de cotações das ações.
    *   **Data:** A data da cotação.
    *   **Simbolo:** O ticker da ação.
    *   **Nome_Empresa:** O nome da empresa.
    *   **Preco:** O preço de fechamento da ação.
    *   **Volume:** O volume de negociações.
    *   **Variacao:** A variação percentual do preço em relação ao dia anterior.
*   `historico_cambio.csv`: Contém o histórico de cotações de moedas.
    *   **Data:** A data da cotação.
    *   **Simbolo:** O símbolo da moeda (ex: USDBRL=X).
    *   **Nome_Moeda:** O nome da moeda.
    *   **Preco:** O preço de fechamento.
    *   **Variacao:** A variação percentual do preço em relação ao dia anterior.
*   `historico_criptomoedas.csv`: Contém o histórico de cotações de criptomoedas.
    *   **Data:** A data da cotação.
    *   **Simbolo:** O símbolo da criptomoeda (ex: BTC-USD).
    *   **Nome_Cripto:** O nome da criptomoeda.
    *   **Preco:** O preço de fechamento em USD.
    *   **Volume:** O volume de negociações.
    *   **Variacao:** A variação percentual do preço em relação ao dia anterior.
*   `dados_economicos.csv`: Contém o histórico de indicadores econômicos.
    *   **Data:** A data do indicador.
    *   **SELIC:** A taxa Selic.
    *   **IPCA:** O índice de preços ao consumidor.
    *   **IGP-M:** O índice geral de preços do mercado.
    *   **INPC:** O índice nacional de preços ao consumidor.
    *   **CDI:** A taxa CDI.
    *   **PIB_MENSAL:** O PIB mensal.

## 4. Funções e Responsabilidades

*   **Engenheiro de Dados:** Responsável por desenvolver e manter o processo de ETL, garantindo a qualidade e a consistência dos dados.
*   **Analista de Dados:** Responsável por analisar os dados armazenados, gerar relatórios e extrair insights.
*   **Proprietário dos Dados (Data Steward):** Responsável por definir as regras de qualidade e de negócios para os dados, bem como garantir a conformidade com as políticas de governança.

## 5. Procedimentos

*   **Monitoramento:** O processo de ETL é monitorado através de logs armazenados no arquivo `results/etl_process.log`.
*   **Qualidade de Dados:** A qualidade dos dados é garantida através de validações e transformações realizadas durante o processo de ETL.
*   **Segurança:** O acesso aos dados é restrito aos usuários autorizados.
*   **Controle de Versão:** O código-fonte do projeto é versionado utilizando o Git, o que permite o rastreamento de alterações e a colaboração entre os membros da equipe.

## 6. Requisitos

*   **Requisitos Funcionais:**
    *   O sistema deve ser capaz de coletar dados de ações, câmbio, criptomoedas e indicadores econômicos.
    *   O sistema deve processar e armazenar os dados em formato CSV.
    *   O sistema deve registrar o processo de ETL em um arquivo de log.
*   **Requisitos Não-Funcionais:**
    *   O processo de ETL deve ser executado diariamente.
    *   O sistema deve ser robusto e tolerante a falhas.
    *   O acesso aos dados deve ser seguro e controlado.
