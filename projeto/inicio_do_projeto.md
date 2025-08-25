# Definição do Problema – Projeto PUC Investimentos

## 1. Problema  

No cenário atual, investidores e pessoas interessadas em finanças enfrentam dificuldades em **acompanhar de forma integrada e intuitiva** os principais indicadores econômicos e financeiros do Brasil e do mercado internacional.  

As informações estão frequentemente dispersas em diferentes fontes (sites da B3, Banco Central, IBGE, exchanges de criptomoedas, etc.), dificultando a análise consolidada e o processo de tomada de decisão.  

Além disso, a ausência de ferramentas acessíveis e interativas torna o processo ainda mais complexo, principalmente para iniciantes no mercado financeiro.  

---

## 2. Contexto  

Para atender a essa necessidade, o projeto **PUC Investimentos** foi desenvolvido como um dashboard interativo que consolida informações financeiras relevantes em um único ambiente.  

### Conjuntos de dados utilizados e justificativa:  
- **Ações brasileiras (IBRX50)** – Fonte: B3.  
  *Justificativa*: reúne as ações mais líquidas e representativas do mercado brasileiro.  

- **Criptomoedas** – Fonte: exchanges internacionais.  
  *Justificativa*: relevância crescente no mercado global e interesse de investidores em acompanhar sua volatilidade.  

- **Câmbio** – Fonte: Banco Central do Brasil.  
  *Justificativa*: importante para investidores, empresas de comércio exterior e pessoas físicas que dependem de moedas estrangeiras.  

- **Indicadores econômicos (SELIC, IPCA, CDI, PIB, etc.)** – Fontes: IBGE, Banco Central e órgãos oficiais.  
  *Justificativa*: fundamentais para a compreensão do cenário macroeconômico.  

A viabilidade está garantida pela disponibilidade pública e atualizada desses dados, além de integrações possíveis por APIs e datasets de acesso aberto.  

---

## 3. Objetivos  

### Objetivo Geral  
Disponibilizar uma ferramenta digital que consolide indicadores financeiros e econômicos em uma interface intuitiva e interativa, promovendo **acesso democratizado às informações financeiras**.  

### Objetivos Específicos  
- Centralizar, em um único dashboard, dados de ações, criptomoedas, câmbio e indicadores econômicos.  
- Permitir análises interativas (gráficos dinâmicos, rankings, comparativos).  
- Facilitar a compreensão de tendências de mercado para diferentes perfis de usuários.  
- Garantir atualização periódica e confiabilidade das informações apresentadas.  
- Apoiar a educação financeira, oferecendo um recurso acessível para iniciantes e investidores experientes.  

### Resultados Esperados  
- Redução da dispersão de fontes de informação.  
- Maior eficiência e clareza na análise de ativos e indicadores.  
- Ferramenta que auxilie na tomada de decisão financeira de forma segura e transparente.  

---

## 4. Perspectiva do Usuário e Ética  

O usuário, seja ele investidor iniciante ou experiente, precisa de **acesso rápido, confiável e simplificado** aos dados financeiros.  

O projeto adota princípios éticos ao:  
- Utilizar apenas dados de fontes oficiais e públicas.  
- Esclarecer que as informações possuem caráter **informativo e educacional**, não configurando recomendação de investimento.  
- Respeitar a privacidade do usuário, sem coleta indevida de dados pessoais.  
- Contribuir com a sociedade ao incentivar **educação financeira acessível, sustentável e segura**.  

---

## 5. Processo de Controle dos Dados  

Para garantir rastreabilidade e confiabilidade, o processo de controle do **PUC** seguirá estas diretrizes:  

1. **Origem dos dados**: registro da fonte (B3, Banco Central, IBGE, exchanges).  
2. **Coleta**: APIs ou datasets atualizados periodicamente.  
3. **Transformação**: padronização de formatos (ex.: datas, moedas, índices) e tratamento de dados ausentes.  
4. **Armazenamento temporário**: logs com versionamento para identificar alterações.  
5. **Visualização no dashboard**: gráficos e tabelas interativas atualizadas.  
6. **Rastreamento de exceções**:  
   - Erros de conexão ou ausência de atualização serão registrados.  
   - Logs permitirão auditoria das modificações desde a coleta até a visualização final.  
   - Alertas podem ser configurados para notificar inconsistências.  

Esse processo garante **transparência, segurança e integridade** dos dados apresentados no dashboard.  

