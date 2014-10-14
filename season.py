'''
Created on Jul 12, 2014

@author: eotles
'''
from game import Game
from team import Team

class Season(object):
    #initialize season
    def __init__(self, teamFile, scheduleFile, lastPlayedWeek):
        self.teams = self.loadTeams(teamFile)
        self.schedule = dict()
        self.loadSchedule(scheduleFile, lastPlayedWeek)
        for week,gameList in self.schedule.iteritems():
            print("Week #%d" %week)
            for Game in gameList:
                Game.toString()
    
    #open team file.  Make and return team dictionary
    #teamID -> team for all teams
    def loadTeams(self, teamFilePath):
        teams = dict()
        teamFile = open(teamFilePath)
        next(teamFile)
        #teamID = 0
        for row in teamFile:
            teamData = row.strip().split(",")
            teamID = int(teamData[0])
            teamName = teamData[1]
            teams.update({teamID : Team(teamID, teamName)})
            #teamID += 1
        return(teams)
    
    #open schedule file.  Make and return schedule dictionary
    #week -> list of games
    def loadSchedule(self, scheduleFile, lastPlayedWeek):
        schedule = open(scheduleFile)
        next(schedule)
        #gameID = 0
        for row in schedule:
            gameData = row.strip().split(",")
            print(gameData)
            gameID = gameData[0]
            gameWeek = int(gameData[1])
            gameLocation = int(gameData[2])
            gameTeams = [self.teams.get(int(gameData[3])), self.teams.get(int(gameData[4]))]
            newGame = Game(gameID, gameWeek, gameLocation, gameTeams)
            if(gameWeek <= lastPlayedWeek):
                gameScores = [int(gameData[5]), int(gameData[6])]
                newGame.addOutcome(gameScores)
            
            if not(self.schedule.has_key(gameWeek)):
                self.schedule.update({gameWeek: list()})
            self.schedule.update({gameWeek: self.schedule.get(gameWeek)+[(newGame)]})
            #gameID += 1
        schedule.close()

    def makeMC(self, lpw):
        mc = [[0 for _ in self.teams] for _ in self.teams]
        for week,gameList in self.schedule.iteritems():
            if(week <= lpw):
                for game in gameList:
                    winner = game.outcome.winner
                    loser = game.outcome.loser
                    mc[loser.id][winner.id] += 1
                    mc[winner.id][winner.id] += 1
        for rowIndex,row in enumerate(mc):
            rowSum = sum(row)
            mc[rowIndex] = [float(val)/rowSum for val in row]
        return(mc)