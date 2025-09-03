
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
Projeto_Eixo5/
│
├─ projeto_Eixo5/ ← Ambiente virtual (venv)
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
python -m venv projeto_Eixo5

# Ativar venv no PowerShell
.\projeto_Eixo5\Scripts\Activate.ps1

# Ativar venv no CMD
.\projeto_Eixo5\Scripts\activate.bat
```

### 2.2 Instalar Dependências
```
pip install -r requirements.txt
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

# Observações e Recomendações
Para garantir que o projeto rode em qualquer máquina, pode-se criar um Dockerfile com todas as dependências, incluindo os pacotes necessários. Ao considerar execução na AWS, é necessário avaliar o custo de execução, pois a plataforma cobra por CPU, memória e armazenamento. Containers pesados (Python + Selenium + Pandas + scraping) podem consumir recursos consideráveis.

Inicialmente, o desenvolvimento local garante controle sobre instalação de pacotes e execução de scripts, antes de migrar para ambiente em nuvem.
