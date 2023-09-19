import yfinance as yf
import pandas as pd


def yf_ticker(ccy):
    ticker = ccy.upper() + "=X"
    return ticker


def create_tickers(ccy_list):
    tickers = [yf_ticker(ticker) for ticker in ccy_list]
    return tickers


def download_prices_long(tickers):
    data = yf.download(tickers, start="2023-03-20", end="2023-09-15", interval="60m")
    if len(tickers) == 1:
        data.columns = [data.columns, pd.Series(tickers * len(data.columns))]
    data.reset_index(inplace=True)
    data = data.melt(
        id_vars="Datetime", var_name=["Price type", "Instrument"], value_name="Price"
    )
    data.to_csv("currency_prices_long.csv")
    pass
