'''
Created on Jul 12, 2014

@author: eotles
'''
from team import Team
import abc
from _pyio import __metaclass__

class Game(object):


    def __init__(self, gameID, week, location, teams, scores):
        self.id = gameID
        self.teams = teams
        self.location = location
        self.week = week
        self.played = None
        self.outcome = RealOutcome(teams, scores) if(self.played) else SimuOutcome()
        for team in teams:
            team.addGame(self)

    def toString(self):
        print(self.id +"\t" + str(self.teams))
        
    def getWinner(self):
        return(self.team[0] 
               if (self.teams[0].getRanking < self.teams[1].getRanking) 
               else self.team[1])
    
class Outcome(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, teams, scores):
        self.winner = None
        self.scores = dict()
        for index,team in enumerate(teams):
                self.scores.update({team: scores[index]})
    
class RealOutcome(Outcome):
    def __init__(self):
        super(RealOutcome, self).__init__()
    
    
class SimuOutcome(Outcome):
    def __init__(self):
        super(SimuOutcome, self).__init__()