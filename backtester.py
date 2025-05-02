import pandas as pd

def run_backtest(df, signal_function, score_threshold=4):
    trades = []
    window = 21  # Required because your indicators need rolling(20)

    for i in range(window, len(df) - 3):  # Leave room for 3-candle exit
        window_df = df.iloc[i - window:i + 1].copy()
        signal = signal_function(window_df)

        if signal['match_score'] >= score_threshold:
            entry = df.iloc[i]['close']
            atr = df.iloc[i]['atr']
            tp = entry + 1.5 * atr
            sl = entry - 1.0 * atr
            exit_price = None
            exit_reason = "timeout"
            duration = 3

            for j in range(1, 4):  # Check next 3 candles
                high = df.iloc[i + j]['high']
                low = df.iloc[i + j]['low']

                if high >= tp:
                    exit_price = tp
                    exit_reason = "tp_hit"
                    duration = j
                    break
                elif low <= sl:
                    exit_price = sl
                    exit_reason = "sl_hit"
                    duration = j
                    break

            if exit_price is None:
                exit_price = df.iloc[i + 3]['close']

            pnl = ((exit_price - entry) / entry) * 100

            filter_keys = [
                'recent_high_break', 'range_breakout',
                'strong_candle', 'volume_spike',
                'rsi_bounce', 'macd_cross_up'
            ]
            filters = [k for k in filter_keys if signal.get(k)]
            filters_triggered = ",".join(filters) if filters else "none"


            trades.append({
                'timestamp': df.iloc[i]['timestamp'],
                'symbol': df.iloc[i]['symbol'],
                'entry_price': entry,
                'exit_price': exit_price,
                'pnl_pct': round(pnl, 4),
                'match_score': signal['match_score'],
                'exit_reason': exit_reason,
                'duration_candles': duration,
                'atr_on_entry': atr,
                'filters_triggered': filters_triggered,
                'final_signal': signal['final_signal']
            })

    return pd.DataFrame(trades)
