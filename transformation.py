# transforming.py

import pandas as pd

# -----------------------------------------------
# Manual Mathematical Calculation of EMA (Commented for Reference)
# -----------------------------------------------

"""
def calculate_ema(prices, span):
    '''
    prices = list of closing prices
    span = number of periods for EMA (example: 9, 20)

    EMA Mathematical Formula (Recursive):
    --------------------------------------
    K = 2 / (span + 1)

    EMA_today = (Price_today × K) + (EMA_yesterday × (1 - K))

    Step 1: Start with SMA (Simple Moving Average) of the first 'span' closes:
    SMA = (Price_1 + Price_2 + ... + Price_n) / n

    Step 2: Then for each next price:
    EMA_today = (Current_Price × K) + (Previous_EMA × (1 - K))

    Note: If there are fewer than 'span' prices, EMA cannot be calculated.
    '''

    ema_values = []
    k = 2 / (span + 1)  # smoothing factor

    if len(prices) < span:
        return []  # Not enough data to calculate EMA

    # Step 1: Start with SMA as the first EMA value
    sma = sum(prices[:span]) / span
    ema_values.append(sma)

    # Step 2: Apply EMA formula recursively
    for price in prices[span:]:
        ema_yesterday = ema_values[-1]
        ema_today = (price * k) + (ema_yesterday * (1 - k))
        ema_values.append(ema_today)

    return ema_values
"""

# -----------------------------------------------
# Actual Code Using Pandas ewm() to Add EMA Columns
# -----------------------------------------------

def add_ema(df, span, column_name):
    """
    Adds an Exponential Moving Average (EMA) column to the DataFrame.
    
    - Uses pandas ewm() method which internally follows the same EMA formula.
    - EMA cannot be calculated if available data points < span (pandas handles this automatically by setting NaN).
    """
    if len(df) < span:
        df[column_name] = pd.NA  # Not enough data, assign NA
    else:
        df[column_name] = df['close'].ewm(span=span, adjust=False).mean()
    
    return df

def add_ema9_ema20(df):
    """
    Adds both EMA 9 and EMA 20 columns to the DataFrame.
    
    EMA 9 → Short-term trend
    EMA 20 → Medium-term trend
    """
    df = add_ema(df, span=9, column_name='ema_9')
    df = add_ema(df, span=20, column_name='ema_20')
    return df


# transforming.py

# -----------------------------------------------
# MACD (Moving Average Convergence Divergence) - Mathematical Explanation
# -----------------------------------------------

"""
MACD is a momentum-trend indicator using EMAs.

Steps to calculate MACD:
-----------------------------------------------
1. Calculate EMA_12 (12-period Exponential Moving Average of Close prices)
2. Calculate EMA_26 (26-period Exponential Moving Average of Close prices)
3. MACD Line = EMA_12 - EMA_26

4. Calculate Signal Line = 9-period EMA of MACD Line
5. Histogram = MACD Line - Signal Line

Formulas:
-----------------------------------------------
EMA_today = (Price_today × (2 / (n + 1))) + (EMA_yesterday × (1 - (2 / (n + 1))))
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line

**Minimum data needed:**
- At least 26 rows to start calculating MACD
- At least 35 rows to have stable MACD and Signal together
"""

# -----------------------------------------------
# Actual Function to Add MACD Columns
# -----------------------------------------------

def add_macd(df):
    """
    Adds MACD Line, Signal Line, and MACD Histogram to the DataFrame.
    """
    if len(df) < 26:
        # Not enough data to calculate proper MACD
        df['macd'] = pd.NA
        df['macd_signal'] = pd.NA
        df['macd_histogram'] = pd.NA
        return df
    
    # Step 1: Calculate EMA 12 and EMA 26 of Close Prices
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    
    # Step 2: MACD Line = EMA 12 - EMA 26
    df['macd'] = ema_12 - ema_26
    
    # Step 3: Signal Line = EMA 9 of MACD Line
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    # Step 4: MACD Histogram = MACD Line - Signal Line
    df['macd_histogram'] = df['macd'] - df['macd_signal']
    
    return df


# transforming.py

import pandas as pd

# -----------------------------------------------
# RSI (Relative Strength Index) - Mathematical Explanation
# -----------------------------------------------

"""
RSI measures the strength of recent price movements to detect overbought/oversold conditions.

Steps to calculate RSI:
------------------------------------------------
1. Calculate "Change" = Today's Close - Yesterday's Close
2. Separate positive "Gains" and negative "Losses"
3. Calculate average Gain and average Loss over 'period' (default 14)
   - First Average = Simple Moving Average (SMA)
   - After that, use smoothed averages (Wilder's Smoothing)
4. Calculate RS (Relative Strength) = (Average Gain) / (Average Loss)
5. Calculate RSI:
   RSI = 100 - (100 / (1 + RS))

Notes:
------------------------------------------------
- If average loss is 0 → RSI = 100 (perfect uptrend)
- If average gain is 0 → RSI = 0 (perfect downtrend)
- RSI oscillates between 0 and 100.
"""

# -----------------------------------------------
# Actual Function to Add RSI Column
# -----------------------------------------------

def add_rsi(df, period=14):
    
    """
    Adds an RSI column to the DataFrame using 'close' prices.
    
    Parameters:
    - df: pandas DataFrame
    - period: number of periods to calculate RSI over (default = 14)
    """

    if len(df) < period:
        df['rsi'] = pd.NA
        return df

    # Step 1: Calculate daily price changes
    delta = df['close'].diff()

    # Step 2: Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)  # negative losses converted to positive

    # Step 3: Calculate average gain and loss
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Step 4: Use Wilder's smoothing for subsequent values
    avg_gain = avg_gain.fillna(method='ffill')
    avg_loss = avg_loss.fillna(method='ffill')

    # Step 5: Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Step 6: Add RSI to DataFrame
    df['rsi'] = rsi

    return df


# transforming.py
# -----------------------------------------------
# Bollinger Bands - Full Mathematical Explanation
# -----------------------------------------------

"""
Bollinger Bands measure volatility based on standard deviation.

Formulas:
------------------------------------------------
1. Middle Band = SMA (Simple Moving Average) of Close Prices over 'period'
2. Standard Deviation (σ) = square root of variance over 'period'
3. Upper Band = Middle Band + (multiplier × σ)
4. Lower Band = Middle Band - (multiplier × σ)

Default Settings:
------------------------------------------------
- period = 20
- multiplier = 2
"""

# -----------------------------------------------
# Function to Add Bollinger Bands Columns
# -----------------------------------------------

def add_bollinger_bands(df, period=20, multiplier=2):
    """
    Adds Middle Band, Upper Band, and Lower Band columns to the DataFrame.
    
    Parameters:
    - df: pandas DataFrame with 'close' prices
    - period: number of periods to calculate bands (default=20)
    - multiplier: number of StdDev to widen/narrow bands (default=2)
    """

    if len(df) < period:
        # Not enough data to calculate Bollinger Bands
        df['bb_middle'] = pd.NA
        df['bb_upper'] = pd.NA
        df['bb_lower'] = pd.NA
        return df

    # Step 1: Middle Band (Simple Moving Average of 'close')
    df['bb_middle'] = df['close'].rolling(window=period, min_periods=period).mean()

    """df['close']	Pandas Series	The closing prices column from your DataFrame.
    .rolling(window=period, min_periods=period)	Rolling Object	Creates a "sliding window" of size period (like a small moving dataset).
    .mean()	Method	For each window, compute the Simple Moving Average.
    df['bb_middle'] = ...	Assignment	Store the result into a new column called 'bb_middle'.
Rolling Window =

Imagine a sliding ruler that covers 20 candles (if period=20)

It slides one candle at a time.

Each time, it averages the 20 closes under it.

Moves forward by 1, repeats.

✅ rolling() doesn't compute anything itself — it prepares the moving window.

✅ .mean() tells it what to compute on each window.
    """




    # Step 2: Standard Deviation of 'close'
    std = df['close'].rolling(window=period, min_periods=period).std()
#same logic but for this we are storing the result in a vardiable, std which is the standard deviation, if you see the end of this line there is a std deviation object called on the 
#the rolling window instead of the .mean() which usually calculates the SMA
#✅ std is a Pandas Series.

#✅ Each value inside std is:

#The Standard Deviation of the last period (example: 20) candles at that point.

#✅ So std is a column where:

#For every new row (after enough candles),

#It stores the standard deviation calculated from the rolling window just behind it.


    # Step 3: Upper Band and Lower Band

    df['bb_upper'] = df['bb_middle'] + (multiplier * std)
    df['bb_lower'] = df['bb_middle'] - (multiplier * std)

    return df

# transforming.py

# -----------------------------------------------
# Average True Range (ATR) - Mathematical Explanation
# -----------------------------------------------

"""
ATR measures the average volatility over a set period.

Steps:
------------------------------------------------
1. True Range (TR) = max(High-Low, |High-PreviousClose|, |Low-PreviousClose|)
2. ATR = Simple Moving Average (SMA) of TR over 'period' (default 14)

Default Settings:
------------------------------------------------
- period = 14
"""

# -----------------------------------------------
# Function to Add ATR Column
# -----------------------------------------------

def add_atr(df, period=14):
    """
    Adds an ATR column to the DataFrame.
    
    Parameters:
    - df: pandas DataFrame with 'high', 'low', 'close' columns
    - period: number of periods to calculate ATR (default=14)
    """

    if len(df) < period:
        df['atr'] = pd.NA
        return df

    # Step 1: Calculate Previous Close
    prev_close = df['close'].shift(1)

#✅ SYNTAX:

#df['close'] → The Series (column) of close prices.
#.shift(1) → Shift the entire Series down by 1 row.
#LOGIC:
#This gives you Yesterday’s close for today's row.
#Because True Range sometimes needs to compare today's High/Low with yesterday's Close (to capture gaps).
#


    # Step 2: Calculate True Range (TR)
    tr1 = df['high'] - df['low']
#Simple subtraction between high and low prices for each row.
    tr2 = (df['high'] - prev_close).abs()
    #(df['high'] - prev_close) → Subtract yesterday's close from today's high.
#.abs() → Take the absolute value (make it positive).
#If price gapped up overnight (opened much higher),
#then today's High could be much higher than yesterday's Close.
#Always positive because volatility is size, not direction.
    tr3 = (df['low'] - prev_close).abs()

#(df['low'] - prev_close) → Subtract yesterday's close from today's low.

#.abs() → Take the absolute value.
#If price gapped down overnight (opened much lower),
#Then today's Low could be much lower than yesterday's Close.
#Again positive always — size of movement matters, not direction.

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    #pd.concat([tr1, tr2, tr3], axis=1) →ombine tr1, tr2, tr3 side-by-side into a mini DataFrame of 3 columns.
    #.max(axis=1) →For each row, take the maximum value across these 3 columns.
    #True Range is the largest of: High-Low (normal range), High-PreviousClose (gap up), Low-PreviousClose (gap down).
    #

    # Step 3: Calculate ATR as the moving average of TR
    df['atr'] = tr.rolling(window=period, min_periods=period).mean()

    return df
