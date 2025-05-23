import pandas as pd
import talib
from data.MyFile import fetch_and_clean_ticker_data


def sma_rsi_crossover(data, short_window=20, long_window=50, rsi_window=14):

    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    data['RSI'] = talib.RSI(data['Close'],timeperiod=rsi_window)
    data['Signal'] = 0
    data.loc[
    (data['SMA_Short'] > data['SMA_Long']) &
    (data['SMA_Short'].shift(1) <= data['SMA_Long'].shift(1)) &
    (data['RSI'] < 70),
    'Signal'
] = 1
    data.loc[
    (data['SMA_Short'] < data['SMA_Long']) &
    (data['SMA_Short'].shift(1) >= data['SMA_Long'].shift(1)) &
    (data['RSI'] > 30),
    'Signal'
] = -1
    return data

tickers = ["AAPL", "GOOG", "TSLA", "AMZN", "META"]

# Fetch cleaned data
cleaned_data = fetch_and_clean_ticker_data(tickers)

# Apply strategy to each
for ticker in tickers:
    if ticker in cleaned_data:
        df = cleaned_data[ticker]
        result = sma_rsi_crossover(df)
        print(f"\n{ticker} Signals:")
        print(result[['Date', 'Close', 'SMA_Short', 'SMA_Long', 'RSI', 'Signal']].tail())



