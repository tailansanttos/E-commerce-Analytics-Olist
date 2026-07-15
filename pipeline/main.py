from extract.extract_data_kaggle import extract_data
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('C:/E-commerce Analytics Olist/logs/main.log', encoding='utf-8'),
                               logging.StreamHandler()])
def pipeline_main():
    logging.info('Iniciando a pipeline ELT.')
    logging.info("Extraindo dados.")
    extract_data()
