"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch

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
"""

import numpy as np
import random as rn

class RTLearner(object):

    def __init__(self,leaf_size=1,verbose=False):
        self.T= np.array([[]])
        self.leaf_size = leaf_size
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'pjhaveri6'  # replace tb34 with your Georgia Tech username

    def build_t(self,data):

        if data.shape[0]<= self.leaf_size:

            return np.array([[-1, data[0][-1],-1, -1]])
        f=0
        f = rn.randint(0, data.shape[1]-2)
        #for i in range(0,data.shape[1]-1):

           # c=np.corrcoef(data[:,i],data[:,-1])
           # if(i==0):
            #    d=np.absolute(c[0][1])
            #if np.absolute(c[0][1])>d:
              #  d=np.absolute(c[0][1])
              #  f=i
        SplitVal=np.median(data[:,f])
        a=np.argmax(data[:,f])
        val = data[a][f]

        if(SplitVal==val):
            return np.array([[-1,data[a][-1],-1,-1]])

        lefttree=self.build_t(data[data[:,f]<=SplitVal])
        righttree = self.build_t(data[data[:, f] > SplitVal])
        root = np.array([[f, SplitVal, 1, lefttree.shape[0] + 1]])
        return np.concatenate((np.concatenate((root,lefttree),axis=0),righttree),axis=0)

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:, 0:dataX.shape[1]] = dataX
        newdataX[:,-1]=dataY
        self.T = self.build_t(newdataX)


        # build and save the model
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)

    def size_leaf_node(self):
        return self.T.shape[0]


    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """



        a=np.empty(shape=points.shape[0])
        for i in range(0,len(points)):
            g=0
            fact=int(self.T[g][0])
            while fact!=-1:

                if(points[i][fact]<=self.T[g][1]):

                    g+=int(self.T[g][2])

                else:
                    g+=int(self.T[g][3])
                fact = int(self.T[g][0])


            a[i] = self.T[g][1]

        return a


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
