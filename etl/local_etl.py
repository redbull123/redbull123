import pandas as pd
import os
from pathlib import Path
import shutil
import logging
from dataclasses import dataclass
import sqlalchemy
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

@dataclass
class TelecomETL:
    """ETL pipeline for processing telecom signaling events."""
    raw_dir: str
    staging_dir: str
    processed_dir: str
    db_uri: str

    def extract_transform_load(self, logger: logging.Logger):
        """
        Executes the Extract, Transform, Load (ETL) process.

        Args:
            logger: Logging instance.
        """
        raw_dir = Path(self.raw_dir)
        staging_dir = Path(self.staging_dir)
        processed_dir = Path(self.processed_dir)
        logger.info(f"Raw directory: {raw_dir}")
        logger.info(f"Staging directory: {staging_dir}")
        logger.info(f"Processed directory: {processed_dir}")
        # Create directories if they don't exist
        staging_dir.mkdir(exist_ok=True)
        processed_dir.mkdir(exist_ok=True)

        if not raw_dir.exists():
            logger.info(f"Raw directory does not exist: {raw_dir}")
            return

        files_processed = 0

        for file in os.listdir(raw_dir):
            if file.startswith('events_') and file.endswith('.json'):
                try:
                    file_path = raw_dir / file
                    shutil.move(file_path, staging_dir / file)
                    file_path = staging_dir / file
                    logger.info(f"Processing file: {file}")

                    # Extract
                    df = pd.read_json(file_path)
                    logger.info(f"Extracted {len(df)} rows from {file}")

                    # Transform
                    if 'imsi' in df.columns:
                        df['imsi'] = df['imsi'].str.replace('IMSI_', '')
                    logger.info(f"Transformed {len(df)} rows")

                    # Load
                    engine = sqlalchemy.create_engine(self.db_uri)

                    df.to_sql('eventos', con=engine, if_exists='append', index=False)
                    logger.info(f"Data loaded successfully: {len(df)} rows")

                    # Move file to processed
                    shutil.move(file_path, processed_dir / file)
                    logger.info(f"File moved to processed: {file}")
                    files_processed += 1

                except Exception as e:
                    logger.error(f"Error processing file {file}: {e}")

        logger.info(f"ETL process completed. Files processed: {files_processed}")

def setup_logging() -> None:
    """Configures logging to output to both a file and the console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("etl_process.log"),
            logging.StreamHandler()
        ]
    )
def main():
    """Main entry point for the ETL process."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting ETL process...")

    # Configuration using environment variables with defaults
    raw_dir = os.getenv("RAW_DATA_DIR", "data/raw/")
    staging_dir = os.getenv("STAGING_DATA_DIR", "data/staging/")
    processed_dir = os.getenv("PROCESSED_DATA_DIR", "data/processed/")
    db_uri = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/telecom_analytics")

    etl_obj = TelecomETL(
        raw_dir=raw_dir,
        staging_dir=staging_dir,
        processed_dir=processed_dir,
        db_uri=db_uri
    )
    etl_obj.extract_transform_load(logger)

if __name__ == "__main__":
    main()
