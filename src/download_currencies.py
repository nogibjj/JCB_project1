import yfinance as yf
import pandas as pd


def yf_ticker(ccy):
    ticker = ccy.upper() + "=X"
    return ticker


def create_tickers(ccy_list):
    tickers = [yf_ticker(ticker) for ticker in ccy_list]
    return tickers


def download_prices_long(tickers, start=None, end=None, period=None):
    if (start is None) & (end is None):
        data = yf.download(tickers, period=period, interval="60m")
        pass
    else:
        data = yf.download(tickers, start=start, end=end, interval="60m")
    if len(tickers) == 1:
        data.columns = [data.columns, pd.Series(tickers * len(data.columns))]
    data.reset_index(inplace=True)
    data = data.melt(
        id_vars="Datetime", var_name=["Price type", "Instrument"], value_name="Price"
    )
    data.to_csv("currency_prices_long.csv")
    pass
