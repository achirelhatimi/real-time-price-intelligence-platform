from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='jumia_scraping_dag',
    default_args=default_args,
    description='Scraping quotidien de Jumia.ma',
    schedule_interval='0 0 * * *',
    start_date=datetime(2026, 3, 26),
    catchup=False,
) as dag:

    
    scraping_task = BashOperator(
    task_id='scraper_jumia',
    bash_command='cd /opt/airflow/dags && python3 -m scrapy crawl jumia',
)
    
