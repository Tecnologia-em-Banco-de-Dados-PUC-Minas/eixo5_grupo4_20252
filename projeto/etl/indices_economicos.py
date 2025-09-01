from bcb import sgs
from datetime import datetime, timedelta
import pandas as pd
import os

def _get_results_dir():
    """
    Retorna o diretório de resultados do projeto.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))

def buscar_dados_economicos():
    """
    Busca os dados econômicos do Banco Central do Brasil e salva em um arquivo CSV.
    """
    data_final = datetime.now()
    data_inicial = data_final - timedelta(days=365*10)
    
    codigos = {
        'SELIC': 432,
        'IPCA': 433,
        'IGP-M': 189,
        'INPC': 188,
        'CDI': 12,
        'PIB_MENSAL': 4380
    }
    
    dados = {}
    
    for nome, codigo in codigos.items():
        try:
            df = sgs.get({nome: codigo}, start=data_inicial, end=data_final)
            dados[nome] = df
        except Exception as e:
            print(f"Erro ao buscar dados do {nome}: {str(e)}")
    
    df_final = pd.concat(dados.values(), axis=1)
    
    results_dir = _get_results_dir()
    nome_arquivo = os.path.join(results_dir, 'dados_economicos.csv')
    df_final.to_csv(nome_arquivo)
    
    return df_final

if __name__ == "__main__":
    buscar_dados_economicos()