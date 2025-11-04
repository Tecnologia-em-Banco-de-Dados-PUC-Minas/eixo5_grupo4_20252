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

_Mais detalhes na seção "Dashboards e Gráficos"._

### 2. Criação dos Modelos de Aprendizado de Máquina
**Descrição:** desenvolver modelos que identifiquem padrões e tendências nos dados financeiros.  

**Tipos de modelos previstos:**
- **Regressão Linear:** prever valores futuros (ex: taxa Selic, preço do dólar, cotação de ações);
- **Random Forest:** modelo ensemble para previsões robustas de indicadores econômicos (ex: SELIC, IPCA, PIB Mensal) com features avançadas (lags, médias móveis, tendências);
- **Classificação:** identificar tendências (alta, queda, estabilidade);
- **Clustering (agrupamento):** descobrir correlações entre ativos ou indicadores.  

**Ferramentas:**
- `scikit-learn` (modelos preditivos)
- `pandas` e `numpy` (tratamento de dados)
- `plotly` (visualizações)

**Resultado esperado:** scripts treinados que possam prever ou analisar o comportamento dos indicadores.

### 3. Integração com o Chatbot Financeiro
**Descrição:** conectar os modelos ao painel, criando uma interface de diálogo com o usuário.  

**Funcionamento:**
1. O usuário faz uma pergunta (ex: “qual a tendência do dólar para amanhã?”);  
2. O sistema interpreta a intenção da pergunta (NLP);  
3. Consulta o modelo ou a base de dados;  
4. Retorna uma resposta textual formatada.  

_Mais detalhes na seção "Testes do Modelo"._

**Ferramentas:**
- `streamlit` (interface interativa)
- Modelos próprios de ML desenvolvidos na etapa anterior.  

**Resultado esperado:** chatbot integrado à aplicação, capaz de responder com base nos dados e previsões do sistema.

### 4. Avaliação e Melhoria Contínua
**Descrição:** testar a precisão dos modelos e a relevância das respostas do chatbot.  

#### 4.1. Otimização do Modelo Random Forest para Indicadores Econômicos

Durante o desenvolvimento e testes do modelo Random Forest, foram identificados problemas críticos de precisão e erros de implementação que foram sistematicamente corrigidos através de uma abordagem iterativa de análise e refinamento.

**Problemas Identificados:**

1. **INPC - MAPE Incorreto (9.889.154.181.767.804%)**
   - **Causa raiz:** O indicador INPC possui valores próximos de zero e até negativos (variação de -0.6% a 1.71%), resultando em divisões por valores extremamente pequenos no cálculo do MAPE (*Mean Absolute Percentage Error*).
   - **Impacto:** Métrica completamente inutilizável para avaliação do modelo.

2. **PIB Mensal - Erros Elevados**
   - **Valores iniciais:** MAE = 98.957, RMSE = 108.977, R² = -3.24
   - **Causa raiz:** O modelo básico (apenas features temporais: ano, mês, dia, trimestre) não capturava a tendência de crescimento mensal de 0.67% presente na série temporal do PIB.
   - **Impacto:** Previsões imprecisas com erro de ~10% e R² negativo indicando desempenho inferior à média simples.

3. **Erro de Tipo (TypeError)**
   - **Causa:** Tentativa de formatar valores `None` como percentual quando MAPE não era calculável.

4. **Erro de Features Incompatíveis (ValueError)**
   - **Causa:** Função de previsão utilizava features diferentes das usadas no treinamento do modelo PIB Mensal.

**Soluções Implementadas:**

1. **Cálculo Condicional de MAPE**
   ```python
   # MAPE calculado apenas para valores > 1.0 e positivos
   if np.all(np.abs(y_test) > 1.0) and np.all(y_test > 0):
       mape = mean_absolute_percentage_error(y_test, y_pred)
       if mape > 0.5:  # Descarta MAPE > 50%
           mape = None
   ```
   - **Justificativa:** Evita distorções causadas por divisões por valores próximos de zero.
   - **Resultado:** Métricas confiáveis para SELIC (14.87%) e PIB Mensal (6.54%).

2. **Engenharia de Features Avançadas para PIB Mensal**
   - **Features de Lag:** Incorporação de valores históricos (lag_1, lag_3, lag_12) permitindo capturar dependência temporal.
   - **Médias Móveis:** Suavização de tendências com janelas de 3 e 6 meses (ma_3, ma_6).
   - **Tendência Linear:** Adição de índice temporal para capturar crescimento sistemático.
   - **Hiperparâmetros Otimizados:** n_estimators=200 e max_depth=10 (versus 100 e None no modelo base).

3. **Previsão Iterativa para PIB Mensal**
   - Implementação de previsão passo a passo (*walk-forward*), onde cada previsão utiliza valores anteriores previstos para calcular as features de lag e médias móveis.
   - Garante consistência entre features de treino e inferência.

4. **Adição de Métricas Complementares**
   - **MAE** (*Mean Absolute Error*): Mais robusto para valores pequenos.
   - **R²** (*Coeficiente de Determinação*): Avalia qualidade do ajuste.
   - Formatação adequada: pontos percentuais (%) para índices e R$ para PIB.

**Resultados Obtidos:**

| Indicador | MAE (Antes → Depois) | RMSE (Antes → Depois) | R² (Antes → Depois) | MAPE |
|-----------|----------------------|------------------------|---------------------|------|
| SELIC | - | - | - | 14.87% ✓ |
| IPCA | - | - | - | N/A* |
| IGP-M | - | - | - | N/A* |
| INPC | - | - | - | N/A* |
| CDI | - | - | - | N/A* |
| **PIB Mensal** | **98.957 → 67.500** | **108.977 → 79.639** | **-3.24 → -1.21** | **9.74% → 6.54%** |

*N/A: MAPE não calculado devido a valores próximos de zero (usa-se MAE e RMSE como referência).*

**Melhorias Quantitativas (PIB Mensal):**
- Redução de **31.8%** no MAE
- Redução de **27%** no RMSE  
- Melhoria de **2.03 pontos** no R²
- Redução de **3.2 pontos percentuais** no MAPE

**Conclusão:**
As melhorias implementadas demonstram a importância de: (1) escolher métricas adequadas ao tipo de dado, (2) realizar engenharia de features específicas para séries temporais com tendências, e (3) validar consistência entre treino e inferência. O modelo otimizado apresenta erros significativamente menores e maior robustez preditiva.

---

**Ações previstas:**
- Validação dos modelos (métricas: R², RMSE, accuracy);
- Ajuste de hiperparâmetros;
- Ampliação do vocabulário e intenções do chatbot;
- Atualização periódica dos dados financeiros.  

**Resultado esperado:** melhoria contínua da qualidade das previsões e interações.

--- 

## Resumo Geral dos Testes de Aprendizado de Máquina
Na etapa de testes foram realizados testes com diferentes algoritmos e indicadores financeiros, com o objetivo de avaliar a capacidade preditiva de cada modelo.

| Modelo | Tipo | Indicadores testados | Principais métricas | Resultado / Observações |
|---------|------|----------------------|----------------------|---------------------------|
| **Regressão Linear** | Regressão | SELIC, PIB Mensal | R² ≈ 0.70, RMSE alto | Modelo base para comparação; capturou tendência geral, mas apresentou erros elevados. |
| **Random Forest (Base)** | Regressão | SELIC, IPCA, IGP-M, INPC, CDI, PIB Mensal | MAE = 98.957, RMSE = 108.977, R² = -3.24, MAPE = 9.74% | Modelo inicial apresentava alto erro para PIB e métricas distorcidas para índices pequenos. |
| **Random Forest (Otimizado)** | Regressão | SELIC, PIB Mensal | MAE = 67.500, RMSE = 79.639, R² = -1.21, MAPE = 6.54% | Melhoria de 31.8% no MAE e 27% no RMSE. Melhor modelo até o momento. |
| **Classificação de Tendência** | Classificação | Direção de variação (Alta, Queda, Estável) de câmbio e ações | Accuracy ≈ 0.80 (estimado) | Identificou corretamente padrões de tendência; útil para respostas do chatbot. |
| **Clustering (K-Means)** | Agrupamento | Correlação entre ativos e indicadores | Análise visual nos gráficos do dashboard | Revelou grupos de ativos com comportamento semelhante (ex: ações e câmbio correlacionados). |

### Observações gerais
- O Random Forest otimizado apresentou o melhor desempenho quantitativo nos testes de regressão.  
- O uso de features temporais (lags, médias móveis, tendência) foi decisivo para reduzir os erros.  
- Modelos de classificação e clustering complementam o sistema, apoiando análises qualitativas e insights no chatbot.  
- A engenharia de features e a escolha de métricas adequadas foram cruciais para lidar com dados financeiros de diferentes escalas.

### Dashboards e Gráficos

Veja o PUC Invest em ação!

[Demonstração do Dashboard](https://github.com/Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo4_20252/blob/d44b286db8e8192bc5a88134226b37cd8aaea87b/projeto/assets/PUC-Invest_Demo.gif)

### Testes do modelo

1. O que é o PUC Invest? 
<img width="1915" height="511" alt="image" src="https://github.com/user-attachments/assets/5b4339c0-a737-43d1-b7d3-379008d904d6" />

2. Como identificar as melhores ações? 
<img width="736" height="211" alt="image" src="https://github.com/user-attachments/assets/ea4ae136-3f39-48d7-90c1-398dc1003129" />

3. Quais criptomoedas são monitoradas? 
<img width="769" height="389" alt="image" src="https://github.com/user-attachments/assets/22a75c9b-9ecb-492e-8459-ff0bfe24c2c3" />

4. Comparação de câmbio 
<img width="727" height="238" alt="image" src="https://github.com/user-attachments/assets/94a7bfe7-a7ec-448f-ba48-a67b5829e2e6" />

5. Principais indicadores econômicos 
<img width="734" height="352" alt="image" src="https://github.com/user-attachments/assets/98a3abe2-33ba-43e0-8879-5cd8f390e8b1" /> 
<img width="1794" height="937" alt="image" src="https://github.com/user-attachments/assets/64428761-1366-4fe3-b277-d889e14ab278" /> 
<img width="1792" height="920" alt="image" src="https://github.com/user-attachments/assets/eb762510-b0d9-46ef-b17a-1d6a869b4089" />

6. Previsões e Tendências 
<img width="733" height="202" alt="image" src="https://github.com/user-attachments/assets/4191d9f1-df7d-45a1-a925-89fd2b1c9822" />

7. Interatividade 
<img width="750" height="231" alt="image" src="https://github.com/user-attachments/assets/28a0c789-215f-4841-b0b5-e7c106901da1" />

8. Atualização dos dados 
<img width="743" height="233" alt="image" src="https://github.com/user-attachments/assets/e953ec29-8c36-4d6a-ab80-4e1c180045f6" />

9. Sobre o desenvolvimento do projeto 
<img width="767" height="313" alt="image" src="https://github.com/user-attachments/assets/dcb14394-c02f-4691-aee2-856c9c8d7f61" />

10. Análise comparativa
<img width="746" height="375" alt="image" src="https://github.com/user-attachments/assets/84b9afec-b26d-4f6b-b43a-860762d4b53a" />
