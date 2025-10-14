import pandas as pd
from datetime import datetime
import os
import chardet
import re

def processar_ibrx50():
    """
    Processa o arquivo CSV do IBrX-50, limpando e formatando os dados.
    """
    data_atual = datetime.now().strftime("%d-%m-%y")

    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))
    arquivos_na_pasta = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if f.endswith(".csv")]

    if not arquivos_na_pasta:
        print("Nenhum arquivo .csv encontrado na pasta.")
    else:
        caminho_arquivo_recente = max(arquivos_na_pasta, key=os.path.getmtime)
        nome_arquivo_recente = os.path.basename(caminho_arquivo_recente)
        print(f"O arquivo baixado mais recentemente é: {nome_arquivo_recente}")
        
        padrao_data = r"(\d{2}-\d{2}-\d{2})"
        match = re.search(padrao_data, nome_arquivo_recente)
        
        if match:
            data_arquivo = match.group(1)
            print(f"Data do arquivo: {data_arquivo}")

    nome_arquivo = os.path.join(results_dir, f"IBXLDia_{data_arquivo}.csv")
    #nome_arquivo = os.path.join(results_dir, f"IBXLDia_{data_atual}.csv")

    if not os.path.exists(nome_arquivo):
        raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado!")

    try:
        with open(nome_arquivo, "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        print(f"Encoding detectado: {encoding}")

        with open(nome_arquivo, "r", encoding=encoding) as file:
            linhas = file.readlines()

        linhas_limpas = [linha.strip().rstrip(";") + "\n" for linha in linhas]

        dados_acoes = [linha for linha in linhas_limpas[2:] if linha.strip()]

        df = pd.DataFrame([linha.strip().split(";") for linha in dados_acoes])

        df.columns = ["Código", "Ação", "Tipo", "Qtde. Teórica", "Part. (%)"]

        df = df.iloc[:-2]

        try:
            df["Part. (%)"] = df["Part. (%)"].str.replace(",", ".").astype(float)
        except Exception as e:
            print("\nErro ao converter porcentagem:")
            print(f"Colunas disponíveis: {df.columns.tolist()}")
            print(f"Primeiras linhas do DataFrame:\n{df.head()}")
            raise e

        duplicatas = df.duplicated().sum()
        if duplicatas > 0:
            print(f"\nForam encontradas {duplicatas} linhas duplicadas")
            df = df.drop_duplicates()
            print(f"Duplicatas removidas. Novo número de linhas: {len(df)}")
        else:
            print("\nNão foram encontradas duplicatas")

        df_codigo = df[["Código"]]

        try:
            with open(nome_arquivo, "w", encoding="UTF-8") as file:
                file.write(f"IBXL - Carteira do Dia {data_atual}\n")

                file.write("Código\n")

                for codigo in df_codigo["Código"]:
                    file.write(f"{codigo}\n")

                print(
                    f"Arquivo salvo com sucesso apenas com os códigos: {nome_arquivo}"
                )
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {str(e)}")
            raise e

        print(f"\nInformações do arquivo {nome_arquivo}:")
        print(f"Número de linhas: {len(df)}")
        print("\nPrimeiras 5 linhas do DataFrame:")
        print(df.head())

        return df

    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None
