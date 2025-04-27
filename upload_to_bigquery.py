# upload_to_bigquery.py

import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas as pd

# Load environment variables
load_dotenv()

# Set Google credentials for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Create a BigQuery Client
client = bigquery.Client()

def upload_dataframe_to_bigquery(df, table_name, write_mode="WRITE_APPEND"):
    """
    Uploads any DataFrame to BigQuery into the specified table.

    Parameters:
    ------------------------------------
    - df: pandas DataFrame you want to upload
    - table_name: BigQuery table name (example: 'fact_prices', 'dim_coins', etc.)
    - write_mode: 
        - 'WRITE_APPEND' (default) → adds new rows
        - 'WRITE_TRUNCATE' → deletes old data, uploads fresh

    Automatically detects schema from DataFrame columns.
    """

    project_id = "scalp-457602"         # Your GCP project id
    dataset_id = "crypto_data"          # Your BigQuery dataset

    # Build the full table path
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    # Set the upload job config
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_mode,
        autodetect=True,  # BigQuery guesses schema from DataFrame
    )

    # Upload the DataFrame
    job = client.load_table_from_dataframe(
        df,
        full_table_id,
        job_config=job_config
    )

    # Wait for upload to complete
    job.result()

    print(f"✅ Uploaded {len(df)} rows to {full_table_id} successfully.")
