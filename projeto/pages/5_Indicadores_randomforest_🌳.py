import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from projeto.style.style_config import apply_custom_style, COLORS, add_footer

# Aplicar estilo customizado
apply_custom_style()


# Função para calcular a variação percentual
def calcular_variacao(serie, tipo="mensal"):
    """Calcula a variação percentual de uma série temporal.

    Args:
        serie (pd.Series): Série de dados com índice de data.
        tipo (str, optional): Tipo de variação a ser calculada ('diario', 'mensal', 'anual').
                              Defaults to "mensal".

    Returns:
        tuple: Uma tupla contendo o valor atual e a variação percentual.
               Retorna (valor, None) se a variação não puder ser calculada.
    """
    valores = serie.dropna()
    if len(valores) < 2:
        return None, None

    valor_atual = valores.iloc[-1]

    if tipo == "diario":
        valor_anterior = valores.iloc[-2]
    elif tipo == "mensal":
        if not isinstance(valores.index, pd.DatetimeIndex):
            valores.index = pd.to_datetime(valores.index)
        valores_mensais = valores.groupby(pd.Grouper(freq="ME")).last().dropna()
        if len(valores_mensais) >= 2:
            valor_atual = valores_mensais.iloc[-1]
            valor_anterior = valores_mensais.iloc[-2]
        else:
            return valor_atual, None
    elif tipo == "anual":
        if not isinstance(valores.index, pd.DatetimeIndex):
            valores.index = pd.to_datetime(valores.index)
        valores_anuais = valores.groupby(pd.Grouper(freq="Y")).last().dropna()
        if len(valores_anuais) >= 2:
            valor_atual = valores_anuais.iloc[-1]
            valor_anterior = valores_anuais.iloc[-2]
        else:
            return valor_atual, None

    if valor_anterior != 0:
        variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
        return valor_atual, variacao
    return valor_atual, None


def formatar_valor(valor, tipo):
    """Formata um valor numérico como string de acordo com seu tipo.

    Args:
        valor (float or int): O valor a ser formatado.
        tipo (str): O tipo de formatação ('moeda', 'percentual', ou outro).

    Returns:
        str: O valor formatado como string, ou "N/A" se o valor for None.
    """
    if valor is None:
        return "N/A"
    if tipo == "moeda":
        return f"R$ {valor:,.2f}"
    elif tipo == "percentual":
        return f"{valor:.2f}%"
    else:
        return f"{valor:.2f}"


@st.cache_data
def carregar_dados():
    """Carrega e pré-processa os dados econômicos do arquivo CSV.

    Returns:
        dict: Um dicionário onde as chaves são os nomes dos indicadores
              e os valores são os DataFrames correspondentes.
    """
    dados_path = os.path.join(project_root, "results", "dados_economicos.csv")

    df = pd.read_csv(dados_path)
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Criar DataFrames individuais para cada indicador
    selic_df = df[["Date", "SELIC"]].copy()
    selic_df = selic_df.dropna().reset_index(drop=True)
    selic_df["SELIC"] = pd.to_numeric(selic_df["SELIC"], errors="coerce")

    ipca_df = df[["Date", "IPCA"]].copy()
    ipca_df = ipca_df.dropna().reset_index(drop=True)
    ipca_df["IPCA"] = pd.to_numeric(ipca_df["IPCA"], errors="coerce")

    igpm_df = df[["Date", "IGP-M"]].copy()
    igpm_df = igpm_df.dropna().reset_index(drop=True)
    igpm_df["IGP-M"] = pd.to_numeric(igpm_df["IGP-M"], errors="coerce")

    inpc_df = df[["Date", "INPC"]].copy()
    inpc_df = inpc_df.dropna().reset_index(drop=True)
    inpc_df["INPC"] = pd.to_numeric(inpc_df["INPC"], errors="coerce")

    cdi_df = df[["Date", "CDI"]].copy()
    cdi_df = cdi_df.dropna().reset_index(drop=True)
    cdi_df["CDI"] = pd.to_numeric(cdi_df["CDI"], errors="coerce")

    pib_df = df[["Date", "PIB_MENSAL"]].copy()
    pib_df = pib_df.dropna().reset_index(drop=True)
    pib_df["PIB_MENSAL"] = pd.to_numeric(pib_df["PIB_MENSAL"], errors="coerce")

    # Criar dicionário com todos os dataframes
    dataframes = {
        "SELIC": selic_df,
        "IPCA": ipca_df,
        "IGP-M": igpm_df,
        "INPC": inpc_df,
        "CDI": cdi_df,
        "PIB_MENSAL": pib_df,
    }

    return dataframes


def criar_features_temporais(df):
    """Cria features baseadas em data a partir de uma coluna 'Date'.

    Args:
        df (pd.DataFrame): DataFrame com uma coluna 'Date' do tipo datetime.

    Returns:
        pd.DataFrame: O DataFrame original com novas colunas de features
                      temporais (ano, mes, dia, etc.).
    """
    df = df.copy()
    df["ano"] = df["Date"].dt.year
    df["mes"] = df["Date"].dt.month
    df["dia"] = df["Date"].dt.day
    df["dia_semana"] = df["Date"].dt.dayofweek
    df["trimestre"] = df["Date"].dt.quarter
    return df



def criar_features_melhoradas(df, indicador):
    """Cria features avancadas incluindo lags e medias moveis para series com tendencia.
    
    Args:
        df (pd.DataFrame): DataFrame com coluna Date e o indicador.
        indicador (str): Nome da coluna do indicador.
    
    Returns:
        pd.DataFrame: DataFrame com features adicionais.
    """
    df = df.copy()
    df["ano"] = df["Date"].dt.year
    df["mes"] = df["Date"].dt.month
    df["dia"] = df["Date"].dt.day
    df["dia_semana"] = df["Date"].dt.dayofweek
    df["trimestre"] = df["Date"].dt.quarter
    
    # Features de lag (valores anteriores)
    df['lag_1'] = df[indicador].shift(1)
    df['lag_3'] = df[indicador].shift(3)
    df['lag_12'] = df[indicador].shift(12)
    
    # Medias moveis
    df['ma_3'] = df[indicador].rolling(window=3).mean()
    df['ma_6'] = df[indicador].rolling(window=6).mean()
    
    # Tendencia linear (indice temporal)
    df['tendencia'] = range(len(df))
    
    return df.dropna()

def treinar_random_forest(df, indicador, periodos_previsao=6):
    """Treina um modelo de Random Forest para prever um indicador.

    Args:
        df (pd.DataFrame): DataFrame com os dados históricos e features temporais.
        indicador (str): Nome da coluna do indicador a ser previsto.
        periodos_previsao (int, optional): Número de períodos para previsão. Defaults to 6.

    Returns:
        tuple: Uma tupla contendo o modelo treinado, o scaler, métricas (MAE, RMSE, R2, MAPE).
               Retorna (None, None, None, None, None, None) se não houver dados suficientes.
    """
    if len(df) < 24:
        return None, None, None, None, None, None

    # Usar features melhoradas para PIB_MENSAL (que tem tendencia forte)
    if indicador == "PIB_MENSAL":
        df_features = criar_features_melhoradas(df, indicador)
        X = df_features[["ano", "mes", "trimestre", "lag_1", "lag_3", "lag_12", "ma_3", "ma_6", "tendencia"]]
        # Ajustar hiperparametros para PIB
        n_estimators = 200
        max_depth = 10
    else:
        df_features = criar_features_temporais(df)
        X = df_features[["ano", "mes", "dia", "trimestre"]]
        n_estimators = 100
        max_depth = None
    
    y = df_features[indicador]

    if np.isinf(y).any() or y.isna().any():
        return None, None, None, None, None, None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)
    
    # Calcular MAE (Erro Absoluto Médio) - mais confiável para valores pequenos
    mae = mean_absolute_error(y_test, y_pred)
    
    # Calcular RMSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Calcular R² (coeficiente de determinação)
    r2 = r2_score(y_test, y_pred)
    
    # Calcular MAPE apenas se não houver valores muito próximos de zero ou negativos
    # Para evitar divisão por valores muito pequenos que causam erros enormes
    # Também verifica se a média dos valores é razoável para o cálculo percentual
    if np.all(np.abs(y_test) > 1.0) and np.all(y_test > 0):  # Valores > 1 e todos positivos
        try:
            mape = mean_absolute_percentage_error(y_test, y_pred)  # Retorna valor 0-1
            # Se MAPE for muito alto (> 50%), também não exibir
            if mape > 0.5:
                mape = None
        except:
            mape = None
    else:
        mape = None

    return modelo, scaler, mae, rmse, r2, mape


def fazer_previsoes_random_forest(modelo, scaler, df, indicador, periodos=6):
    """Gera previsões futuras usando um modelo de random forest treinado.

    Args:
        modelo (RandomForestRegressor): O modelo treinado.
        scaler (StandardScaler): O normalizador ajustado aos dados de treino.
        df (pd.DataFrame): O DataFrame histórico para obter a última data.
        indicador (str): O nome da coluna do indicador.
        periodos (int, optional): Número de meses a prever. Defaults to 6.

    Returns:
        tuple: Uma tupla com (previsões, intervalo_inferior, intervalo_superior).
    """
    ultima_data = df["Date"].iloc[-1]
    datas_futuras = pd.date_range(start=ultima_data, periods=periodos + 1, freq="ME")[1:]

    # Para PIB_MENSAL, usar previsão iterativa com features de lag
    if indicador == "PIB_MENSAL":
        previsoes = []
        df_temp = df.copy()
        
        for data_futura in datas_futuras:
            # Criar features para a próxima previsão
            df_temp_features = criar_features_melhoradas(df_temp, indicador)
            
            if len(df_temp_features) > 0:
                ultima_linha = df_temp_features.iloc[-1:]
                X_futuro = ultima_linha[["ano", "mes", "trimestre", "lag_1", "lag_3", "lag_12", "ma_3", "ma_6", "tendencia"]].copy()
                
                # Atualizar features temporais para data futura
                X_futuro["ano"] = data_futura.year
                X_futuro["mes"] = data_futura.month
                X_futuro["trimestre"] = (data_futura.month - 1) // 3 + 1
                X_futuro["tendencia"] = len(df_temp)
                
                X_futuro_scaled = scaler.transform(X_futuro)
                previsao = modelo.predict(X_futuro_scaled)[0]
                previsoes.append(previsao)
                
                # Adicionar previsão ao df_temp para próxima iteração
                nova_linha = pd.DataFrame({
                    "Date": [data_futura],
                    indicador: [previsao]
                })
                df_temp = pd.concat([df_temp, nova_linha], ignore_index=True)
        
        previsoes = np.array(previsoes)
    else:
        # Para outros indicadores, usar método original
        df_futuro = pd.DataFrame({"Date": datas_futuras})
        df_futuro = criar_features_temporais(df_futuro)
        X_futuro = df_futuro[["ano", "mes", "dia", "trimestre"]]
        X_futuro_scaled = scaler.transform(X_futuro)
        previsoes = modelo.predict(X_futuro_scaled)

    std_historico = df[indicador].std()
    intervalo_inferior = previsoes - 1.96 * std_historico
    intervalo_superior = previsoes + 1.96 * std_historico

    return (
        pd.Series(previsoes, index=datas_futuras),
        pd.Series(intervalo_inferior, index=datas_futuras),
        pd.Series(intervalo_superior, index=datas_futuras),
    )


# Carregando os dados
df_dict = carregar_dados()

# Título da página
st.title("Indicadores Econômicos do Brasil - Random Forest 🌳")
st.markdown("---")

st.markdown("""
    ### Descrição dos Indicadores Econômicos:
    
    - **SELIC**: Taxa básica de juros da economia brasileira, definida pelo Banco Central. É um dos principais instrumentos de política monetária para controle da inflação.
    
    - **IPCA**: Índice de Preços ao Consumidor Amplo, considerado o índice oficial de inflação do Brasil. Mede a variação de preços de produtos e serviços consumidos pelas famílias.
    
    - **IGP-M**: Índice Geral de Preços do Mercado, calculado pela FGV. Muito utilizado para reajustes de contratos de aluguel e tarifas públicas.
    
    - **INPC**: Índice Nacional de Preços ao Consumidor, que mede a variação do custo de vida para famílias com renda de 1 a 5 salários mínimos.
    
    - **CDI**: Certificado de Depósito Interbancário, taxa que serve de referência para investimentos de renda fixa e empréstimos entre bancos.
    
    - **PIB Mensal**: Produto Interno Bruto, representa a soma de todos os bens e serviços produzidos no país, sendo um indicador da atividade econômica.
    """)

st.markdown("---")

# Adicionando CSS para melhorar o layout dos cards
st.markdown(
    """
<style>
    div[data-testid="column"] {
        padding: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Criando cards para cada indicador
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# Dicionário com informações dos indicadores
indicadores = {
    "SELIC": {
        "nome": "Taxa SELIC",
        "descricao": "Taxa básica de juros da economia",
        "frequencia": "Atualização diária",
        "tipo_valor": "percentual",
        "tipo_variacao": "diario",
        "col": col1,
    },
    "IPCA": {
        "nome": "IPCA",
        "descricao": "Índice de Preços ao Consumidor Amplo",
        "frequencia": "Atualização mensal",
        "tipo_valor": "percentual",
        "tipo_variacao": "mensal",
        "col": col2,
    },
    "IGP-M": {
        "nome": "IGP-M",
        "descricao": "Índice Geral de Preços do Mercado",
        "frequencia": "Atualização mensal",
        "tipo_valor": "percentual",
        "tipo_variacao": "mensal",
        "col": col3,
    },
    "INPC": {
        "nome": "INPC",
        "descricao": "Índice Nacional de Preços ao Consumidor",
        "frequencia": "Atualização mensal",
        "tipo_valor": "percentual",
        "tipo_variacao": "mensal",
        "col": col4,
    },
    "CDI": {
        "nome": "Taxa CDI",
        "descricao": "Certificado de Depósito Interbancário",
        "frequencia": "Atualização diária",
        "tipo_valor": "percentual",
        "tipo_variacao": "diario",
        "col": col5,
    },
    "PIB_MENSAL": {
        "nome": "PIB Mensal",
        "descricao": "Produto Interno Bruto (em milhões R$)",
        "frequencia": "Atualização mensal",
        "tipo_valor": "moeda",
        "tipo_variacao": "mensal",
        "col": col6,
    },
}

# Criando cards e gráficos para cada indicador
for codigo, info in indicadores.items():
    with info["col"]:
        df_indicador = df_dict[codigo]
        serie = df_indicador.set_index("Date")[codigo]
        valor_atual, variacao = calcular_variacao(serie, info["tipo_variacao"])

        # Definindo cores com base na variação
        if variacao is not None:
            if variacao > 0:
                cor_valor = "#00ff00"  # Verde
            elif variacao < 0:
                cor_valor = "#ff0000"  # Vermelho
            else:
                cor_valor = "white"
        else:
            cor_valor = "white"

        # Formatando o valor de acordo com o tipo
        valor_formatado = formatar_valor(valor_atual, info["tipo_valor"])

        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; background-color: #1a1a1a; color: white; margin: 10px; height: 100%;">
                <h3 style="margin-top: 0;">{info["nome"]}</h3>
                <p style="margin: 10px 0;">{info["descricao"]}</p>
                <p style="color: #888888; font-size: 0.8em; margin: 10px 0;">{info["frequencia"]}</p>
                <h2 style="color: {cor_valor}; margin: 15px 0;">{valor_formatado}</h2>
                <p style="color: {cor_valor}; margin-bottom: 0;">Variação: {"%.2f" % variacao if variacao is not None else "N/A"}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Adicionando espaço entre os cards
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Gráficos
st.markdown("## Evolução dos Indicadores")

tabs = st.tabs([f"**{indicador}**" for indicador in indicadores.keys()])

for (codigo, info), tab in zip(indicadores.items(), tabs):
    with tab:
        df_indicador = df_dict[codigo]

        fig = go.Figure()

        # Linha principal
        fig.add_trace(
            go.Scatter(
                x=df_indicador["Date"],
                y=df_indicador[codigo],
                mode="lines",
                name=info["nome"],
                line=dict(color=COLORS["primary"]),
            )
        )

        # Média móvel 30 dias
        if len(df_indicador) > 30:
            fig.add_trace(
                go.Scatter(
                    x=df_indicador["Date"],
                    y=df_indicador[codigo].rolling(30).mean(),
                    mode="lines",
                    name="Média Móvel (30 dias)",
                    line=dict(color=COLORS["secondary"], dash="dot"),
                )
            )

        fig.update_layout(
            title=f"Evolução do {info['nome']}",
            xaxis_title="Data",
            yaxis_title="Valor",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

# Tabs para diferentes visualizações
tab1, tab2 = st.tabs(["Comparativo", "Previsões"])

with tab1:
    # Gráfico comparativo (normalizado)
    fig_comp = go.Figure()

    # Lista de cores para o gráfico comparativo
    cores = ["primary", "secondary", "accent", "dark_blue", "text", "background"]

    for i, (codigo, info) in enumerate(indicadores.items()):
        df_indicador = df_dict[codigo]

        # Preparando os dados de acordo com a frequência
        if info["tipo_variacao"] == "mensal":
            # Convertendo para datetime
            df_indicador["Date"] = pd.to_datetime(df_indicador["Date"])
            # Agrupando por mês e pegando o último valor de cada mês
            dados_agrupados = (
                df_indicador.set_index("Date")
                .groupby(pd.Grouper(freq="ME"))
                .last()
                .reset_index()
            )
            dados_agrupados = dados_agrupados.dropna()
        elif info["tipo_variacao"] == "anual":
            # Convertendo para datetime
            df_indicador["Date"] = pd.to_datetime(df_indicador["Date"])
            # Agrupando por ano e pegando o último valor de cada ano
            dados_agrupados = (
                df_indicador.set_index("Date")
                .groupby(pd.Grouper(freq="Y"))
                .last()
                .reset_index()
            )
            dados_agrupados = dados_agrupados.dropna()
        else:
            dados_agrupados = df_indicador

        # Normalizando os dados para comparação
        if len(dados_agrupados) > 0:
            dados_norm = dados_agrupados[codigo] / dados_agrupados[codigo].iloc[0] * 100

            fig_comp.add_trace(
                go.Scatter(
                    x=dados_agrupados["Date"],
                    y=dados_norm,
                    name=info["nome"],
                    line=dict(width=2, color=COLORS[cores[i % len(cores)]]),
                )
            )

    fig_comp.update_layout(
        title="Comparativo da Evolução dos Indicadores (Base 100)",
        xaxis_title="Data",
        yaxis_title="Valor (Base 100)",
        height=600,
        showlegend=True,
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig_comp, use_container_width=True)

with tab2:
    st.markdown("## Previsões dos Indicadores")

    # Seletor de horizonte de previsão
    horizonte = st.slider(
        "Horizonte de Previsão (meses)",
        min_value=1,
        max_value=12,
        value=6,
        help="Selecione quantos meses à frente você deseja prever",
    )

    for codigo, info in indicadores.items():
        st.markdown(f"### {info['nome']}")

        # Preparando os dados
        df_indicador = df_dict[codigo].copy()

        # Verificando se temos dados suficientes
        if len(df_indicador) < 24:
            st.warning(
                f"Dados insuficientes para gerar previsões confiáveis para {info['nome']}"
            )
            continue

        # Tratamento para frequência mensal
        if info["tipo_variacao"] == "mensal":
            # Convertendo para datetime
            df_indicador["Date"] = pd.to_datetime(df_indicador["Date"])
            # Agrupando por mês e pegando o último valor de cada mês
            df_indicador = (
                df_indicador.set_index("Date")
                .groupby(pd.Grouper(freq="ME"))
                .last()
                .reset_index()
            )
            df_indicador = df_indicador.dropna()

        # Treinando modelo de random forest
        modelo, scaler, mae, rmse, r2, mape = treinar_random_forest(
            df_indicador, codigo, periodos_previsao=horizonte
        )

        if modelo and scaler:
            # Fazendo previsões
            previsoes, intervalo_inf, intervalo_sup = fazer_previsoes_random_forest(
                modelo, scaler, df_indicador, codigo, periodos=horizonte
            )

            # Plotando resultados
            fig = go.Figure()

            # Dados históricos
            fig.add_trace(
                go.Scatter(
                    x=df_indicador["Date"],
                    y=df_indicador[codigo],
                    name="Dados Históricos",
                    line=dict(color=COLORS["primary"]),
                )
            )

            # Último valor histórico
            ultimo_valor = df_indicador[codigo].iloc[-1]
            fig.add_trace(
                go.Scatter(
                    x=[df_indicador["Date"].iloc[-1]],
                    y=[ultimo_valor],
                    mode="markers",
                    marker=dict(color=COLORS["primary"], size=10),
                    name="Último Valor Real",
                    showlegend=False,
                )
            )

            # Previsões
            fig.add_trace(
                go.Scatter(
                    x=previsoes.index,
                    y=previsoes,
                    name="Previsão",
                    line=dict(color=COLORS["secondary"], dash="dash"),
                )
            )

            # Primeiro valor previsto
            fig.add_trace(
                go.Scatter(
                    x=[previsoes.index[0]],
                    y=[previsoes.iloc[0]],
                    mode="markers",
                    marker=dict(color=COLORS["secondary"], size=10),
                    name="Início da Previsão",
                    showlegend=False,
                )
            )

            # Intervalo de confiança
            fig.add_trace(
                go.Scatter(
                    x=pd.concat(
                        [pd.Series(previsoes.index), pd.Series(previsoes.index[::-1])]
                    ),
                    y=pd.concat([intervalo_sup, intervalo_inf[::-1]]),
                    fill="toself",
                    fillcolor="rgba(0,150,200,0.2)",
                    line=dict(color="rgba(255,255,255,0)"),
                    name="Intervalo de Confiança",
                )
            )

            fig.update_layout(
                title=f"Previsão {info['nome']} - Próximos {horizonte} meses",
                xaxis_title="Data",
                yaxis_title=f"Valor {' (%)' if info['tipo_valor'] == 'percentual' else ' (R$ milhões)' if info['tipo_valor'] == 'moeda' else ''}",
                height=400,
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(fig, use_container_width=True)


            # Exibindo as métricas de avaliação do modelo
            st.markdown("##### Métricas de Avaliação do Modelo de Previsão")
            col_metrica1, col_metrica2, col_metrica3 = st.columns(3)
            
            # Formatar valores de acordo com o tipo de indicador
            if codigo == "PIB_MENSAL":
                mae_fmt = f"R$ {mae:,.0f}"
                rmse_fmt = f"R$ {rmse:,.0f}"
                mae_help = "Erro médio em milhões de reais. Quanto menor, melhor."
                rmse_help = "Magnitude média dos erros em milhões de reais. Quanto menor, melhor."
            else:
                # Indicadores percentuais (SELIC, IPCA, IGP-M, INPC, CDI)
                mae_fmt = f"{mae:.2f}%"
                rmse_fmt = f"{rmse:.2f}%"
                mae_help = "Erro médio percentual. Quanto menor, melhor."
                rmse_help = "Magnitude média dos erros percentuais. Quanto menor, melhor."
            
            with col_metrica1:
                st.metric(label="Erro Absoluto Médio (MAE)",
                          value=mae_fmt,
                          help=mae_help)
            with col_metrica2:
                st.metric(label="Raiz do Erro Quadrático Médio (RMSE)",
                          value=rmse_fmt,
                          help=rmse_help)
            with col_metrica3:
                st.metric(label="Coeficiente de Determinação (R²)",
                          value=f"{r2:.4f}",
                          help="Indica a qualidade do ajuste do modelo (-∞ a 1). Quanto mais próximo de 1, melhor.")
            
            # Exibir MAPE apenas se disponível
            if mape is not None:
                st.metric(label="Erro Percentual Médio Absoluto (MAPE)",
                          value=f"{mape:.2%}",
                          help="Indica o erro médio das previsões em termos percentuais. Quanto menor, melhor o modelo.")
            else:
                st.info("⚠️ MAPE não calculado: valores muito próximos de zero podem gerar resultados imprecisos. Use MAE e RMSE como referência.")

# Adicionar footer padronizado
add_footer()
