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
    project_id = "scalp-457602"
    dataset_id = "crypto_data"
    full_table_id = f"{project_id}.{dataset_id}.{table_name}"

    # Manual schema needed for array field
    if table_name == "backtest_trades":
        schema = [
            bigquery.SchemaField("timestamp", "DATETIME"),
            bigquery.SchemaField("symbol", "STRING"),
            bigquery.SchemaField("entry_price", "FLOAT"),
            bigquery.SchemaField("exit_price", "FLOAT"),
            bigquery.SchemaField("pnl_pct", "FLOAT"),
            bigquery.SchemaField("match_score", "INTEGER"),
            bigquery.SchemaField("exit_reason", "STRING"),
            bigquery.SchemaField("duration_candles", "INTEGER"),
            bigquery.SchemaField("atr_on_entry", "FLOAT"),
            bigquery.SchemaField("filters_triggered", "STRING"),
            bigquery.SchemaField("filters_triggered_list", "STRING", mode="REPEATED"),  #ARRAY<STRING>
            bigquery.SchemaField("final_signal", "BOOLEAN"),
        ]
    elif table_name == "backtest_trades_v2":
        schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("symbol", "STRING"),
            bigquery.SchemaField("entry_price", "FLOAT"),
            bigquery.SchemaField("exit_price", "FLOAT"),
            bigquery.SchemaField("exit_reason", "STRING"),
            bigquery.SchemaField("duration_candles", "INTEGER"),
            bigquery.SchemaField("pnl_pct", "FLOAT"),
            bigquery.SchemaField("was_profitable", "BOOLEAN"),
            bigquery.SchemaField("trade_type", "STRING"),
            bigquery.SchemaField("mfe_atr", "FLOAT"),
            bigquery.SchemaField("mae_atr", "FLOAT"),
            bigquery.SchemaField("tp_price", "FLOAT"),
            bigquery.SchemaField("sl_price", "FLOAT"),
            bigquery.SchemaField("atr_on_exit", "FLOAT"),
            bigquery.SchemaField("match_score", "INTEGER"),
            bigquery.SchemaField("rsi_bounce", "BOOLEAN"),
            bigquery.SchemaField("macd_cross_up", "BOOLEAN"),
            bigquery.SchemaField("recent_high_break", "BOOLEAN"),
            bigquery.SchemaField("range_breakout", "BOOLEAN"),
            bigquery.SchemaField("strong_candle", "BOOLEAN"),
            bigquery.SchemaField("volume_spike", "BOOLEAN"),
            bigquery.SchemaField("signal_combo_name", "STRING"),
            bigquery.SchemaField("logic_debug_note", "STRING"),
        ]

    else:
        schema = None

    job_config = bigquery.LoadJobConfig(
        write_disposition=write_mode,
        autodetect=(schema is None),
        schema=schema
    )

    job = bigquery.Client().load_table_from_dataframe(
        df,
        full_table_id,
        job_config=job_config
    )

    job.result()
    print(f"✅ Uploaded {len(df)} rows to {full_table_id} successfully.")
