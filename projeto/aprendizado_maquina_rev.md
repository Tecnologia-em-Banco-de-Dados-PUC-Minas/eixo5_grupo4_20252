# Aprendizado de Máquina  

O objetivo é desenvolver e integrar modelos de aprendizado de máquina (Machine Learning) capazes de analisar dados financeiros e gerar respostas automatizadas a partir de perguntas feitas pelo usuário no painel do PUC Investimentos, direcionando a usabilidade para insights com base nos dados coletados.

O propósito final é criar um chatbot inteligente que:
- Utilize os dados do painel (câmbio, ações, cripto, indicadores);
- Responda perguntas de forma contextualizada;
- Apoie análises e previsões financeiras simples.

## Etapas do Desenvolvimento

### 1. Preparação e Consolidação dos Dados
**Descrição:** reunir todos os dados coletados pelos módulos ETL (ações, câmbio, cripto e indicadores econômicos).  
**Atividades:**
- Limpeza e padronização dos dados;
- Unificação em um único dataset;
- Ajuste de formatos de data e valores;
- Criação de colunas auxiliares para análise (ex: variação mensal, anual, valorização, desvalorização).  
**Resultado esperado:** base consolidada e limpa, pronta para ser usada nos modelos de ML.

### 2. Criação dos Modelos de Aprendizado de Máquina
**Descrição:** desenvolver modelos que identifiquem padrões e tendências nos dados financeiros.  

**Tipos de modelos previstos:**
- **Regressão Linear:** prever valores futuros (ex: taxa Selic, preço do dólar, cotação de ações);
- **Classificação:** identificar tendências (alta, queda, estabilidade);
- **Clustering (agrupamento):** descobrir correlações entre ativos ou inindicadores.  

**Ferramentas:**
- `scikit-learn` (modelos preditivos)
- `pandas` e `numpy` (tratamento de dados)
- `matplotlib` ou `plotly` (visualizações)

**Resultado esperado:** scripts treinados que possam prever ou analisar o comportamento dos indicadores.

### 3. Integração com o Chatbot Financeiro
**Descrição:** conectar os modelos ao painel, criando uma interface de diálogo com o usuário.  

**Funcionamento:**
1. O usuário faz uma pergunta (ex: “qual a tendência do dólar para amanhã?”);  
2. O sistema interpreta a intenção da pergunta (NLP);  
3. Consulta o modelo ou a base de dados;  
4. Retorna uma resposta textual formatada.  

**Ferramentas:**
- `streamlit` (interface interativa)
- Modelos próprios de ML desenvolvidos na etapa anterior.  

**Resultado esperado:** chatbot integrado à aplicação, capaz de responder com base nos dados e previsões do sistema.

### 4. Avaliação e Melhoria Contínua
**Descrição:** testar a precisão dos modelos e a relevância das respostas do chatbot.  

**Ações previstas:**
- Validação dos modelos (métricas: R², RMSE, accuracy);
- Ajuste de hiperparâmetros;
- Ampliação do vocabulário e intenções do chatbot;
- Atualização periódica dos dados financeiros.  

**Resultado esperado:** melhoria contínua da qualidade das previsões e interações.
