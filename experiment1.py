import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random
from util import get_data, plot_data
import ManualStrategy as ms
import StrategyLearner as sl
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
def compute(val):
    daily_return = val.copy()
    daily_return[1:] = (daily_return[1:] / daily_return[:-1].values) - 1
    daily_return = daily_return[1:]
    cr = (val[-1] / val[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = adr / sddr
    print (cr, adr, sddr, sr)
def main():
    sd = dt.date(2008,1,1)
    ed = dt.date(2009,12,31)
    sv = 100000
    symbol = ['JPM']
    dates = dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(symbol, dates)


    str_learn = sl.StrategyLearner(verbose= False, impact=0.0)
    str_learn.addEvidence('JPM', sd, ed, sv)
    df_str = str_learn.testPolicy('JPM', sd, ed, sv)

    df_trades,df_benchmark = ms.testPolicy('JPM', sd, ed, sv)

    portfolio_stand = compute_portvals(df_str,sv,0.0,0.0)
    compute(portfolio_stand)

    port_ms = compute_portvals(df_trades,sv,0.0,0.0)
    compute(port_ms)
    port_bench = compute_portvals(df_benchmark,sv,0.0,0.0)
    compute(port_bench)

    chart = pd.concat([portfolio_stand, port_ms,port_bench], axis=1)
    chart.columns = ['Portfolio Strategy Learner','Portfolio Manual Strategy', 'Portfolio Benchmark']
    chart.plot(grid=True, title='Comparison of Portfolio Values', use_index=True, color=['Red', 'Blue','Black'])
    plt.savefig("Comp")
    plt.show()



if __name__=="__main__":
    main()
