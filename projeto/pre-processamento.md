# Pré-Processamento de Dados

O **pré-processamento de dados** é a etapa do projeto responsável por preparar o ambiente e os dados para que o processamento principal ocorra de forma organizada e sem erros. Nessa fase, são realizadas tarefas como:

- Estruturação do projeto e organização das pastas.
- Criação do ambiente virtual (venv) para gerenciar dependências Python.
- Instalação de pacotes necessários (pandas, Selenium, requests etc.) de acordo com os requisitos do projeto (`requirements.txt`).
- Verificação e configuração dos módulos ETL para coleta e tratamento de dados.
- Garantia de que todos os scripts e pacotes estejam disponíveis para execução correta do projeto.

O objetivo é criar uma base sólida, garantindo que o código possa ser executado de forma consistente em diferentes máquinas ou ambientes, antes de avançar para a coleta e processamento de dados propriamente ditos.

## 1. Estrutura do Projeto

Estamos avaliando a possibilidade de implementar o Projeto na AWS através de Docker, para que o acesso e execução sejam simplificados a partir de qualquer máquina.  

No entanto, inicialmente estamos trabalhando com uma estrutura local. Portanto, é necessário criar a estrutura de pastas conforme descrito abaixo, garantindo que os pacotes do projeto sejam instalados corretamente e que o script principal possa ser executado com sucesso.

### Estrutura de Pastas
```
Projeto_Eixo5_Grupo4_20252/
│
├─ PUCInvestimentos/ ← Ambiente virtual (venv)
├─ etl/ ← Pacote com scripts de pré-processamento e coleta
│ ├─ init.py ← Permite que Python reconheça a pasta como pacote
│ ├─ scraping_ibrx50.py
│ ├─ tratar_ibrx50.py
│ ├─ acoes.py
│ ├─ criptomoedas.py
│ ├─ cambio.py
│ └─ indices_economicos.py
├─ main_process.py ← Script principal
└─ requirements.txt ← Lista de pacotes Python necessários
```
## 2. Preparação do Ambiente

### 2.1 Criar e Ativar o Ambiente Virtual (venv)

```
# Criar venv
python -m venv PUCInvestimentos

# Ativar venv no PowerShell
.\PUCInvestimentos\Scripts\Activate.ps1

# Ativar venv no CMD
.\PUCInvestimentos\Scripts\activate.bat
```

### 2.2 Instalar Dependências
```
pip install -r requirements.txt
```

### 2.3 Rodar a pipeline
```
python projeto/main_process.py
```

## 3. Preparação dos Módulos ETL
* Certificar-se de que a pasta `etl/` contém todos os arquivos .py necessários.
* Garantir que exista o arquivo `__init__.py` para que Python reconheça a pasta como pacote.

Importações Típicas no main_process.py
```
from etl.scraping_ibrx50 import download_ibrx50_data as baixar_dados_ibrx50
from etl.tratar_ibrx50 import processar_ibrx50 as tratar_dados_ibrx50
from etl.acoes import baixar_historico_acoes
from etl.criptomoedas import baixar_historico_cripto
from etl.cambio import baixar_historico_cambio
from etl.indices_economicos import buscar_dados_economicos
```

## 4. Limpeza e Tratamento dos Dados

Nesta terceira etapa, os dados já estão disponíveis, podendo estar em diferentes fontes e em diferentes formatos e padrões em cada variável ali presente, precisando realizar conversões e junções para cada formato obtido. Sendo assim, essa etapa pretende conhecer melhor os dados, retirar dados e valores que não deveriam estar presentes, tratar variáveis e valores que não estão nos padrões esperados. Resumidamente, deixar o conjunto de dados pronto e ‘limpo’ para os próximos passos de análises e treinamento dos algoritmos.

As ações realizadas para a limpeza e criação de relações incluem:
- **Conversão de Tipos:** Ajuste de colunas para os tipos corretos (ex: datas, números).
- **Tratamento de Nulos:** Decisão de como lidar com valores ausentes (remover, preencher com média/mediana, etc.).
- **Padronização de Formatos:** Garantir que dados como datas e moedas sigam um padrão único.
- **Junção de Fontes:** Unir os diferentes datasets (Ações, Câmbio, Criptomoedas, Índices) em um único conjunto de dados coeso para análise.
- **Remoção de Outliers:** Identificar e tratar valores discrepantes que possam distorcer a análise.

## 5. Ferramentas Selecionadas

É importante destacar as escolhas de ferramentas para a realização dos trabalhos. Após discussões da equipe, oficializamos as escolhas abaixo, justificando as características relevantes de cada uma.

Analisando as possíveis linguagens de programação, bibliotecas e ferramentas complementares para resolver o problema, bem como o aprendizado obtido ao longo do curso, foi escolhida a linguagem **Python** e seu ecossistema para o contexto de aprendizado de máquina.

- **Linguagem de Programação: Python**
  - **Justificativa:** É uma linguagem de alto nível, com sintaxe clara e uma vasta gama de bibliotecas para análise de dados, machine learning e automação. Sua grande comunidade garante suporte e desenvolvimento contínuo.

- **Bibliotecas Principais:**
  - **Pandas:** Ferramenta fundamental para manipulação e análise de dados. Sua estrutura de DataFrame é ideal para lidar com os dados tabulares de ações, câmbio e indicadores econômicos.
  - **yfinance:** Biblioteca para acesso direto aos dados históricos de ações do Yahoo Finance, simplificando a coleta de dados do mercado financeiro.
  - **python-bcb:** Facilita a consulta a dados e séries temporais do Banco Central do Brasil, utilizada para obter a taxa SELIC e outros indicadores.
  - **Requests:** Utilizadas para realizar chamadas a APIs de forma eficiente, como a da YFinance para dados de criptomoedas.
  - **Selenium:** Ferramenta de automação de navegadores, essencial para o web scraping de dados que não são disponibilizados via API, como a composição do índice IBrX-50.

# Observações e Recomendações
Para garantir que o projeto rode em qualquer máquina, pode-se criar um Dockerfile com todas as dependências, incluindo os pacotes necessários. Ao considerar execução na AWS, é necessário avaliar o custo de execução, pois a plataforma cobra por CPU, memória e armazenamento. Containers pesados (Python + Selenium + Pandas + scraping) podem consumir recursos consideráveis.

Inicialmente, o desenvolvimento local garante controle sobre instalação de pacotes e execução de scripts, antes de migrar para ambiente em nuvem.
