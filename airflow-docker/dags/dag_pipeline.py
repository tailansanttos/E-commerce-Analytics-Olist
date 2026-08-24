from airflow import DAG
from pathlib import Path
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from pipeline.extract.extract_data_kaggle import extract_data
from pipeline.extract.ingest_raw_to_bronze import raw_to_bronze
from pipeline.transform.silver.transform import orquestrador_transformacoes
from pipeline.load.load_bgq import load_silver_to_bigquery
from pipeline.transform.gold.transform_bqg import transform_gold_in_bigquery



default_args = {'owner':'Tailan', 'retries':2, 'retry_delay':timedelta(minutes=5)}
with DAG(dag_id='dag_pipeline_ecommerce_olist', default_args=default_args, 
         schedule="@daily", start_date=datetime(2026, 8, 23), description='Airflow Pipeline dados olist.', 
         tags=['airflow', 'python', 'dados_ecommerce']) as dag:
    
    tarefa_ingestao_dados = PythonOperator(
        task_id='ingestao_dados',
        python_callable= extract_data
    )
    tarefa_data_raw_to_bronze = PythonOperator(
        task_id = 'mover_dados_para_bronze',
        python_callable= raw_to_bronze
    )
    tarefa_transformar_dados = PythonOperator(
        task_id = 'transformacao_dados',
        python_callable= orquestrador_transformacoes
    )
    tarefa_salvar_bigquery = PythonOperator(
        task_id = 'salvar_dados',
        python_callable= load_silver_to_bigquery
    )
    tarefa_modelagem_star = PythonOperator(
        task_id = 'modelagem_datawarehouse',
        python_callable= transform_gold_in_bigquery
    )

    (tarefa_ingestao_dados >> tarefa_data_raw_to_bronze >> tarefa_transformar_dados >> tarefa_salvar_bigquery >> tarefa_modelagem_star)