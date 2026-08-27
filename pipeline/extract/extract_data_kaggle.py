import logging
import kagglehub
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

raiz_projeto = Path(__file__).parent.parent.parent
caminho_log = raiz_projeto / "logs" / "extract_data.log"
caminho_log.parent.mkdir(parents=True, exist_ok=True)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(caminho_log, encoding='utf-8'),
                               logging.StreamHandler()])

def extract_data():
    
    caminho_raw = raiz_projeto / "data" / "raw"
    # Cria a pasta caso nao exista
    caminho_raw.mkdir(parents=True, exist_ok=True)

    caminho_dataset = kagglehub.dataset_download('olistbr/brazilian-ecommerce')
    
    arquivos = [f for f in os.listdir(caminho_dataset) if f.endswith(".csv")]
    for arquivo in arquivos:
        origem = Path(caminho_dataset) / arquivo
        destino = caminho_raw / arquivo

        with open(origem, 'rb') as f_origem:
            with open(destino, 'wb') as f_destino:
                f_destino.write(f_origem.read())
        logging.info("Arquivos copiados com sucesso.")
    


