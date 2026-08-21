from extract.extract_data_kaggle import extract_data
from extract.ingest_raw_to_bronze import raw_to_bronze
from transform.silver.transform import orquestrador_transformacoes
from load.load_bgq import load_silver_to_bigquery
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('C:/E-commerce Analytics Olist/logs/main.log', encoding='utf-8'),
                               logging.StreamHandler()])
def pipeline_main():
    logging.info('Iniciando a pipeline ELT.')
    logging.info("Extraindo dados.")
    extract_data()
    logging.info(f'Convertendo dados para parquet.')
    raw_to_bronze()

    logging.info(f'Iniciando transformações.')
    orquestrador_transformacoes()

    logging.info(f'Iniciando LOAD ao Bigquery.')
    load_silver_to_bigquery()

pipeline_main()