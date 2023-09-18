""" Script for testing lib """

from lib import read_data
import polars as pl


def test_read_data():
    df = read_data("currency_prices_long.csv")
    assert type(df) == pl.DataFrame
