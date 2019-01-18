import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt

def get_bb(prices):
    syms = prices.columns.tolist()
    symbol = syms[0]
    price = prices[symbol]
    normed = price / price[0]
    # Bollinger Bands
    rm = normed.rolling(20).mean()
    rstd = normed.rolling(20).std()
    upper = rm + (rstd * 2)
    lower = rm - (rstd * 2)
    bbval  = (normed - lower)/(upper - lower)

    # plt.plot(rm)
    # plt.plot(upper)
    # plt.plot(lower)
    # plt.ylabel('Normalized Price')
    # plt.xlabel('Date')
    # plt.xticks([100, 200, 300, 400, 500, 600], ['2008-04', '2008-07', '2008-10', '2009-01', '2009-10'])
    # plt.legend(['Upper BB', 'Lower BB', 'Rolling Mean'])
    # plt.show()
    # plt.clf()

    return bbval,upper,lower,rm,rstd

def get_momentum(prices):
    syms = prices.columns.tolist()
    symbol = syms[0]
    price = prices[symbol]
    normed = price / price[0]
    # Momentum
    rm = normed.rolling(20).mean()
    rstd = normed.rolling(20).std()
    mom = (normed / normed.shift(20)) - 1
    # plt.plot(normed)
    # plt.plot(mom)
    # plt.ylabel('Normalized Price')
    # plt.xlabel('Date')
    # plt.xticks([100, 200, 300, 400, 500, 600], ['2008-04', '2008-07', '2008-10', '2009-01', '2009-10'])
    # plt.legend(['Price', 'Momentum'])
    # plt.show()
    # plt.clf()

    return mom

def get_sma(prices):
    syms = prices.columns.tolist()
    symbol = syms[0]
    price = prices[symbol]
    normed = price / price[0]
    rm = normed.rolling(20).mean()
    rstd = normed.rolling(20).std()
    sma = normed.divide(rm, axis='index')
    # plt.plot(normed)
    # plt.plot(rm)
    # plt.ylabel('Normalized Price')
    # plt.xlabel('Date')
    # plt.xticks([100, 200, 300, 400, 500, 600], ['2008-04', '2008-07', '2008-10', '2009-01', '2009-10'])
    # plt.legend(['Price', 'Rolling Mean'])
    # plt.show()
    # plt.clf()
    return sma

def get_cci(prices):
    price = prices['JPM']
    normed = price / price[0]
    rm = normed.rolling(12).mean()
    rstd = normed.rolling(12).std()
    #Commodity channel index
    cci = (normed - rm) / (2* rstd)
    plt.ylabel('Normalized Price')
    plt.xlabel('Date')
    plt.xticks([100, 200, 300, 400, 500, 600], ['2008-04', '2008-07', '2008-10', '2009-01', '2009-10'])

    plt.plot(normed)
    plt.plot(cci)
    plt.legend(['Price', 'CCI'])
    plt.show()
    return cci

def technical_analysis(prices):

    print prices
    bbvsal = get_bb(prices)
    momval = get_momentum(prices)
    smaval = get_sma(prices)
    cci_val = get_cci(prices)

def test_code():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = 'JPM'
    dates = pd.date_range(sd, ed)
    prices = ut.get_data([symbol], dates)
    technical_analysis(prices)


if __name__ == "__main__":
    test_code()

