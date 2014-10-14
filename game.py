'''
Created on Jul 12, 2014

@author: eotles
'''
from team import Team
import abc
from _pyio import __metaclass__

#Object representing a game.
class Game(object):

    #gameID: unique game identifier
    #week: the week number the game is being played in // might not be necessary
    #location:
    #teams: list like [team1, team2] to represent teams playing.
    def __init__(self, gameID, week, location, teams):
        self.id = gameID
        self.teams = teams
        self.location = location
        self.week = week
        for team in teams:
            team.addGame(self)
        self.outcome = None
        
    def addOutcome(self, scores):
        self.outcome = Outcome(self.teams, scores)

    def toString(self):
        outString = str(self.id) +"\t"
        for teamIndex,team in enumerate(self.teams):
            outString += team.name
            if(self.outcome != None):
                outString += ": " + str(self.outcome.scores[teamIndex])
            outString += "\t"
        print(outString)

class Outcome(object):
    def __init__(self, teams, scores):
        self.winner = teams[0] if (scores[0] > scores[1]) else (teams[1] if (scores[0] < scores[1]) else None)
        self.loser  = teams[1] if (scores[0] > scores[1]) else (teams[0] if (scores[0] < scores[1]) else None)
        self.scores = scores
