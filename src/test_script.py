""" Test script for yf_currencies """
from yf_currencies import *


def test_yf_currencies():
    assert "usdmxn" in currencies
    assert prices.shape[1] == 5
    assert "High" in average_prices["Price type"]
