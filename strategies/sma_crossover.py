import sys
import os
import pandas as pd
from ta.momentum import RSIIndicator
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.MyFile import fetch_and_clean_ticker_data


def sma_rsi_crossover(data, short_window=20, long_window=50, rsi_window=14):

    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    close_series = pd.Series(data['Close'].values.ravel())
    rsi_indicator = RSIIndicator(close=close_series,window=rsi_window)
    data['RSI'] = rsi_indicator.rsi()
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
        file_path = os.path.join("data",f"{ticker}.csv")
        result.to_csv(file_path, index=False)
        



