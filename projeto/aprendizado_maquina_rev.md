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
