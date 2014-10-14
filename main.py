'''
Created on Jul 12, 2014

@author: eotles
'''
from season import Season
from team import Team
import numpy as np
import copy

SCHEDULE_FILE = "/Users/eotles/Documents/workspace/Bracketology/schedule.csv"
TEAM_FILE = "/Users/eotles/Documents/workspace/Bracketology/teams.csv"
LAST_PLAYED_WEEK = 2


def main():
    s = Season(TEAM_FILE,SCHEDULE_FILE, LAST_PLAYED_WEEK)
    mc = s.makeMC(LAST_PLAYED_WEEK)
    m = np.matrix(mc)
    print(m)
    n = copy.deepcopy(m)
    for i in xrange(100):
        print("Iteration %d" %i)
        n = n*m
        print(n)
    #print(s.makeMC(LAST_PLAYED_WEEK))
    

if __name__ == '__main__':
    main()