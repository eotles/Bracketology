'''
Created on Jul 12, 2014

@author: eotles
'''
from season import Season
from team import Team

SCHEDULE_FILE = "/Users/eotles/Documents/workspace/Bracketology/schedule.csv"
CURRENT_WEEK = 0
TEAMS = {1:Team(1, "ONE"), 2:Team(2, "Two"), 3:Team(3, "Three"), 4:Team(4, "Four")}
WEEKS = ["1", "2", "3"]


def main():
    Season(CURRENT_WEEK,TEAMS,SCHEDULE_FILE)
    

if __name__ == '__main__':
    main()