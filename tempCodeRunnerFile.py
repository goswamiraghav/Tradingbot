backtest_results = run_backtest(df, generate_signal_row, score_threshold=4)
print(backtest_results.head())