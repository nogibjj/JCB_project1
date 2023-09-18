""" Test script for yf_currencies """
import yf_currencies as yfc


def test_yf_currencies():
    assert "usdmxn" in yfc.currencies
    assert yfc.prices.shape[1] == 5
    assert "High" in yfc.average_prices["Price type"]
