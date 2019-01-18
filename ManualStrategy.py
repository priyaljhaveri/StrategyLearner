import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
import matplotlib.pyplot as plt
from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import get_bb,get_sma,get_momentum

def testPolicy(symbol, sd, ed, sv):
    symbols = ['JPM']
    dates = pd.date_range(sd, ed)
    benchmark = get_data(symbols, dates, addSPY=False).dropna()
    prices = benchmark['JPM'].values
    trades = pd.DataFrame(data=np.zeros(len(prices)), index=benchmark.index, columns=['JPM'])
    print benchmark
    sma = get_sma(benchmark)
    mom = get_momentum(benchmark)
    bbval,upper,lower,rolling_m,rolling_s = get_bb(benchmark)
    holding =0
    benchmark = pd.DataFrame({'Date': dt.datetime(2008,1,2), 'JPM': [1000]})
    benchmark.set_index("Date", inplace=True)
    for i in range(12, len(prices)):
        if sma[i] < 0.95 and bbval[i]<0:
            trades['JPM'].iloc[i] = 1000 - holding
            holding = 1000
        elif sma[i] > 1.05 and bbval[i]>1:
            trades['JPM'].iloc[i] = - holding - 1000
            holding = -1000
    return trades,benchmark

if __name__ == "__main__":
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    symbol = 'JPM'
    dates = pd.date_range(sd, ed)
    prices = get_data([symbol], dates)
    prices = prices['JPM']
    start_value = 100000
    trades = testPolicy(symbol="JPM", sd=sd, ed=ed, sv=start_value)

    benchmark = pd.DataFrame({'Date': [sd], 'JPM': [1000]})
    benchmark.set_index("Date", inplace=True)
    port_vals = compute_portvals(trades)
    daily_return = port_vals.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (port_vals[-1] / port_vals[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr,adr,sr)
    daily_return = port_vals.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (port_vals[-1] / port_vals[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr, adr, sr)
    port_vals = port_vals+0.1
    port_vals = port_vals / port_vals[0]
    plt.plot(port_vals , color = 'black')
    benchmark = prices / prices[0]
    plt.plot(benchmark, color = 'blue')
    plt.ylabel('Normalized Price')
    plt.xlabel('Date')
    plt.xticks([100, 200, 300, 400, 500, 600], ['2008-04', '2008-07', '2008-10', '2009-01', '2009-10'])
    plt.legend(['Portfolio', 'Benchmark'])

    plt.show()

