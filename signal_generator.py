# signal_generator.py

def generate_signal_row(df):
    current = df.iloc[-1]  # Current candle
    prev = df.iloc[-2]     # Previous candle (for engulfing check)

    # --- Rolling logic windows ---
    recent_high = df['close'].rolling(window=20).max().shift(1)
    breakout_up = current['close'] > recent_high.iloc[-1]
    # Market: price just broke recent resistance
    # Math: close > max(close of last 20 candles)

    range_size = df['high'].rolling(20).max() - df['low'].rolling(20).min()
    range_breakout = (current['close'] > df['high'].rolling(20).max().shift(1).iloc[-1]) and (range_size.iloc[-1] > current['atr'])
    # Market: range was tight, and price just broke above it
    # Math: breakout confirmed by range width vs ATR

    body = abs(current['close'] - current['open'])
    candle_strength = body > current['atr'] * 0.7
    # Market: large candle body = strong conviction
    # Math: body must be at least 70% of volatility (ATR)

    avg_vol = df['volume'].rolling(20).mean()
    volume_spike = current['volume'] > avg_vol.iloc[-1] * 1.2
    # Market: sudden spike in volume confirms move
    # Math: volume > 1.5× rolling average volume

    rsi_ok = 45 <= current['rsi'] <= 52
    # Market: RSI bounce zone in bullish trends
    # Math: RSI must be in tight mid-range

    macd_cross_up = current['macd'] > current['macd_signal']
    # Market: MACD line crossing signal = momentum shift
    # Math: MACD > signal = bullish signal

    # --- Candlestick patterns ---
    upper_wick = current['high'] - max(current['open'], current['close'])
    lower_wick = min(current['open'], current['close']) - current['low']

    is_hammer = (lower_wick > 2 * body) and (upper_wick < 0.2 * body)
    is_doji = body < (current['high'] - current['low']) * 0.1
    is_engulfing_bull = (
        (prev['close'] < prev['open']) and
        (current['close'] > current['open']) and
        (current['close'] > prev['open']) and
        (current['open'] < prev['close'])
    )

    # --- Final decision ---
    """final_signal = all([
        breakout_up,
        range_breakout,
        candle_strength,
        volume_spike,
        rsi_ok,
        macd_cross_up
    ])
"""
    match_score = sum([
        breakout_up,
        range_breakout,
        candle_strength,
        volume_spike,
        rsi_ok,
        macd_cross_up
    ])

    final_signal = match_score >= 4  # You can tweak this to >=3 if needed
    

    #logic_debug_note = 'all matched' if final_signal else 'filters failed'
    logic_debug_note = f'{match_score}/6 filters matched'
    

    if is_hammer:
        pattern = 'hammer'
    elif is_doji:
        pattern = 'doji'
    elif is_engulfing_bull:
        pattern = 'engulfing_bull'
    else:
        pattern = 'none'

    return {
        'timestamp': current['timestamp'],
        'symbol': current['symbol'],
        'recent_high_break': breakout_up,
        'range_breakout': range_breakout,
        'strong_candle': candle_strength,
        'volume_spike': volume_spike,
        'rsi_bounce': rsi_ok,
        'macd_cross_up': macd_cross_up,
        'match_score': match_score,
        'final_signal': final_signal,
        'logic_debug_note': logic_debug_note,
        'is_hammer': is_hammer,
        'is_doji': is_doji,
        'is_engulfing_bull': is_engulfing_bull,
        'detected_pattern': pattern
    }
