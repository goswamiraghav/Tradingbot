# signal_generator.py
"""
def generate_signal_row(df):
    current = df.iloc[-1]  # Current candle
    prev = df.iloc[-2]     # Previous candle (for engulfing check)

    # --- Rolling logic windows ---
    recent_high = df['close'].rolling(window=20).max().shift(1)
    breakout_up = current['close'] > recent_high.iloc[-1]
    # Market: price just broke recent resistance

    range_size = df['high'].rolling(20).max() - df['low'].rolling(20).min()
    range_breakout = (current['close'] > df['high'].rolling(20).max().shift(1).iloc[-1]) and (range_size.iloc[-1] > current['atr'])
    # Market: range was tight, and price just broke above it

    body = abs(current['close'] - current['open'])
    candle_strength = body > current['atr'] * 0.7
    # Market: large candle body = strong conviction

    avg_vol = df['volume'].rolling(20).mean()
    volume_spike = current['volume'] > avg_vol.iloc[-1] * 1.2
    # Market: sudden spike in volume confirms move

    rsi_ok = 45 <= current['rsi'] <= 52
    # Market: RSI bounce zone in bullish trends

    macd_cross_up = current['macd'] > current['macd_signal']
    # Market: MACD line crossing signal = momentum shift

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

    # --- New: Group filters into a dictionary for logic and logging ---
    filters = {
        'recent_high_break': breakout_up,
        'range_breakout': range_breakout,
        'strong_candle': candle_strength,
        'volume_spike': volume_spike,
        'rsi_bounce': rsi_ok,
        'macd_cross_up': macd_cross_up
    }

    # --- New: Collect names of matched filters ---
    filters_triggered = [key for key, value in filters.items() if value]

    # --- Updated: Calculate match_score as count of matched filters ---
    match_score = len(filters_triggered)

    # --- Final Signal Decision ---
    final_signal = match_score >= 4
    logic_debug_note = f'{match_score}/6 filters matched'

    # --- Candlestick pattern detection output ---
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
        'detected_pattern': pattern,
        'filters_triggered_list': filters_triggered  # New: This helps later for debugging and analysis
    }
"""
def generate_signal_row(df):
    active_signals = []
    current = df.iloc[-1]
    prev = df.iloc[-2]

    # Rolling calculations
    recent_high = df['close'].rolling(window=20).max().shift(1)
    breakout_up = current['close'] > recent_high.iloc[-1]

    range_size = df['high'].rolling(20).max() - df['low'].rolling(20).min()
    range_breakout = (
        current['close'] > df['high'].rolling(20).max().shift(1).iloc[-1]
        and range_size.iloc[-1] > current['atr']
    )

    body = abs(current['close'] - current['open'])
    candle_strength = body > current['atr'] * 0.7

    avg_vol = df['volume'].rolling(20).mean()
    volume_spike = current['volume'] > avg_vol.iloc[-1] * 1.2

    rsi_ok = 45 <= current['rsi'] <= 52
    macd_cross_up = current['macd'] > current['macd_signal']

    upper_wick = current['high'] - max(current['open'], current['close'])
    lower_wick = min(current['open'], current['close']) - current['low']
    is_hammer = (lower_wick > 2 * body) and (upper_wick < 0.2 * body)
    is_doji = body < (current['high'] - current['low']) * 0.1
    is_engulfing_bull = (
        prev['close'] < prev['open'] and
        current['close'] > current['open'] and
        current['close'] > prev['open'] and
        current['open'] < prev['close']
    )

    # ✅ Bollinger Band logic
    bb_upper_break = current['close'] > current['bb_upper']
    bb_lower_break = current['close'] < current['bb_lower']
    bb_bandwidth = current['bb_upper'] - current['bb_lower']
    bb_squeeze = bb_bandwidth < df['bb_middle'].rolling(20).std().iloc[-1]  # Approx squeeze detection

    filters = {
        'recent_high_break': breakout_up,
        'range_breakout': range_breakout,
        'strong_candle': candle_strength,
        'volume_spike': volume_spike,
        'rsi_bounce': rsi_ok,
        'macd_cross_up': macd_cross_up,
        'bb_upper_break': bb_upper_break,
        'bb_lower_break': bb_lower_break,
        'bb_squeeze_breakout': bb_squeeze
    }

    filters_triggered = [key for key, value in filters.items() if value]
    match_score = len(filters_triggered)
    final_signal = match_score >= 4
    logic_debug_note = f"{match_score}/9 filters matched"
    signal_combo_name = '+'.join(sorted(filters_triggered)) if filters_triggered else 'none'

    # Candlestick pattern
    if is_hammer:
        pattern = 'hammer'
    elif is_doji:
        pattern = 'doji'
    elif is_engulfing_bull:
        pattern = 'engulfing_bull'
    else:
        pattern = 'none'
    #print("DEBUG COMBO:", signal_combo_name)

    return {
        'timestamp': current['timestamp'],
        'symbol': current['symbol'],
        'recent_high_break': breakout_up,
        'range_breakout': range_breakout,
        'strong_candle': candle_strength,
        'volume_spike': volume_spike,
        'rsi_bounce': rsi_ok,
        'macd_cross_up': macd_cross_up,
        'bb_upper_break': bb_upper_break,
        'bb_lower_break': bb_lower_break,
        'bb_squeeze_breakout': bb_squeeze,
        'match_score': match_score,
        'final_signal': final_signal,
        'logic_debug_note': logic_debug_note,
        'is_hammer': is_hammer,
        'is_doji': is_doji,
        'is_engulfing_bull': is_engulfing_bull,
        'detected_pattern': pattern,
        'filters_triggered_list': filters_triggered,
        'signal_combo_name': signal_combo_name
    }
