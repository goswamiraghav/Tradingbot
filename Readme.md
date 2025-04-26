# Tradingbot

A beginner-friendly cryptocurrency trading bot project.

## Features

- Fetches historical OHLCV data from KuCoin
- Calculates popular technical indicators:
  - EMA (9, 20)
  - MACD
  - RSI
  - Bollinger Bands
  - ATR
- Prepares clean datasets for backtesting and live trading
- Connected to Google BigQuery for future storage and analysis

## Technologies

- Python
- Pandas
- Google Cloud BigQuery
- CCXT Library
- dotenv for environment management

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `.env` file and service account key in the `Keys/` folder
4. Run `main.py`

## Future Plans

- Upload processed data automatically to BigQuery
- Build trading strategies based on indicators
- Add live trading and risk management features
