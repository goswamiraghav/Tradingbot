# backtester.py
"""import pandas as pd

def run_backtest(df, signal_function, score_threshold=4):
    trades = []
    window = 21  # Required because your indicators need rolling(20)

    for i in range(window, len(df) - 3):  # Leave room for 3-candle exit
        window_df = df.iloc[i - window:i + 1].copy()
        signal = signal_function(window_df)

        if signal['match_score'] >= score_threshold:
            entry = df.iloc[i]['close']
            atr = df.iloc[i]['atr']
            tp = entry + 2.0 * atr  # Updated TP multiplier
            sl = entry - 1.15 * atr  # Updated SL multiplier
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
                'filters_triggered_list': signal.get('filters_triggered_list', []),  # Store as ARRAY<STRING>
                'final_signal': signal['final_signal']
            })

    return pd.DataFrame(trades)

again we are commenting this and new code belowwww;;;;;;;;;;;;;;;ooooooö0000000===============================================---------==========-------=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    

import pandas as pd

def run_backtest_v2(df, signal_function, score_threshold=4, tp_k=1.95, sl_k=1.5, max_duration=3):
    trades = []
    window = 21  # Indicator buffer

    # Only trade these signal combos (from your analysis)
    ALLOWED_COMBOS = {
        "volume_spike+recent_high_break+strong_candle",
        "macd_cross_up+range_breakout+volume_spike+strong_candle"
    }

    for i in range(window, len(df) - max_duration):
        window_df = df.iloc[i - window:i + 1].copy()
        signal = signal_function(window_df)

        # Only trade if combo is allowed and signal strength is enough
        if signal['match_score'] >= score_threshold:
            entry_price = df.iloc[i]['close']
            atr = df.iloc[i]['atr']
            symbol = df.iloc[i]['symbol']
            tp_price = entry_price + tp_k * atr
            sl_price = entry_price - sl_k * atr
            trailing_sl = sl_price
            exit_price = None
            exit_reason = "timeout"
            mfe = float('-inf')
            mae = float('inf')

            for j in range(1, max_duration + 1):
                row = df.iloc[i + j]
                high = row['high']
                low = row['low']
                close = row['close']
                current_atr = row['atr']

                # Update trailing SL
                trailing_sl = max(trailing_sl, close - sl_k * current_atr)

                # MFE / MAE
                mfe = max(mfe, (high - entry_price) / atr)
                mae = min(mae, (low - entry_price) / atr)

                if high >= tp_price:
                    exit_price = tp_price
                    exit_reason = "tp_hit"
                    duration = j
                    break
                elif low <= trailing_sl:
                    exit_price = trailing_sl
                    exit_reason = "sl_hit"
                    duration = j
                    break
            else:
                exit_price = df.iloc[i + max_duration]['close']
                duration = max_duration

            pnl = ((exit_price - entry_price) / entry_price) * 100
            was_profitable = pnl > 0
            trade_type = "Scalp" if duration <= 3 else "Swing" if duration <= 15 else "Position"

            trades.append({
                'timestamp': df.iloc[i]['timestamp'],
                'symbol': symbol,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'exit_reason': exit_reason,
                'duration_candles': duration,
                'pnl_pct': round(pnl, 4),
                'was_profitable': was_profitable,
                'trade_type': trade_type,
                'tp_price': tp_price,
                'sl_price': sl_price,
                'mfe_atr': round(mfe, 4),
                'mae_atr': round(mae, 4),
                'match_score': signal['match_score'],
                'rsi_bounce': signal.get('rsi_bounce', False),
                'macd_cross_up': signal.get('macd_cross_up', False),
                'recent_high_break': signal.get('recent_high_break', False),
                'range_breakout': signal.get('range_breakout', False),
                'strong_candle': signal.get('strong_candle', False),
                'volume_spike': signal.get('volume_spike', False),
                'signal_combo_name': signal.get('signal_combo_name', 'unknown'),
            })

    return pd.DataFrame(trades)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=-=-=-==-=-=-==-=-=-=-=-=-=-=-=-=-=-
"""
import pandas as pd

def run_backtest_v2(df, signal_function, score_threshold=2, tp_k_base=1.95, sl_k_base=1.5, max_duration=3, cooldown_after_loss=3):
    trades = []
    window = 21  # Buffer for rolling indicators
    last_exit_index = -cooldown_after_loss  # Initialize cooldown tracker

    #Only allow high-performing signal combinations
    ALLOWED_COMBOS = {
    "rsi_bounce+strong_candle"
    }



    for i in range(window, len(df) - max_duration):
        # Cooldown logic: Skip if we're within cooldown window after a loss
        if i <= last_exit_index + cooldown_after_loss:
            continue

        window_df = df.iloc[i - window:i + 1].copy()
        signal = signal_function(window_df)
        signal_combo = signal.get('signal_combo_name', 'unknown')

        # Only continue if combo is in the allowed list and signal is strong enough
        if signal['match_score'] >= score_threshold and signal_combo in ALLOWED_COMBOS:
            # Entry filters: trend confirmation and volatility filter
            rsi = df.iloc[i]['rsi']
            ema_9 = df.iloc[i]['ema_9']
            ema_20 = df.iloc[i]['ema_20']
            close = df.iloc[i]['close']
            open_ = df.iloc[i]['open']
            candle_body = abs(close - open_)
            atr = df.iloc[i]['atr']

            if ema_9 <= ema_20 or candle_body < 0.1 * atr or atr < 0.2:
                continue  # 🚫 Skip if trend is weak, candle is too small, or low volatility

            # Dynamically adjust TP/SL if signal is very strong
            if signal['match_score'] >= 5:
                tp_k, sl_k = 2.2, 1.2
            else:
                tp_k, sl_k = tp_k_base, sl_k_base

            entry_price = close
            tp_price = entry_price + tp_k * atr
            sl_price = entry_price - sl_k * atr
            trailing_sl = sl_price
            symbol = df.iloc[i]['symbol']
            exit_price = None
            exit_reason = "timeout"
            mfe = float('-inf')
            mae = float('inf')

            # Simulate trade over the next few candles
            for j in range(1, max_duration + 1):
                row = df.iloc[i + j]
                high = row['high']
                low = row['low']
                close = row['close']
                current_atr = row['atr']

                # Trailing SL adapts to volatility mid-trade
                trailing_sl = max(trailing_sl, close - sl_k * current_atr)

                # Track max favorable and adverse excursions
                mfe = max(mfe, (high - entry_price) / atr)
                mae = min(mae, (low - entry_price) / atr)

                if high >= tp_price:
                    exit_price = tp_price
                    exit_reason = "tp_hit"
                    duration = j
                    break
                elif low <= trailing_sl:
                    exit_price = trailing_sl
                    exit_reason = "sl_hit"
                    duration = j
                    break
            else:
                # If no exit condition hit, close at timeout
                exit_price = df.iloc[i + max_duration]['close']
                duration = max_duration

            pnl = ((exit_price - entry_price) / entry_price) * 100
            was_profitable = pnl > 0
            trade_type = "Scalp" if duration <= 3 else "Swing" if duration <= 15 else "Position"
            atr_on_exit = df.iloc[i + duration]['atr']

            # Add explanation of trade in debug note
            logic_debug_note = f"Score: {signal['match_score']} | TP: {tp_price:.2f} | SL: {sl_price:.2f} | RSI: {rsi:.2f} | Dur: {duration}"

            # Set cooldown trigger if trade was a loss
            if not was_profitable:
                last_exit_index = i + duration

            # Append trade details to result
            trades.append({
                'timestamp': df.iloc[i]['timestamp'],
                'symbol': symbol,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'exit_reason': exit_reason,
                'duration_candles': duration,
                'pnl_pct': round(pnl, 4),
                'was_profitable': was_profitable,
                'trade_type': trade_type,
                'tp_price': tp_price,
                'sl_price': sl_price,
                'atr_on_exit': atr_on_exit,
                'mfe_atr': round(mfe, 4),
                'mae_atr': round(mae, 4),
                'match_score': signal['match_score'],
                'rsi_bounce': signal.get('rsi_bounce', False),
                'macd_cross_up': signal.get('macd_cross_up', False),
                'recent_high_break': signal.get('recent_high_break', False),
                'range_breakout': signal.get('range_breakout', False),
                'strong_candle': signal.get('strong_candle', False),
                'volume_spike': signal.get('volume_spike', False),
                'signal_combo_name': signal_combo,
                'logic_debug_note': logic_debug_note
            })

    return pd.DataFrame(trades)
