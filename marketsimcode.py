"""MC2-P1: Market simulator.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Priyal Jhaveri
GT User ID: pjhaveri6
GT ID: 903391526
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data


def author():
    return "pjhaveri6"


def compute_portvals(orders_df, start_val=100000, commission=0, impact=0):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months

    start_date = orders_df.index[0]
    end_date = dt.datetime(2009,12,31)
    symbols=["JPM"]
    portvals = get_data(symbols, pd.date_range(start_date, end_date))
    portvals = portvals.drop('SPY', 1)
    portvals = portvals.fillna(method='ffill')
    portvals = portvals.fillna(method='bfill')

    portvals.insert(portvals.shape[1],'Cash',1)

    df_trades = portvals.copy()

    for columns in df_trades.columns:
        df_trades[columns] = 0.0
    #print orders_df
    for j,k in orders_df.iterrows():
        if k['JPM']>0:
            df_trades.at[j,'JPM'] += k['JPM']
            price = portvals.at[j,'JPM']
            df_trades.at[j, 'Cash'] += ((price * k['JPM'] * -1) * (1 + impact)) - commission

        else:
            df_trades.at[j, 'JPM'] += 1 * k['JPM']
            price = portvals.at[j, 'JPM']
            df_trades.at[j, 'Cash'] += ((price * k['JPM'] * -1) * (1 - impact)) - commission
    df_holdings = df_trades.copy()
    #print df_trades
    for columns in df_holdings.columns:
        df_holdings[columns]=0.0

    df_holdings.at[start_date, 'Cash'] = start_val
    start_date = df_trades.index[0]
    temp = df_trades.loc[start_date]

    for index, rows in df_trades.iterrows():
        if index == start_date:
            df_holdings.loc[index]+=temp
        else:
            df_holdings.loc[index] += (temp + df_trades.loc[index])
        temp = df_holdings.loc[index]
    #print df_holdings
    values = df_holdings.copy()
    values = values * portvals

    final_val = values.sum(axis=1)
    return final_val


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[
            portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print


if __name__ == "__main__":
    test_code()