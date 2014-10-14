'''
Created on Jul 12, 2014

@author: eotles
'''

#Object representing a team
class Team(object):

    #teamID: unique identifier of team
    #team name: name of team
    #games helps to keep track of every game team plays in.
    def __init__(self, teamID, name):
        self.id = teamID
        self.name = name
        self.games = dict()
    
    #Add game to the list of games that this team plays in
    def addGame(self, Game):
        self.games.update({Game.week: Game})
        