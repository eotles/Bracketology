'''
Created on Jul 12, 2014

@author: eotles
'''
import sys
from season import Season
from team import Team
import numpy as np
import copy
import random

SCHEDULE_FILE = "/Users/eotles/Documents/workspace/Bracketology/data/schedule_2014.csv"
TEAM_FILE = "/Users/eotles/Documents/workspace/Bracketology/data/teams_2014.csv"
CONFERENCES_FILE = "/Users/eotles/Documents/workspace/Bracketology/data/conferences_2014.csv"
LAST_PLAYED_WEEK = 9


def main(reps):
    s = Season(TEAM_FILE,SCHEDULE_FILE, CONFERENCES_FILE, LAST_PLAYED_WEEK)
    #s2 = copy.deepcopy(s)
    #mc = s.makeMC(LAST_PLAYED_WEEK)
    #m = np.matrix(mc)
    #print(m)
    #n = copy.deepcopy(m)
    #for i in xrange(100):
    #    print("Iteration %d" %i)
    #    n = n*m
    #    print(n)
    #print(s.makeMC(LAST_PLAYED_WEEK))
    #o = np.sum(n, axis=0)
    #print(o.tolist())
    
    
    #training / testing
    #for t in [8,10,12,14]:
    #    print("%d -> %d" %(t,t+1))
    #    s.training([2],
    #               [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40, 0.5 ,0.5, 0.7, 0.8, 0.9, 1],
    #               [0, 0.1, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    #               t,t+1)
    
    #for t in [9,11,13]:
    #    for setup in [[2, 0.04, 0.3], [2, 0.01, 0.35], [2, 0, 0.29], [2, 0.38, 0.24]]:
    #        print("%d -> %d, %s, %f" %(t,t+1, setup, s.training([setup[0]], [setup[1]], [setup[2]], t, t+1)))
    
    random.seed(42)
    for i in range(10):
        seed = random.randint(0,99999)
        print("---------------------------%d------------------------------------" %i)
        s.runSimulation(seed,reps, 9, 0.04, 0.3)
    

if __name__ == '__main__':
    main(int(sys.argv[1]))