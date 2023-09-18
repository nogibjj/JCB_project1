""" This is a script that performs some descriptive analysis on diverse currencies """

# Let's import the descriptive statistics we've created in lib.py and a few methods from our download_currencies module:

from lib import read_data, print_range, plot_returns
from download_currencies import download_prices_long, create_tickers
import polars as pl

# use download_prices_long to download hourly data on usdmxn, eurusd, nzdusd for the last 6 months
currencies = ["usdmxn", "eurusd", "nzdusd"]
tickers = create_tickers(currencies)
download_prices_long(tickers)

# import data as polars dataframe
prices = read_data("currency_prices_long.csv")
print(prices.head())
print(prices["Price type"].unique())

# Let's look at a quick example of each currency's average price by Price type for the last 6 months:
average_prices = (
    prices.group_by(["Instrument", "Price type"])
    .mean()
    .filter(pl.col("Price type") != "Volume")[["Instrument", "Price type", "Price"]]
    .sort(by="Instrument")
)
print(average_prices)

# a more specific description of price ranges using Price type == Close
print_range(prices)

# plot each currency's cumulative returns over the period
plot_returns(prices, "Close")
