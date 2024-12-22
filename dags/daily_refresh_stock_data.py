import sys
import os

# Add the 'include' directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
include_path = os.path.join(current_dir, '../include')
sys.path.insert(0, include_path)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import logging

# Import custom functions and constants
from variables import DB_CONFIG, STOCKS
from constants import (
    COMPANY_INFO_COLUMNS,
    STOCK_FUNDAMENTALS_COLUMNS,
    STOCK_RECOMMENDATIONS_COLUMNS,
    PRICE_HISTORY_COLUMNS,
    HISTORY_START_DATE,
    HISTORY_END_DATE
)
from utils import get_company_info, store_dataframe_in_mysql, get_price_history

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define local timezone
Local_TimeZone =  pendulum.timezone("Europe/Amsterdam")

# DAG definition
with DAG(
    dag_id = 'daily_refresh_stock_data',
    default_args = default_args,
    description = 'Extracts Stock and Company Data from yfinance on a daily basis on every working day (EOD) and stores it in MySQL',
    schedule_interval = "0 18 * * 1-5", #Run every workday at 18:00
    start_date = datetime(2023, 1, 1, tzinfo=Local_TimeZone),
    catchup = False,
    tags = ['EOD Stock and Company Data'],
) as dag:

    # Task to extract company info data
    def extract_company_info():
        logging.info("Starting extraction of company info.")
        company_info_df = get_company_info(STOCKS, COMPANY_INFO_COLUMNS)
        logging.info(f"Extracted company info for stocks: {STOCKS}.")
        logging.debug(f"Extracted DataFrame:\n{company_info_df}")
        return company_info_df

    # Task to extract stock fundamentals data
    def extract_stock_fundamentals():
        logging.info("Starting extraction of stock fundamentals.")
        stock_fundamentals_df = get_company_info(STOCKS, STOCK_FUNDAMENTALS_COLUMNS)
        logging.info(f"Extracted stock fundamentals for stocks: {STOCKS}.")
        logging.debug(f"Extracted DataFrame:\n{stock_fundamentals_df}")
        return stock_fundamentals_df

    # Task to extract stock recommendations data
    def extract_stock_recommendations():
        logging.info("Starting extraction of stock recommendations.")
        stock_recommendations_df = get_company_info(STOCKS, STOCK_RECOMMENDATIONS_COLUMNS)
        logging.info(f"Extracted stock recommendations for stocks: {STOCKS}.")
        logging.debug(f"Extracted DataFrame:\n{stock_recommendations_df}")
        return stock_recommendations_df
    
    # Task to extract price history data
    def extract_price_history():
        logging.info("Starting extraction of price history.")
        price_history_df = get_price_history(HISTORY_START_DATE, HISTORY_END_DATE,STOCKS, PRICE_HISTORY_COLUMNS)
        logging.info(f"Extracted price history for stocks: {STOCKS}.")
        logging.debug(f"Extracted DataFrame:\n{price_history_df}")
        return price_history_df

    # Task to store company info data
    def store_company_info(**kwargs):
        company_info_df = kwargs['ti'].xcom_pull(task_ids='extract_company_info')
        logging.info("Storing company info data into MySQL.")
        store_dataframe_in_mysql(
            df=company_info_df,
            table_name="company_info",
            column_definitions=COMPANY_INFO_COLUMNS,
            db_config=DB_CONFIG,
        )
        logging.info("Company info data successfully stored in MySQL.")

    # Task to store stock fundamentals data
    def store_stock_fundamentals(**kwargs):
        stock_fundamentals_df = kwargs['ti'].xcom_pull(task_ids='extract_stock_fundamentals')
        logging.info("Storing stock fundamentals data into MySQL.")
        store_dataframe_in_mysql(
            df=stock_fundamentals_df,
            table_name="stock_fundamentals",
            column_definitions=STOCK_FUNDAMENTALS_COLUMNS,
            db_config=DB_CONFIG,
        )
        logging.info("Stock fundamentals data successfully stored in MySQL.")

    # Task to store stock recommendations data
    def store_stock_recommendations(**kwargs):
        stock_recommendations_df = kwargs['ti'].xcom_pull(task_ids='extract_stock_recommendations')
        logging.info("Storing stock recommendations data into MySQL.")
        store_dataframe_in_mysql(
            df=stock_recommendations_df,
            table_name="stock_recommendations",
            column_definitions=STOCK_RECOMMENDATIONS_COLUMNS,
            db_config=DB_CONFIG,
        )
        logging.info("Stock recommendations data successfully stored in MySQL.")

    # Task to store price history data
    def store_price_history(**kwargs):
        price_history_df = kwargs['ti'].xcom_pull(task_ids='extract_price_history')
        logging.info("Storing price history data into MySQL.")
        store_dataframe_in_mysql(
            df=price_history_df,
            table_name="price_history",
            column_definitions=PRICE_HISTORY_COLUMNS,
            db_config=DB_CONFIG,
        )
        logging.info("Price history data successfully stored in MySQL.")

    # Define extraction tasks
    extract_company_info_task = PythonOperator(
        task_id='extract_company_info',
        python_callable=extract_company_info,
    )

    extract_stock_fundamentals_task = PythonOperator(
        task_id='extract_stock_fundamentals',
        python_callable=extract_stock_fundamentals,
    )

    extract_stock_recommendations_task = PythonOperator(
        task_id='extract_stock_recommendations',
        python_callable=extract_stock_recommendations,
    )

    extract_price_history_task = PythonOperator(
        task_id='extract_price_history',
        python_callable=extract_price_history,
    )

    # Define storage tasks
    store_company_info_task = PythonOperator(
        task_id='store_company_info',
        python_callable=store_company_info,
        provide_context=True,
    )

    store_stock_fundamentals_task = PythonOperator(
        task_id='store_stock_fundamentals',
        python_callable=store_stock_fundamentals,
        provide_context=True,
    )

    store_stock_recommendations_task = PythonOperator(
        task_id='store_stock_recommendations',
        python_callable=store_stock_recommendations,
        provide_context=True,
    )

    store_price_history_task = PythonOperator(
        task_id='store_price_history',
        python_callable=store_price_history,
        provide_context=True,
    )

    # Define task dependencies
    extract_company_info_task >> store_company_info_task
    extract_stock_fundamentals_task >> store_stock_fundamentals_task
    extract_stock_recommendations_task >> store_stock_recommendations_task
    extract_price_history_task >> store_price_history_task