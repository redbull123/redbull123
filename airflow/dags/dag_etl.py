from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from airflow.decorators import dag, task
import pandas as pd
import os
from pathlib import Path
import shutil


default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id='dag_etl',
    default_args=default_args,
    start_date=datetime(2025, 1, 25, 2),
    schedule='@daily',
    catchup=False
)
def etl():
    @task
    def extract_transform_load():
        """
        Extracts data from raw files, transforms it, and loads it into the database.
        Paths are configured via environment variables with defaults.
        """
        # Configuration using environment variables with defaults
        raw_dir = Path(os.getenv("RAW_DATA_DIR", "/opt/airflow/dags/raw"))
        staging_dir = Path(os.getenv("STAGING_DATA_DIR", "/opt/airflow/dags/staging"))
        processed_dir = Path(os.getenv("PROCESSED_DATA_DIR", "/opt/airflow/dags/processed"))
        postgres_conn_id = os.getenv("POSTGRES_CONN_ID", "Test-dB")

        # Create directories if they don't exist
        staging_dir.mkdir(exist_ok=True)
        processed_dir.mkdir(exist_ok=True)

        if not raw_dir.exists():
            print(f"Raw directory does not exist: {raw_dir}")
            return

        files_processed = 0

        for file in os.listdir(raw_dir):
            if file.startswith('events_') and file.endswith('.json'):
                file_path = raw_dir / file
                print(f"Processing file: {file}")

                try:
                    # Extract
                    df = pd.read_json(file_path)
                    print(f"Extracted {len(df)} rows from {file}")

                    # Transform
                    if 'imsi' in df.columns:
                        df['imsi'] = df['imsi'].str.replace('IMSI_', '')
                    print(f"Transformed {len(df)} rows")

                    # Load
                    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
                    engine = hook.get_sqlalchemy_engine()
                    df.to_sql('eventos', con=engine, if_exists='append', index=False)
                    print(f"Data loaded successfully: {len(df)} rows")

                    # Move file to processed
                    shutil.move(file_path, processed_dir / file)
                    print(f"File moved to processed: {file}")
                    files_processed += 1

                except Exception as e:
                    print(f"Error processing file {file}: {e}")
                    # Move to staging for manual review
                    shutil.move(file_path, staging_dir / file)

        print(f"ETL process completed. Files processed: {files_processed}")

    # Execute the ETL process
    extract_transform_load()

etl_dag = etl()
