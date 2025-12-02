
# Otimização

Durante o processo de treinamento dos modelos, foram feitos ajustes simples com o objetivo de melhorar o desempenho das predições. Abaixo estão descritas as principais ações utilizadas na otimização.

## Otimização dos Modelos de Machine Learning

### 1.1 Seleção dos parâmetros

Foram testados diferentes valores para alguns hiperparâmetros básicos dos algoritmos, como quantidade de árvores (no caso de modelos baseados em Random Forest) e profundidade máxima.  
Esses ajustes permitiram identificar combinações que apresentaram melhor equilíbrio entre acurácia e taxa de erro.

### 1.2 Avaliação de métricas

Para avaliar a qualidade dos modelos, foram utilizadas métricas como:

-   **Acurácia** – percentual de acertos do modelo.
    
-   **Taxa de erro** – proporção de previsões incorretas.
    
-   **Matriz de confusão** – tabela que compara previsões e valores reais, permitindo visualizar onde o modelo acerta e onde erra.
    

A partir dessas métricas foi possível verificar qual algoritmo teve o melhor desempenho e como cada conjunto de parâmetros impactou os resultados.

----------

## Oportunidades de Melhoria

Durante o desenvolvimento do painel e dos modelos de Machine Learning, foram identificadas oportunidades de melhoria que podem ampliar o uso e a qualidade da aplicação.

### 1. Aprimoramento da interação com o chatbot

O chatbot pode ser expandido para consultar diferentes fontes externas na web, permitindo respostas mais completas e atualizadas.  
No entanto, esse tipo de funcionalidade exige atenção, pois envolve riscos como obtenção de informações incorretas, dependência de sites externos e possíveis questões de segurança.

Para reduzir esses riscos, algumas medidas podem ser adotadas:

-   limitar as fontes externas que podem ser acessadas;
    
-   validar o conteúdo retornado antes de gerar uma resposta;
    
-   restringir os tipos de dados que podem ser consultados.
    

Essas práticas aumentariam a segurança e a confiabilidade da funcionalidade.

### 2. Filtros mais detalhados no painel

Outra oportunidade de melhoria é o aprimoramento dos filtros exibidos no dashboard.  
Filtros mais completos — como seleção por período, setor, moeda ou intervalos personalizados — tornariam a análise mais precisa e ajudariam o usuário a identificar padrões com mais clareza.

Essa evolução também facilitaria o uso dos modelos, permitindo cruzar dados de forma mais direta e objetiva.

----------

## Oportunidades de Mercado

O painel PUC Invest pode ser utilizado no mercado como uma ferramenta de apoio à análise financeira, oferecendo uma visão consolidada de ações, criptomoedas, câmbio e indicadores econômicos. Em contextos onde decisões dependem de informações rápidas e confiáveis, o painel funciona como um concentrador de dados, permitindo acompanhar tendências, comparar ativos e interpretar movimentos relevantes do mercado.

Os modelos preditivos integrados podem servir como suporte complementar para projeções de curto prazo. Embora não substituam análises especializadas, ajudam a identificar mudanças de comportamento e possíveis cenários futuros, oferecendo mais contexto para quem acompanha o desempenho dos ativos.

No ambiente corporativo ou educacional, o painel pode ser utilizado para:

-   apoiar decisões internas em empresas com rotinas de investimento;
    
-   auxiliar na elaboração de relatórios e estudos financeiros;
    
-   servir como recurso didático para o entendimento de indicadores e séries temporais.
    

Por integrar diferentes fontes de dados e apresentá-las de maneira organizada, o painel tem potencial para ser uma ferramenta útil tanto para estudantes quanto para profissionais que necessitam de uma visão rápida e abrangente do mercado financeiro.
