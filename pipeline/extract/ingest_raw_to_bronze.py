import logging
import os
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('C:/E-commerce Analytics Olist/logs/extract_data.log', encoding='utf-8'),
                               logging.StreamHandler()])

def raw_to_bronze():
    raiz_projeto = Path(__file__).parent.parent.parent
    pasta_raw = raiz_projeto / 'data' / 'raw'
    pasta_bronze = raiz_projeto / 'data' / 'bronze'

    pasta_bronze.mkdir(parents=True, exist_ok=True)

    arquivos_csv = list(pasta_raw.glob("*.csv"))
    if not arquivos_csv:
        logging.warning(f'Nenhum arquivo CSV encontrado na pasta {pasta_raw}')
        return

    for caminho_csv in arquivos_csv:
        nome_original = caminho_csv.name

        nome_limpo = nome_original.replace('olist_', '').replace('_dataset.csv', '').replace(".csv", "")
        caminho_parquet = pasta_bronze / f'{nome_limpo}.parquet'

        logging.info(f'Processando: {nome_original} -> {caminho_parquet}')
        try:
            df = pd.read_csv(caminho_csv)
            df.to_parquet(caminho_parquet, engine='pyarrow', index=False)
        except Exception as e:
            logging.error(f'Erro ao processar {nome_original}: {e}')