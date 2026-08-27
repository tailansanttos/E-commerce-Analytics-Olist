import os
import pandas as pd
import pandas_gbq as pbq
from google.cloud import bigquery
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()

raiz_projeto = Path(__file__).parent.parent.parent
caminho_log = raiz_projeto / "logs" / "load_bigquery.log"
caminho_log.parent.mkdir(parents=True, exist_ok=True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(caminho_log, encoding='utf-8'),
                               logging.StreamHandler()])

def load_silver_to_bigquery():
    client = bigquery.Client()
    id_projeto  = client.project
    dataset_id = "olist_silver"

    raiz_projeto = Path(__file__).parent.parent.parent
    caminho_silver = raiz_projeto / "data" / "silver"

    arquivos_parquet = list(caminho_silver.glob("*.parquet"))
    if not arquivos_parquet:
        logging.warning(f'Nenhum dado encontrado.')
        return

    for arquivo in arquivos_parquet:
        nome_tabela = arquivo.name.replace(".parquet", "")
        destino_bq = f'{dataset_id}.{nome_tabela}'
        logging.info(f'Inicianddo UPLOAD de {nome_tabela} para o Bigquery.')

        try:
            df = pd.read_parquet(arquivo)
            pbq.to_gbq(dataframe=df,destination_table=destino_bq, project_id=id_projeto, if_exists='replace')
            logging.info(f'Sucesso Tabela {destino_bq} carregada.')
        except Exception as e:
            logging.error(f'Erro ao subir tabela {nome_tabela}: {e}')

   
    