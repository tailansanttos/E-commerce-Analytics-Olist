from extract.extract_data_kaggle import extract_data
from extract.ingest_raw_to_bronze import raw_to_bronze
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

pipeline_main()