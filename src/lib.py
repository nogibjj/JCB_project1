""" A python script that does data analysis using polars dataframes """

import polars as pl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from download_currencies import download_prices_long, create_tickers


def read_data(path):
    """
    Read the data from the path specified.
    """
    try:
        df = pl.read_csv(path, try_parse_dates=True)
        df = df.drop_nulls()
    except FileNotFoundError:
        tickers = create_tickers(["usdmxn, eurusd, nzdusd"])
        download_prices_long(tickers)
        df = pl.read_csv(path, try_parse_dates=True)
        df = df.drop_nulls()
    return df


def plot_returns(ccy_df, column="Close"):
    """takes data from a polars dataframe and plots the returns"""
    fig, ax = plt.subplots()
    tickers = ccy_df["Instrument"].unique()
    for ccy in tickers:
        df = ccy_df.filter(
            (pl.col("Instrument") == ccy) & (pl.col("Price type") == column)
        )
        ax.plot(df["Datetime"], df["Price"].pct_change().cumsum())
        pass
    plt.legend(tickers)
    ax.set_ylabel("% change")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d%b"))
    plt.locator_params(axis="x", nbins=5)
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    fig.suptitle("Currency returns")
    pass


def save_plot(path):
    plt.savefig(path)
    pass


def print_range(ccy_df):
    tickers = ccy_df["Instrument"].unique()
    print(
        "Let's analyze the following currencies {}:\n".format(
            [ccy[:6] for ccy in tickers]
        )
    )
    for ccy in tickers:
        ccy_reduced = ccy[:6]
        low = (
            ccy_df.filter(
                (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Low")
            )
            .min()["Price"]
            .item()
        )
        high = (
            ccy_df.filter(
                (pl.col("Instrument") == ccy) & (pl.col("Price type") == "High")
            )
            .max()["Price"]
            .item()
        )
        close = ccy_df.filter(
            (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Close")
        )[-1]["Price"].item()
        ccy_open = ccy_df.filter(
            (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Open")
        )[0]["Price"].item()
        average = ccy_df.filter(
            (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Close")
        )["Price"].mean()
        std_dev = ccy_df.filter(
            (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Close")
        )["Price"].std()
        print(ccy_reduced + "'s current value is {}.".format(round(close, 2)))
        print(
            "Between {} and {}:".format(
                ccy_df["Datetime"].min().strftime("%d/%b/%y"),
                ccy_df["Datetime"].max().strftime("%d/%b/%y"),
            )
        )
        print(
            "- "
            + ccy_reduced
            + " {} {}%".format(
                "dropped" if close < ccy_open else "rose",
                round((close / ccy_open - 1) * 100, 2),
            )
        )
        print(
            "- "
            + ccy_reduced
            + " reached a low of {} on {}".format(
                round(low, 2),
                ccy_df.filter(pl.col("Price") == low)[0]["Datetime"]
                .item()
                .strftime("%d %b %y"),
            )
        )
        print(
            "- "
            + ccy_reduced
            + " reached a high of {} on {}".format(
                round(high, 2),
                ccy_df.filter(pl.col("Price") == high)[0]["Datetime"]
                .item()
                .strftime("%d %b %y"),
            )
        )
        print(
            "- "
            + ccy_reduced
            + " had an average and standard deviation of {} and {} over the period.".format(
                round(average, 2), round(std_dev, 2)
            )
        )
        print(
            ccy_df.filter(
                (pl.col("Instrument") == ccy) & (pl.col("Price type") == "Close")
            )["Price"].describe()
        )


if __name__ == "__main__":
    currencies = read_data("currency_prices_long.csv")
    print_range(currencies)
    plot_returns(currencies)
    plt.savefig("currency_returns.png")
