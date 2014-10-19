'''
Created on Jul 12, 2014

@author: eotles
'''
from game import Game
from team import Team
import collections
import math
import numpy as np
import random as rand
import copy

class Season(object):
    #initialize season
    def __init__(self, teamFile, scheduleFile, lastPlayedWeek):
        self.teams = self.loadTeams(teamFile)
        self.lastPlayedWeek = lastPlayedWeek
        self.schedule = dict()
        self.loadSchedule(scheduleFile, lastPlayedWeek)
        #for week,gameList in self.schedule.iteritems():
        #    print("Week #%d" %week)
        #    for Game in gameList:
        #        Game.toString()
    
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
            #print(gameData)
            gameID = gameData[0]
            gameWeek = int(gameData[1])
            gameLocation = int(gameData[2])
            gameTeams = [self.teams.get(int(gameData[3])), self.teams.get(int(gameData[4]))]
            newGame = Game(gameID, gameWeek, gameLocation, gameTeams)
            if(gameWeek <= lastPlayedWeek):
                gameScores = [int(gameData[5]) if(gameData[5] != '') else 0, 
                              int(gameData[6]) if(gameData[6] != '') else 0]
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
                    #print("%s,%s,%s" %(game.id, winner, loser))
                    if(winner != None):
                        mc[loser.id][winner.id] += 1
                        #mc[winner.id][winner.id] += 1
        for rowIndex,row in enumerate(mc):
            rowSum = sum(row)
            if(rowSum != 0):
                mc[rowIndex] = [float(val)/rowSum for val in row]
        return(mc)

    dict().iteritems()

    def training(self, prItRange, hwRange, mwpRange, fromWeek, answerWeek):
        minErrorSetup = ""
        minError = 99999999
        for prIt in prItRange:
            for homeWeight in hwRange:
                for minWinPer in mwpRange:
                    setup = [prIt, homeWeight, minWinPer]
                    setupError = 0
                    #self.simulateToWeek(prIt, homeWeight, minWinPer, fromWeek, answerWeek)
                    
                    teamRatings = self.getRatings(prIt, fromWeek)
                    gameList = self.schedule.get(answerWeek)
                    #game = Game()
                    #print("\tSimulating Week: %d" %(lpw+1))
                    for game in gameList:
                        #game.toString()
                        ratings = [max(teamRatings[team.id], 0.001) for team in game.teams]
                        homeAdv = homeWeight if(game.location == game.teams[0].id) else -homeWeight if(game.location == game.teams[1].id) else 0
                        pT0Win = min(max(ratings[0]/sum(ratings) + homeAdv , minWinPer), 1.0-minWinPer)
                        actualP = float(game.outcome.scores[0]+1)/(sum(game.outcome.scores)+2)
                        error = math.fabs(pT0Win - actualP)
                        setupError += error
                        #print("%s %s %s" %(pT0Win, actualP, error))
                    #print(setup)
                    #print(setupError)
                    if(setupError < minError):
                        minError = setupError
                        minErrorSetup = setup
        print(minErrorSetup)
        return(minError)
        
    '''
    def training(self, answer):
        results = []
        #rand.seed(42)
        replications = 100
        
        totalOrderingScore = 0
        mOS = 9999999999
        mO = list()
        totalContainingScore = 0
        mCS = 99999999999
        mC = list()
        totalTop10Score = 0
        mTS = 99999999999
        mT = list()
        totalTop4Score = 0
        mT4S = 99999999999
        mT4 = list()
        for prIt in range(0,10,2):
            for homeWeight in [0, 0.01, 0.05, 0.1, 0.15, 0.20, 0.25, 0.5]:
                for minWinPer in [0, 0.01, 0.05, 0.1, 0.15, 0.20]:
                    setup = [prIt, homeWeight, minWinPer]
                    print(setup)
                    totalOrderingScore = 0
                    totalContainingScore = 0
                    totalTop10Score = 0
                    totalTop4Score = 0
                    rand.seed(42)
                    for repId in xrange(replications):
                        #print("Replication: %d" %(repId))
                        repResult = self.simulateSeason(prIt, homeWeight, minWinPer)
                        #print(repResult)
                        results.append(repResult)
                        
                        #orderingscore = 0
                        #for index,team in enumerate(repResult):
                        #    if(team != answer[index]):
                        #        orderingscore += 25-index
                        
                        #containingscore = 0
                        #for team in repResult:
                        #    if(team not in answer):
                        #        containingscore += 1
                        
                        #top10score = 0
                        #for team in repResult[0:10]:
                        #    if(team not in answer[0:10]):
                        #        top10score += 1
                        
                        top4Score = 0
                        print repResult[0:4]
                        print answer[0:4]
                        for team in repResult[0:4]:
                            if(team not in answer[0:4]):
                                top4Score = 1
                                break
                        
                        
                                
                        #print("%d %d %d" %(orderingscore, containingscore, top10score))
                        #totalOrderingScore += orderingscore
                        #totalContainingScore += containingscore
                        #totalTop10Score += top10score
                        totalTop4Score += top4Score
                        if(totalOrderingScore < mOS):
                            mOS = totalOrderingScore
                            mO = setup
                        if(totalContainingScore < mCS):
                            mCS = totalContainingScore
                            mC = setup
                        if(totalTop10Score < mTS):
                            mTS = totalTop10Score
                            mT = setup
                        if(totalTop4Score < mTS):
                            mT4S = totalTop4Score
                            mT4 = setup
                    print("%d %d %d %d" %(totalOrderingScore, totalContainingScore, totalTop10Score, totalTop4Score))
        print mOS,
        print(mO)
        print mC,
        print(mC)
        print mT,
        print(mT)
        print mT4,
        print(mT4)
    '''

    def runSimulation(self, replications, prIt, homeWeight, minWinPer):
        results = []
        rand.seed(42)
        for repId in xrange(replications):
            print("Replication: %d" %(repId))
            repResult = self.simulateSeason(prIt, homeWeight, minWinPer)
            print(repResult)
            results.append(repResult)
        print(results)
        counts = [dict() for _ in repResult]
        for row in results:
            for colIndex,val in enumerate(row):
                valCount = 1
                if(counts[colIndex].has_key(val)):
                    valCount = counts[colIndex].get(val) + 1
                counts[colIndex].update({val: valCount})
        print(counts)
        x = list()
        for teamCount in counts:
            minCount = 0
            minCountTeam = 999
            for team,count in teamCount.iteritems():
                if((count > minCount) and not(team in x)):
                    minCount = count
                    minCountTeam = team
            x.append(minCountTeam)
        print(x)
        return(x)
    
    def simulateToWeek(self, prIt, homeWeight, minWinPer, fromWeek, toWeek):
        currSimWeek = fromWeek
        for currSimWeek in range(fromWeek, toWeek):
            self.simulateNextWeek(currSimWeek, prIt, homeWeight, minWinPer)
    
    def simulateSeason(self, prIt, homeWeight, minWinPer):
        numTop = 25
        teamRating = collections.namedtuple('teamRating', ['teamID', 'rating'])
        rankings = [teamRating(999, -1) for _ in range(0, numTop)]

        self.simulateToWeek(prIt, homeWeight, minWinPer, self.lastPlayedWeek, 16)
       
        ratings = self.getRatings(prIt, 16)
        for teamID, rating in enumerate(ratings):
            for i, ranking in enumerate(rankings):
                if(rating > ranking.rating):
                    for j in range(numTop-1, i, -1):
                        rankings[j] = rankings[j-1]
                    rankings[i] = teamRating(teamID, rating)
                    break
        rankedList = [team.teamID for team in rankings]
        return(rankedList)
    
    def getRatings(self, prIt, lpw):
        #pageRank
        mc = self.makeMC(lpw)
        prMatrix = np.matrix(mc)
        ratingMatrix = copy.deepcopy(prMatrix)
        for _ in xrange(prIt-1):
            ratingMatrix = ratingMatrix*prMatrix
        teamRatings = [rating for rating in np.sum(ratingMatrix, axis=0, keepdims=False).tolist()[0]]
        return(teamRatings)
    
    def simulateNextWeek(self, lpw, prIt, homeWeight, minWinPer):
        #pageRank
        teamRatings = self.getRatings(prIt, lpw)
        
        #predict game outcomes
        gameList = self.schedule.get(lpw+1)
        #game = Game()
        #print("\tSimulating Week: %d" %(lpw+1))
        for game in gameList:
            ratings = [max(teamRatings[team.id], 0.001) for team in game.teams]
            homeAdv = homeWeight if(game.location == game.teams[0].id) else -homeWeight if(game.location == game.teams[1].id) else 0
            pT0Win = max(ratings[0]/sum(ratings) + homeAdv , minWinPer)
            randVar = rand.uniform(0,1)
            if(randVar <= pT0Win):
                winner = game.teams[0]
                scores = [99,0]
                game.addOutcome(scores)
            else:
                scores = [0,99]
                winner = game.teams[1]
                game.addOutcome(scores)
            #print("\t%s\t%s\t%f  %f  %f\t%s"   %(game.teams[0].id, game.teams[1].id, ratings[0], ratings[1], pT0Win, winner.id))

        