# main.py
import os
from dotenv import load_dotenv
from google.cloud import bigquery
from extracting import fetch_kucoin_candles  # <<< IMPORT your function properly
from transformation import add_ema,add_ema9_ema20, add_macd, add_rsi
from transformation import add_bollinger_bands
from transformation import add_atr
from upload_to_bigquery import upload_dataframe_to_bigquery


# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Connect to BigQuery
client = bigquery.Client()

# Test BigQuery connection
query_job = client.query("SELECT 'BigQuery is connected!' AS message")
results = query_job.result()

for row in results:
    print(row["message"])

# >>>>>>>>>>
# Now actually run your data fetching cleanly

df = fetch_kucoin_candles()

df=add_ema9_ema20(df)
df=add_macd(df)
df = add_rsi(df, period=14)
df = add_bollinger_bands(df, period=20, multiplier=2)
df = add_atr(df, period=14)




# Upload fact_prices
upload_dataframe_to_bigquery(df, table_name="fact_prices")
# Later if you create df_dim_coins:
# upload_dataframe_to_bigquery(df_dim_coins, "dim_coins")

# Print the DataFrame to verify
print(df.tail())






# main.py
#import os
#from dotenv import load_dotenv
#from google.cloud import bigquery
#from extracting import fetch_kucoin_candles  # <<< IMPORT your function properly

# Load environment variables
#load_dotenv()
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Connect to BigQuery
#client = bigquery.Client()

# Test BigQuery connection
#query_job = client.query("SELECT 'BigQuery is connected!' AS message")
#results = query_job.result()

#for row in results:
#    print(row["message"])

# >>>>>>>>>>
# Now actually run your data fetching cleanly

#df = fetch_kucoin_candles()

# Print the DataFrame to verify
#print(df.tail())

#import os
#from dotenv import load_dotenv
#from google.cloud import bigquery

#os means operating system, this is a core library in python that allows python to work on the operating system, by allowing user to set environment variables, read them, create/delete folders, work with file paths
#environment variables : They are key-value pairs that store configuration settings, API keys, and other sensitive information outside of the application code, or filepaths for stuff that is to be remained hidden
#Python provides the os module to interact with environment variables. The os.environ object is a dictionary-like mapping that represents the user's environment variables.
#To access an environment variable, use os.environ.get() or os.environ[].
#os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#→ Fetches the value from your .env file.
#(In your case, it's the full path to your service account JSON key.)

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ...
#→ Sets it inside your Python environment so that Google's libraries can see it.

# Load environment variables
#load_dotenv()

# Set Google credentials from .env
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

#os.environ is a dictionary-like object in Python that contains your computer's environment variables. Think of environment variables as hidden settings your operating system and apps use behind the scenes.
#your computer has a secret drawer called 'environment' inside it are labeled notes like: username=raghav, home=user/raghav, google_application_credentials=whatever path they may be
#os.environ is the way python opens that drawer and reads or writes notes in it




# Connect to BigQuery
#client = bigquery.Client()
#This creates a bigquery client object, this client now knows: which project it is in, what service account is being used, which APIs it can call
# now we can send commands to bigquery 


# Test query
#query_job = client.query("SELECT 'BigQuery is connected!' AS message")
#this sends a sql query to bigquery, return the message in a column named message
#results = query_job.result()
#this waits for the query to stop running, collects the results.


#for row in results:
#    print(row["message"])

#for each row in the table returned by bigquery print the message column



#import ccxt
#print(ccxt.exchanges)
#kucoin=ccxt.kucoin()
#btc_price=kucoin.fetch_ticker('BTC/USDT')
#print(btc_price['last'])



