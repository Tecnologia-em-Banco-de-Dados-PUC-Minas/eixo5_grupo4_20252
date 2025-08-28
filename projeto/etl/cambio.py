import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import requests

def _get_results_dir():
    """
    Retorna o diretório de resultados do projeto.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))

def baixar_historico_cambio():
    """
    Baixa o histórico dos últimos 10 anos das principais moedas em relação ao Real
    e salva em um arquivo CSV.
    """
    try:
        moedas = {
            "USDBRL=X": "Dólar Americano",
            "EURBRL=X": "Euro",
            "GBPBRL=X": "Libra Esterlina",
            "JPYBRL=X": "Iene Japonês",
            "CHFBRL=X": "Franco Suíço",
            "CNYBRL=X": "Yuan Chinês",
            "AUDBRL=X": "Dólar Australiano",
            "CADBRL=X": "Dólar Canadense",
        }

        data_inicial = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d")

        dados_historicos = []

        print("Iniciando download do histórico das moedas...")

        for simbolo, nome in moedas.items():
            try:
                moeda = yf.Ticker(simbolo)
                hist = moeda.history(start=data_inicial)

                if hist.empty:
                    continue

                hist["Simbolo"] = simbolo
                hist["Nome"] = nome

                hist = hist.reset_index()
                hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")

                dados_historicos.append(hist)

                print(f"Dados baixados para {nome} ({simbolo})")

            except Exception as e:
                print(f"Erro ao baixar dados de {simbolo}: {str(e)}")
                continue

        if dados_historicos:
            df_historico = pd.concat(dados_historicos, ignore_index=True)

            df_historico = df_historico[["Date", "Simbolo", "Nome", "Close"]]
            df_historico.columns = ["Data", "Simbolo", "Nome_Moeda", "Preco"]

            df_historico["Variacao"] = (
                df_historico.groupby("Simbolo")["Preco"].pct_change() * 100
            )

            results_dir = _get_results_dir()
            nome_arquivo = os.path.join(results_dir, "historico_cambio.csv")
            df_historico.to_csv(nome_arquivo, index=False)
            print(f"\nHistórico salvo com sucesso em '{nome_arquivo}'")

            return df_historico
        else:
            print("\nNenhum dado histórico foi baixado")
            return pd.DataFrame()

    except Exception as e:
        print(f"Erro ao processar dados históricos: {str(e)}")
        return pd.DataFrame()


def obter_variacao_cambio(periodo="1d"):
    """
    Obtém a variação das moedas no período especificado.

    Args:
        periodo (str): Período de análise ('1d' para 30 dias, '1mo' para mensal, '1y' para anual)
    """
    try:
        results_dir = _get_results_dir()
        nome_arquivo = os.path.join(results_dir, "historico_cambio.csv")
        df_historico = pd.read_csv(nome_arquivo)
        df_historico["Data"] = pd.to_datetime(df_historico["Data"])

        data_mais_recente = df_historico["Data"].max()

        if periodo == "1d":
            data_inicio = data_mais_recente - pd.Timedelta(days=30)
            df_periodo = df_historico[df_historico["Data"] >= data_inicio].copy()
            df_periodo = (
                df_periodo.groupby("Simbolo")
                .agg({"Preco": ["first", "last"], "Nome_Moeda": "first"})
                .reset_index()
            )
            df_periodo.columns = [
                "Simbolo",
                "Preco_Inicial",
                "Preco_Final",
                "Nome_Moeda",
            ]

        elif periodo == "1mo":
            df_historico["Mes_Ano"] = df_historico["Data"].dt.to_period("M")
            df_periodo = (
                df_historico.groupby(["Simbolo", "Mes_Ano", "Nome_Moeda"])["Preco"]
                .mean()
                .reset_index()
            )
            df_periodo = df_periodo.sort_values(["Simbolo", "Mes_Ano"])
            df_periodo = (
                df_periodo.groupby("Simbolo")
                .agg({"Preco": ["first", "last"], "Nome_Moeda": "first"})
                .reset_index()
            )
            df_periodo.columns = [
                "Simbolo",
                "Preco_Inicial",
                "Preco_Final",
                "Nome_Moeda",
            ]

        else:
            df_historico["Ano"] = df_historico["Data"].dt.year
            df_periodo = (
                df_historico.groupby(["Simbolo", "Ano", "Nome_Moeda"])["Preco"]
                .mean()
                .reset_index()
            )
            df_periodo = df_periodo.sort_values(["Simbolo", "Ano"])
            df_periodo = (
                df_periodo.groupby("Simbolo")
                .agg({"Preco": ["first", "last"], "Nome_Moeda": "first"})
                .reset_index()
            )
            df_periodo.columns = [
                "Simbolo",
                "Preco_Inicial",
                "Preco_Final",
                "Nome_Moeda",
            ]

        df_periodo["Variacao"] = (
            (df_periodo["Preco_Final"] / df_periodo["Preco_Inicial"]) - 1
        ) * 100

        if df_periodo.empty:
            return pd.DataFrame()

        df_periodo["Preço"] = df_periodo["Preco_Final"].round(
            4
        )
        df_periodo["Variação (%)"] = df_periodo["Variacao"].round(2)
        df_periodo["Símbolo"] = df_periodo["Simbolo"]
        df_periodo["Nome"] = df_periodo["Nome_Moeda"]

        return df_periodo[["Símbolo", "Nome", "Preço", "Variação (%)"]].sort_values(
            "Variação (%)", ascending=False
        )

    except Exception as e:
        print(f"Erro ao obter variação do câmbio: {str(e)}")
        return pd.DataFrame()


def get_usdbrl_rate():
    """
    Obtém a taxa de câmbio USD/BRL mais recente.
    """
    try:
        usdbrl = yf.Ticker("USDBRL=X")
        hist = usdbrl.history(period="1d", interval="1m")
        return hist["Close"].iloc[-1]
    except Exception as e:
        print(f"Erro ao buscar taxa USD/BRL: {e}")
        return 5.0