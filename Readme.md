# Tradingbot

A modular, data-driven cryptocurrency trading bot built for historical signal analysis and backtesting. Designed to operate on high-frequency market data using technical indicators and strategy filters, it supports scalable experimentation with trading logic in both trending and range-bound conditions.
## Project Overview
TradingBot leverages 1-minute OHLCV data from KuCoin, applies key technical indicators, and evaluates multi-condition trading signals. It supports data persistence and queryable analytics through Google BigQuery, enabling systematic backtest evaluations and signal optimization.

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

## Enhancements in v2.0 and v2.1
### Signal Engine (fact_signals)
Introduced filter logic for multi-indicator signals including:

RSI bounce, MACD crossover, range breakout

Bollinger Band breakout, volume spike, strong candle detection

Detected candlestick patterns (Hammer, Doji, Engulfing Bull)

Stored filter combinations, match scores, and debug notes

### Backtesting Engine (backtest_trades_v2)
Enhanced backtesting logic with:

Trailing stop-loss and dynamic take-profit based on ATR

Trade classification: Scalp, Swing, Position

Cooldown logic after losses to prevent overtrading

Signal strength scaling: TP/SL adjusted based on match confidence

Computed trade-specific metrics:

Maximum Favorable Excursion (MFE)

Maximum Adverse Excursion (MAE)

ATR at trade exit

### Combo Strategy Optimization
Isolated and analyzed signal combinations for profitability and risk

Filtered high-confidence setups using:

Signal match score

ATR normalization

Performance in volatile vs. sideways regimes

Identified safest and most consistent signal sets for conservative execution

## Technologies

- Python
- Pandas
- Google Cloud BigQuery
- CCXT Library
- dotenv for environment management
- Looker Studio (for post-analysis)

## Data Architecture
| Table Name           | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `fact_prices`        | Price and indicator-enriched market data                                  |
| `fact_signals`       | Evaluated signals, triggered filters, match scores, and pattern detection |
| `backtest_trades_v2` | Trade entries/exits with dynamic TP/SL, PnL, MFE/MAE, and combo breakdown |


## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `.env` file and service account key in the `Keys/` folder
4. Run `main.py`

## Future Plans

- Upload processed data automatically to BigQuery
- Build trading strategies based on indicators
- Add live trading and risk management features




