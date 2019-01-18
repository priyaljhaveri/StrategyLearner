"""  		   	  			    		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut
from indicators import get_sma,get_bb,get_momentum
import BagLearner as bl
import RTLearner as rt
import random
import numpy as np
  		   	  			    		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact
        self.N = 10
        self.learner = bl.BagLearner(rt.RTLearner,kwargs={"leaf_size":5},bags=20,boost=False,verbose=False)
  		   	  			    		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # add your code to do learning here  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # example usage of the old backward compatible util function  		   	  			    		  		  		    	 		 		   		 		  
        syms=[symbol]  		   	  			    		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print prices  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # example use with new colname  		   	  			    		  		  		    	 		 		   		 		  
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
        volume = volume_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later  		   	  			    		  		  		    	 		 		   		 		  
        if self.verbose: print volume

        bb_val,upper,lower,rm,rs = get_bb(prices)
        sma = get_sma(prices)
        mom = get_momentum(prices)
        x_train = np.zeros(shape=(len(prices),7))

        for i in range(20,len(prices)-self.N):
            x_train[i][0]=bb_val[i]
            x_train[i][1]=upper[i]
            x_train[i][2]=lower[i]
            x_train[i][3]=rm[i]
            x_train[i][4]=rs[i]
            x_train[i][5]=sma[i]
            x_train[i][6]=mom[i]

        x_train = pd.DataFrame(x_train)
        x_train = x_train[:-self.N]
        x_train.fillna(0, inplace=True)
        x_train = x_train.values
        y = []

        for i in range(0,len(prices)-self.N):
            if (prices.ix[i+self.N,symbol]/prices.ix[i,symbol])> 1.0009+self.impact:
                y.append(1)
            elif (prices.ix[i+self.N,symbol]/prices.ix[i,symbol]) < 0.9991-self.impact:
                y.append(-1)
            else:
                y.append(0)

        y_train = np.array(y)

        #print y_train
        self.learner.addEvidence(x_train,y_train)




    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # here we build a fake set of trades  		   	  			    		  		  		    	 		 		   		 		  
        # your code should return the same sort of data  		   	  			    		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
        prices = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        bb_val, upper, lower, rm, rs = get_bb(prices)
        sma = get_sma(prices)
        mom = get_momentum(prices)
        x_test = np.zeros(shape=(len(prices), 7))

        for i in range(20, len(prices) - self.N):
            x_test[i][0] = bb_val[i]
            x_test[i][1] = upper[i]
            x_test[i][2] = lower[i]
            x_test[i][3] = rm[i]
            x_test[i][4] = rs[i]
            x_test[i][5] = sma[i]
            x_test[i][6] = mom[i]

        x_test = pd.DataFrame(x_test)
        x_test = x_test[:-self.N]
        x_test = x_test.values
        y_test = self.learner.query(x_test)

        trades = pd.DataFrame(0, columns=prices.columns, index=prices.index)

        flag = 0
        for i in range(0, len(prices) - self.N):
            if y_test[i] == 1:
                if flag == 0:
                    flag = 1000
                    trades[symbol].iloc[i] = 1000
                elif flag == -1000:
                    flag = 1000
                    trades.iloc[i, 0] = 2000
            if y_test[i] == -1:
                if flag == 0:
                    flag = -1000
                    trades[symbol].iloc[i] = -1000
                elif flag == 1000:
                    flag = -1000
                    trades[symbol].iloc[i] = -2000

        # trades.values[:,:] = 0 # set them all to nothing
        # trades.values[0,:] = 1000 # add a BUY at the start
        # trades.values[40,:] = -1000 # add a SELL
        # trades.values[41,:] = 1000 # add a BUY
        # trades.values[60,:] = -2000 # go short from long
        # trades.values[61,:] = 2000 # go long from short
        # trades.values[-1,:] = -1000 #exit on the last day
        # if self.verbose: print type(trades) # it better be a DataFrame!
        # if self.verbose: print trades
        # if self.verbose: print prices_all
        return trades
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "One does not simply think up a strategy"
    learner = StrategyLearner()
    learner.addEvidence(symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000)
    learner.testPolicy(symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000)
