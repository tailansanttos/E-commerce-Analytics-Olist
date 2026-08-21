import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('C:/E-commerce Analytics Olist/logs/main.log', encoding='utf-8'),
                               logging.StreamHandler()])



def extract_data():
    raiz_projeto = Path(__file__).parent.parent.parent.parent
    pasta_bronze = raiz_projeto / 'data' / 'bronze'

    arquivos_parquet = list(pasta_bronze.glob('*.parquet'))
    if not arquivos_parquet:
        logging.warning(f'Nenhum arquivo encontrado na pasta {pasta_bronze}')
        return

    dfs_bronze = {}

    for arquivo in arquivos_parquet:
        nome_limpo = arquivo.name.replace(".parquet", "")
        
        try:
            dfs_bronze[nome_limpo] = pd.read_parquet(arquivo)
            logging.info(f'Arquivo {nome_limpo} carregado com sucesso.')
        except Exception as e:
            logging.error(f'Erro ao ler arquivo {arquivo.name}: {e}')
    return dfs_bronze




''' PRA CADA DATAFRAME, BUSCAR PELO NOME'''
def converter_datetime_orders(df:pd.DataFrame):
    colunas_orders_dates = ['order_purchase_timestamp',
       'order_approved_at', 'order_delivered_carrier_date',
       'order_delivered_customer_date', 'order_estimated_delivery_date']
    
    for coluna in colunas_orders_dates:
        df[coluna] = pd.to_datetime(df[coluna])
        logging.info(f'Coluna {coluna} mudada para o tipo DateTime.')
    return df

def converter_datetime_ordem_items(df:pd.DataFrame):
    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'])
    return df


def converter_datetime_order_reviews(df:pd.DataFrame):
    colunas_converter_reviews = ['review_creation_date', 'review_answer_timestamp']
    for coluna in colunas_converter_reviews:
        df[coluna] = pd.to_datetime(df[coluna])
    return df

def remover_duplicatas_geolocation(df:pd.DataFrame):
    df = df.drop_duplicates(subset=['geolocation_zip_code_prefix'], keep='first')
    return df

def preencher_nulos_dimensoes_peso(df:pd.DataFrame):
    colunas_preencher = ['product_weight_g',
       'product_length_cm', 'product_height_cm', 'product_width_cm']
    for coluna in colunas_preencher:
        mediana_coluna = df[coluna].median()
        df[coluna] = df[coluna].fillna(mediana_coluna)
    return df

def join_products_colunas(df1:pd.DataFrame, df2:pd.DataFrame):
    df1 = df1.merge(right=df2, on='product_category_name', how='left')
    df1 = df1.rename(columns={'product_category_name_english_x': 'product_category_name_english'})
    return df1


def salvar_silver(df:pd.DataFrame, nome_arquivo):
    raiz_projeto  = Path(__file__).parent.parent.parent.parent
    pasta_silver = raiz_projeto / 'data' / 'silver'
    pasta_silver.mkdir(exist_ok=True, parents=True)

    caminho_arquivo = pasta_silver / f'{nome_arquivo}_silver.parquet'

    df.to_parquet(path=caminho_arquivo, index=False, engine='pyarrow')


def orquestrador_transformacoes():
    logging.info(f'Iniciando trasnformações da camada Silver')

    dfs = extract_data()

    if not dfs:
        logging.error(f'Nenhum dado extraido.')
        return

    if 'orders' in dfs:
        dfs['orders'] = converter_datetime_orders(dfs['orders'])
    if 'order_items' in dfs:
        dfs['order_items'] = converter_datetime_ordem_items(dfs['order_items'])
    if 'order_reviews' in dfs:
        dfs['order_reviews'] = converter_datetime_order_reviews(dfs['order_reviews'])
    if 'geolocation' in dfs:
        dfs['geolocation'] = remover_duplicatas_geolocation(dfs['geolocation'])
    if 'prodcuts' in dfs:
        dfs['products'] = preencher_nulos_dimensoes_peso(dfs['products'])

        if 'product_category_name_translation' in dfs:
            dfs['products'] = join_products_colunas(df1=dfs['products'], 
                                                    df2=dfs['product_category_name_translation'])

    logging.info('Iniciando carregamento para a camada Silver')
    for nome_tabela, dataframe in dfs.items():
        try:
            salvar_silver(dataframe, nome_tabela)
            logging.info(f'Tabela {nome_tabela} salva com sucesso.')
        except Exception as e:
            logging.error(f'Erro ao salvar {nome_tabela} na silver: {e}')

    