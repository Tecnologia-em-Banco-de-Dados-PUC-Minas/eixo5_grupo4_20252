import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import requests
from etl.cambio import get_usdbrl_rate

def _get_results_dir():
    """
    Retorna o diretório de resultados do projeto.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))

def baixar_historico_acoes():
    """
    Baixa o histórico dos últimos 10 anos de todas as ações do IBOVESPA
    e salva em um arquivo CSV.
    """
    try:
        results_dir = _get_results_dir()
        
        data_atual = datetime.now().strftime('%d-%m-%y')
        nome_arquivo = os.path.join(results_dir, f'IBXLDia_{data_atual}.csv')
        
        df_acoes = pd.read_csv(nome_arquivo, skiprows=1)
        df_acoes.columns = ['Código']
        tickers = df_acoes['Código'].tolist()
        
        data_inicial = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
        
        dados_historicos = []
        
        print("Iniciando download do histórico das ações...")
        
        for ticker in tickers:
            ticker_yf = f"{ticker}.SA"
            try:
                acao = yf.Ticker(ticker_yf)
                hist = acao.history(start=data_inicial)
                
                if hist.empty:
                    continue
                
                hist['Ticker'] = ticker
                hist['Nome'] = ticker
                
                hist = hist.reset_index()
                hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
                
                dados_historicos.append(hist)
                
                print(f"Dados baixados para {ticker}")
                
            except Exception as e:
                print(f"Erro ao baixar dados de {ticker}: {str(e)}")
                continue
        
        if dados_historicos:
            df_historico = pd.concat(dados_historicos, ignore_index=True)
            
            df_historico = df_historico[['Date', 'Ticker', 'Nome', 'Close', 'Volume']]
            df_historico.columns = ['Data', 'Simbolo', 'Nome_Empresa', 'Preco', 'Volume']
            
            df_historico['Variacao'] = df_historico.groupby('Simbolo')['Preco'].pct_change() * 100
            
            nome_arquivo_historico = os.path.join(results_dir, 'historico_acoes.csv')
            df_historico.to_csv(nome_arquivo_historico, index=False)
            print(f"\nHistórico salvo com sucesso em '{nome_arquivo_historico}'")
            
            return df_historico
        else:
            print("\nNenhum dado histórico foi baixado")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Erro ao processar dados históricos: {str(e)}")
        return pd.DataFrame()

def obter_melhores_e_piores_acoes(periodo='1d'):
    """
    Obtém as 5 melhores e 5 piores ações do período especificado usando o arquivo histórico.
    
    Args:
        periodo (str): Período de análise ('1d' para 30 dias, '1mo' para mensal, '1y' para anual)
    """
    try:
        results_dir = _get_results_dir()
        nome_arquivo = os.path.join(results_dir, 'historico_acoes.csv')
        df_historico = pd.read_csv(nome_arquivo)
        df_historico['Data'] = pd.to_datetime(df_historico['Data'])
        
        data_mais_recente = df_historico['Data'].max()
        
        if periodo == '1d':
            data_inicio = data_mais_recente - pd.Timedelta(days=30)
            df_periodo = df_historico[df_historico['Data'] >= data_inicio].copy()
            df_periodo = df_periodo.groupby('Simbolo').agg({
                'Preco': ['first', 'last'],
                'Nome_Empresa': 'first'
            }).reset_index()
            df_periodo.columns = ['Simbolo', 'Preco_Inicial', 'Preco_Final', 'Nome_Empresa']
            df_periodo['Variacao'] = ((df_periodo['Preco_Final'] / df_periodo['Preco_Inicial']) - 1) * 100
            
        elif periodo == '1mo':
            df_historico['Mes_Ano'] = df_historico['Data'].dt.to_period('M')
            df_periodo = df_historico.groupby(['Simbolo', 'Mes_Ano', 'Nome_Empresa'])['Preco'].mean().reset_index()
            df_periodo = df_periodo.sort_values(['Simbolo', 'Mes_Ano'])
            df_periodo = df_periodo.groupby('Simbolo').agg({
                'Preco': ['first', 'last'],
                'Nome_Empresa': 'first'
            }).reset_index()
            df_periodo.columns = ['Simbolo', 'Preco_Inicial', 'Preco_Final', 'Nome_Empresa']
            df_periodo['Variacao'] = ((df_periodo['Preco_Final'] / df_periodo['Preco_Inicial']) - 1) * 100
            
        else:
            df_historico['Ano'] = df_historico['Data'].dt.year
            df_periodo = df_historico.groupby(['Simbolo', 'Ano', 'Nome_Empresa'])['Preco'].mean().reset_index()
            df_periodo = df_periodo.sort_values(['Simbolo', 'Ano'])
            df_periodo = df_periodo.groupby('Simbolo').agg({
                'Preco': ['first', 'last'],
                'Nome_Empresa': 'first'
            }).reset_index()
            df_periodo.columns = ['Simbolo', 'Preco_Inicial', 'Preco_Final', 'Nome_Empresa']
            df_periodo['Variacao'] = ((df_periodo['Preco_Final'] / df_periodo['Preco_Inicial']) - 1) * 100
        
        if df_periodo.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        df_periodo['Preço'] = df_periodo['Preco_Final'].round(2)
        df_periodo['Variação (%)'] = df_periodo['Variacao'].round(2)
        df_periodo['Símbolo'] = df_periodo['Simbolo']
        df_periodo['Empresa'] = df_periodo['Nome_Empresa']
        
        melhores = df_periodo.nlargest(5, 'Variacao')[['Símbolo', 'Empresa', 'Preço', 'Variação (%)']]
        piores = df_periodo.nsmallest(5, 'Variacao')[['Símbolo', 'Empresa', 'Preço', 'Variação (%)']]
        
        return melhores, piores
    
    except Exception as e:
        print(f"Erro ao processar dados: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

def get_current_prices_acoes(df):
    """
    Obtém os preços atuais das ações e calcula a variação percentual em relação ao preço de compra.
    
    Args:
        df (DataFrame): DataFrame contendo as informações das ações com as colunas:
                        id_acoes, nome, preco_inicial, etc.
    
    Returns:
        DataFrame: DataFrame atualizado com os preços atuais e variação percentual.
    """
    try:
        df_acoes = df.copy(deep=True)
        
        symbol_map = {
            "PETR4": "PETR4.SA",
            "VALE3": "VALE3.SA",
            "ITUB4": "ITUB4.SA", 
            "MGLU3": "MGLU3.SA",
            "WEGE3": "WEGE3.SA",
        }
        
        df_acoes.loc[:, "preco_atual_br"] = df_acoes["nome"].apply(
            lambda x: yf.Ticker(symbol_map.get(x, f"{x}.SA")).history(period="1d")["Close"].iloc[-1]
            if x in symbol_map or x.endswith(".SA") else 0.0
        )
        
        df_acoes.loc[:, "preco_compra_br"] = df_acoes["preco_inicial"]
        
        df_acoes.loc[:, "variacao_percentual_br"] = (
            (df_acoes["preco_atual_br"] - df_acoes["preco_compra_br"]) / df_acoes["preco_compra_br"] * 100
        ).round(2)
        
        df_acoes.loc[:, "valor_investido_br"] = df_acoes["quantidade"] * df_acoes["preco_compra_br"]
        
        return df_acoes
        
    except Exception as e:
        print(f"Erro ao obter preços atuais das ações: {str(e)}")
        return df