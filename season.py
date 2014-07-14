'''
Created on Jul 12, 2014

@author: eotles
'''
from game import Game

class Season(object):
    '''
    classdocs
    '''


    def __init__(self, currentWeek, teams, scheduleFile):
        self.currentWeek = currentWeek
        self.teams = teams
        self.schedule = dict()
        self.loadSchedule(scheduleFile)
        print(self.schedule)
        for week,gameList in self.schedule.iteritems():
            print(week)
            for Game in gameList:
                Game.toString()
    
    def loadSchedule(self, scheduleFile):
        schedule = open(scheduleFile)
        next(schedule)
        for row in schedule:
            gameData = row.strip().split(",")
            print(gameData)
            gameID = gameData[0]
            gameWeek = int(gameData[1])
            gameLocation = int(gameData[2])
            gameTeams = [self.teams.get(int(gameData[3])), self.teams.get(int(gameData[4]))]
            #print(gameTeams)
            gameScores = [gameData[5], gameData[6]]
            newGame = Game(gameID, gameWeek, gameLocation, gameTeams, gameScores)
            newGame.played = (self.currentWeek <= gameWeek)
            if not(self.schedule.has_key(gameWeek)):
                self.schedule.update({gameWeek: list()})
            self.schedule.update({gameWeek: self.schedule.get(gameWeek)+[(newGame)]})
        schedule.close()
            
            