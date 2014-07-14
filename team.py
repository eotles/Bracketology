'''
Created on Jul 12, 2014

@author: eotles
'''
#from game import Game


class Team(object):
    '''
    classdocs
    '''


    def __init__(self, teamID, name):
        self.id = teamID
        self.name = name
        #self.stats = TeamStats(ranking)
        self.games = dict()
        self.stats = dict()
    
    def addGame(self, Game):
        self.games.update({Game.week: Game})
        

class TeamStats(object):
    def __init__(self, ranking):
        self.stats = dict()
        
class WeeklyStats(object):
    def __init__(self, ranking):
        self.ranking = ranking
        