import os
import pandas as pd
from google.cloud import bigquery
from pathlib import Path


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "projeto-olist-elt-edaa00bbd190.json"

def carregar_dados_rar_para_bronze():
    client = bigquery.Client()
    id_projeto  = client.project
    dataset_id = "camada_bronze_olist"

    raiz_projeto = Path(__file__).parent
    caminho_raw = raiz_projeto / "data" / "raw"

    arquivos = list(caminho_raw.glob("*.csv"))
    print(f'Encontrados {len(arquivos)} arquivos.')

    for arquivo in arquivos:
        # PEga o nome do arquivo sem a extensão CSV, para usar como NOME DA TABELA
        nome_tabela = arquivo.stem
        destino = f"{id_projeto}.{dataset_id}.{nome_tabela}"

        print(f"Lendo {arquivo.name}")
        df = pd.read_csv(arquivo)

        # Nome das colunas pra STRING
        df.columns = df.columns.astype(str)

        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(df, destino, job_config=job_config)
        job.result()

        print(f"Tabeça {nome_tabela} carregada com {job.output_rows} linhas")
    