import os
from google.cloud import bigquery
from pathlib import Path
import logging


raiz_projeto = Path(__file__).parent.parent.parent
caminho_log = raiz_projeto / "logs" / "modelagem_star.log"
caminho_log.parent.mkdir(parents=True, exist_ok=True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(caminho_log, encoding='utf-8'),
                               logging.StreamHandler()])


def transform_gold_in_bigquery():
    cliente = bigquery.Client()

    raiz_projeto = Path(__file__).parent.parent.parent
    caminho_sql = raiz_projeto / 'sql'

    arquivos_sql = list(caminho_sql.glob("*.sql"))
    if not arquivos_sql:
        logging.warning(f"Nenhum arquivo sql encontrado na pasta {caminho_sql}")
        return

    logging.info("Iniciando modelagem  da camada gold no Bigquery")

    for arquivo in arquivos_sql:
        nome_arquivo = arquivo.name
        logging.info(f'Executando query {nome_arquivo}')

        with open(arquivo, 'r', encoding='utf-8') as f:
            query = f.read()
        try:
            query_job = cliente.query(query)
            query_job.result()
            logging.info(f'Sucesso!! Tabela da {nome_arquivo} criada/atualizada na gold.')
        except Exception as e:
            logging.error(f'Erro ao executar query.')

