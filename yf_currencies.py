import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def date_range(end_date=None, start_date=None, time_period=30):
    """
    Return a dictionary with start and end dates.
    If end_date not specified, today's date will be returned
    If start_date not specified, 1 month back will be returned
    Enter dates as yyyymmdd
    """
    if time_period > 3600:
        raise ValueError("Choose a shorter time frame.")
    if end_date is None:
        dates = {"end_date": pd.to_datetime(datetime.date.today())}
        pass
    else:
        dates = {"end_date": pd.to_datetime(end_date, dayfirst=True)}
        pass
    if start_date is None:
        dates["start_date"] = dates["end_date"] - datetime.timedelta(days=30)
        pass
    else:
        dates["start_date"] = pd.to_datetime(start_date, dayfirst=True)
        if (pd.to_datetime(datetime.date.today()) - dates["start_date"]).days > 3600:
            raise ValueError("Choose a more recent date.")
        pass
    return dates


def create_ticker(ccy):
    ticker = ccy.upper() + "=X"
    return ticker


def get_prices(ccy, date_range_dictionary):
    """ohlc: str | Open, High, Low or Close"""
    start_date = date_range_dictionary["start_date"]
    end_date = date_range_dictionary["end_date"]
    prices = yf.download(create_ticker(ccy.lower()), start_date, end_date)
    return prices


def create_currencies_dict(ccy_list, date_range_dictionary):
    if type(ccy_list) == str:
        ccy_list = [ccy_list]
    ccy_dict = {}
    for ccy in ccy_list:
        ccy_dict[ccy] = {"Open": None, "High": None, "Low": None, "Close": None}
        ccy_dict[ccy]["Open"] = get_prices(ccy, date_range_dictionary)["Open"]
        ccy_dict[ccy]["High"] = get_prices(ccy, date_range_dictionary)["High"]
        ccy_dict[ccy]["Low"] = get_prices(ccy, date_range_dictionary)["Low"]
        ccy_dict[ccy]["Close"] = get_prices(ccy, date_range_dictionary)["Close"]
        pass
    return ccy_dict


# run some statistics ... max, min and current + % up or down in the period for each ccy?
def create_df(ccy, ccy_dict):
    df = pd.DataFrame(ccy_dict[ccy])
    df.name = ccy
    return df


def get_last(ccy_df):
    last = ccy_df.Close[-1]
    return last


def print_range(ccy_df):
    low = ccy_df.Low.min()
    high = ccy_df.High.max()
    close = ccy_df.Close[-1]
    ccy_open = ccy_df.Open[0]
    average = ccy_df.Close.mean()
    std_dev = np.std(ccy_df.Close)
    print(ccy_df.name + "'s current value is {}.".format(round(close, 2)))
    print(
        "Between {} and {}:".format(
            ccy_df.index.min().strftime("%d/%b/%y"),
            ccy_df.index.max().strftime("%d/%b/%y"),
        )
    )
    print(
        "- "
        + ccy_df.name
        + " {} {}%".format(
            "dropped" if close < ccy_open else "rose",
            round((close / ccy_open - 1) * 100, 2),
        )
    )
    print(
        "- "
        + ccy_df.name
        + " reached a low of {} on {}".format(
            round(low, 2), ccy_df.index[ccy_df.Low == low][0].strftime("%d %b %y")
        )
    )
    print(
        "- "
        + ccy_df.name
        + " reached a high of {} on {}".format(
            round(high, 2), ccy_df.index[ccy_df.High == high][0].strftime("%d %b %y")
        )
    )
    print(
        "- "
        + ccy_df.name
        + " had an average and standard deviation of {} and {} over the period.".format(
            round(average, 2), round(std_dev, 2)
        )
    )
    pass


def print_ccy_levels(ccy_list, time_period=30):
    currencies = create_currencies_dict(ccy_list, date_range(time_period=time_period))
    for ccy in ccy_list:
        df = create_df(ccy, currencies)
        print_range(df)
        pass
    pass


def generate_summary_statistics(
    ccy_list=None, ccy_dict=None, column="Close", time_period=30
):
    if type(ccy_list) == str:
        ccy_dict = create_currencies_dict(ccy_list, date_range(time_period=time_period))
        pass
    if type(ccy_list) == list:
        ccy_dict = create_currencies_dict(ccy_list, date_range(time_period=time_period))
    df = pd.DataFrame(columns=ccy_dict.keys())
    for i in df.columns:
        df[i] = ccy_dict[i][column]
        pass
    return df.describe()


def plot_returns(ccy_list=None, ccy_dict=None, column="Close", time_period=30):
    """It generates a plot of the currencies given.
    1 - If ccy_list is given, data will be downloaded for every currency in the list.
    2 - If ccy_dict is given, plots will be generated for every currency in dict.keys
    """
    if type(ccy_list) == str:
        ccy_dict = create_currencies_dict(ccy_list, date_range(time_period=time_period))
        pass
    if type(ccy_list) == list:
        ccy_dict = create_currencies_dict(ccy_list, date_range(time_period=time_period))
    df = pd.DataFrame(columns=ccy_dict.keys())
    for i in df.columns:
        df[i] = ccy_dict[i][column]
        pass
    fig, ax = plt.subplots()
    for ccy in df.columns:
        ax.plot(df[ccy].pct_change())
        pass
    plt.legend(df.columns)
    ax.set_ylabel("% change")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)
    fig.suptitle("Currency returns")


# potentially add bollinger bands?

if __name__ == "__main__":
    ccys = ["usdmxn", "eurusd", "nzdusd"]
    print(generate_summary_statistics(ccys))
    print_ccy_levels(ccys)
    plot_returns(ccys)
