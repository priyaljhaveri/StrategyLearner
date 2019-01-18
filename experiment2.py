import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import random
from util import get_data, plot_data
import ManualStrategy as ms
import StrategyLearner as strl
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

    str_learn = strl.StrategyLearner(verbose= False, impact=0.0)
    str_learn.addEvidence('JPM', sd, ed, sv)
    df_str1 = str_learn.testPolicy('JPM', sd, ed, sv)

    str_learn = strl.StrategyLearner(verbose=False, impact=0.10)
    str_learn.addEvidence('JPM', sd, ed, sv)
    df_str2 = str_learn.testPolicy('JPM', sd, ed, sv)

    str_learn = strl.StrategyLearner(verbose=False, impact=0.15)
    str_learn.addEvidence('JPM', sd, ed, sv)
    df_str3 = str_learn.testPolicy('JPM', sd, ed, sv)


    portfolio_stand1 = compute_portvals(df_str1,sv,0.0,0.0)
    compute(portfolio_stand1)

    portfolio_stand2 = compute_portvals(df_str2,sv,0.0,0.0)
    compute(portfolio_stand2)
    portfolio_stand3 = compute_portvals(df_str3,sv,0.0,0.0)
    compute(portfolio_stand3)



    chart = pd.concat([portfolio_stand1, portfolio_stand2,portfolio_stand3], axis=1)
    chart.columns = ['Impact = 0','Impact = 0.1', 'Impact = 0.15']
    chart.plot(grid=True, title='Comparison of Portfolio Values', use_index=True, color=['Red', 'Blue','Black'])
    plt.savefig("Impact")
    plt.show()



if __name__=="__main__":
    main()