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



class Season(object):
    #initialize season
    def __init__(self, teamFile, scheduleFile, conferencesFile, lastPlayedWeek):
        self.teams = self.loadTeams(teamFile)
        self.lastPlayedWeek = lastPlayedWeek
        self.schedule = dict()
        self.loadSchedule(scheduleFile, lastPlayedWeek)
        self.loadConferences(conferencesFile)
        self.BLANKMC = [[0 for _ in self.teams] for _ in self.teams]
        self.BLANKGAMERESULTS = [[0 for _ in self.teams] for _ in self.teams]
        self.BLANKCOUNTS = dict()
        for teamID in self.teams:
            self.BLANKCOUNTS.update({teamID: 0})
        #self.gameResultsDict = dict()
        #self.gameCountDict = dict()
        #self.gameResultsDict.update({0: self.BLANKMC})
        #self.gameCountDict.update({0: [0 for _ in self.teams]})
        #for week in xrange(1,lastPlayedWeek+1):
        #    self.makeGR(week)

    
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
        
    def loadConferences(self, conferencesFile):
        confDict = dict()
        confDiv = dict()
        conferences = open(conferencesFile)
        next(conferences)
        for row in conferences:
            conferenceData = row.strip().split(",")
            #print(conferenceData)
            if(conferenceData[2] != ''):
                teamConf = conferenceData[2]
                if(conferenceData[3] != ''):
                    division = conferenceData[3]
                    divList = confDiv.get(teamConf) if(confDiv.has_key(teamConf)) else set()
                    divList.add(division)
                    confDiv.update({teamConf: divList})
                    teamConf += " - " + conferenceData[3]
                #print(teamConf)
                teamList = confDict.get(teamConf) if(confDict.has_key(teamConf)) else list()
                teamList.append(self.teams.get(int(conferenceData[0])))
                confDict.update({teamConf: teamList})

        self.confDict = confDict
        self.confDiv = confDiv
        
        #print(confDict)
        #print(confDiv)
                

    def makeGR(self, lpw):
        gr = list(self.gameResultsDict.get(lpw-1))
        gameCount = list(self.gameCountDict.get(lpw-1))
        for game in self.schedule.get(lpw):
            winner = game.outcome.winner
            loser = game.outcome.loser
            #print("%s,%s,%s" %(game.id, winner, loser))
            if(winner != None):
                gr[loser.id][winner.id] += 1
                gr[winner.id][winner.id] += 1
                gameCount[loser.id] += 1
                gameCount[winner.id] += 1
        
        self.gameResultsDict.update({lpw: gr})
        self.gameCountDict.update({lpw: gameCount})
        return(gr)
    
    
    def makeMC(self, lpw):
        '''
        #mc = [[0 for _ in self.teams] for _ in self.teams]
        #mc = list(self.BLANKMC)
        #gameCount = copy.copy(self.BLANKCOUNTS)
        mc = list(self.gameResultsDict.get(lpw-1))
        #print(mc)
        gameCount = list(self.gameCountDict.get(lpw-1))
        
        for week,gameList in self.schedule.iteritems():
            if(week <= lpw):
                for game in gameList:
                    winner = game.outcome.winner
                    loser = game.outcome.loser
                    #print("%s,%s,%s" %(game.id, winner, loser))
                    if(winner != None):
                        mc[loser.id][winner.id] += 1
                        mc[winner.id][winner.id] += 1
                        gameCount[loser.id] += 1
                        gameCount[winner.id] += 1

        for game in self.schedule.get(lpw):
            winner = game.outcome.winner
            loser = game.outcome.loser
            #print("%s,%s,%s" %(game.id, winner, loser))
            if(winner != None):
                mc[loser.id][winner.id] += 1
                mc[winner.id][winner.id] += 1
                gameCount[loser.id] += 1
                gameCount[winner.id] += 1
        
        self.gameResultsDict.update({lpw: mc})
        self.gameCountDict.update({lpw: gameCount})
        '''

        '''
        mc = self.makeGR(lpw)
        gameCount = self.gameCountDict.get(lpw)
        for rowIndex,row in enumerate(mc):
            rowSum = gameCount[rowIndex]
            if(rowSum != 0):
                nonZeroEntry = 1.0/rowSum
                mc[rowIndex] = [0 if(val==0) else val*nonZeroEntry for val in row]
        '''
        mc = [[0 for _ in self.teams] for _ in self.teams]
        for week, gameList in self.schedule.iteritems():
            if(week <= lpw):
                for game in gameList:
                    winner = game.outcome.winner
                    loser = game.outcome.loser
                    #print("%s,%s,%s" %(game.id, winner, loser))
                    if(winner != None):
                        mc[loser.id][winner.id] += 1
                        #mc[winner.id][winner.id] += 1
        
        for rowIndex, row in enumerate(mc):
            rowSum = sum(row)
            if(rowSum != 0):
                nonZero = float(1)/rowSum
                mc[rowIndex] = [0 if(x==0) else nonZero for x in row]
            

        return(mc)

    #dict().iteritems()

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
        
        
    def runSimulation(self, seed, replications, prIt, homeWeight, minWinPer):
        results = []
        countIn = dict()
        countMiss = dict()
        confIn = dict()
        for teamId,team in self.teams.iteritems():
            countIn.update({team: 0})
            countMiss.update({team: 0})

        rand.seed(seed)
        for repId in xrange(replications):
            #print("Rep: %d" %repId)
            repResult = self.simulateSeason(prIt, homeWeight, minWinPer)
            #print(repResult)
            results.append(repResult)
            for teamId in repResult[:4]:
                team = self.teams.get(teamId)
                countIn.update({team: countIn.get(team)+1})
                #for 
            #team = self.teams.get(repResult[4])
            countMiss.update({team: countMiss.get(team)+1})
               
        for team,count in countIn.iteritems():
            print("%s, %d, %d" %(team.name, count, countMiss.get(team)))
        
        print("\n\n")
        
        for team,count in countIn.iteritems():
            print("%s, %f, %f" %(team.name, float(count)/replications, float(countMiss.get(team))/replications))
        
        
        #print(results)
        #self.countTeamsInTop(results)
    
    def countTeamsInTop(self, results):
        count = dict()
        for teamId,team in self.teams.iteritems():
            count.update({team: 0})
        for row in results[:4]:
            for teamId in row:
                team = self.teams.get(teamId)
                count.update({team: count.get(team)+1})
        
        for team,count in count.iteritems():
            print("%s: %d" %(team.name, count))
            
        
    
    def simulateToWeek(self, prIt, homeWeight, minWinPer, fromWeek, toWeek):
        currSimWeek = fromWeek
        for currSimWeek in range(fromWeek, toWeek):
            #print("sim week: %s" %(currSimWeek))
            self.simulateNextWeek(currSimWeek, prIt, homeWeight, minWinPer)
        
    def championshipGames(self, prIt, champWeek):
        ratings = self.getRatings(prIt, champWeek-1)
        #print(self.confDict)
        gameID = 99999
        gameLocation = -999
        championshipGames = list()
        for conference, divisions in self.confDiv.iteritems():
            #print(conference)
            #print(divisions)
            gameTeams = list()
            for div in divisions:
                confDiv = conference + " - " + div
                #print(confDiv)
                bestRating = -99
                bestTeam = None
                for team in self.confDict.get(confDiv):
                    teamRating = ratings[team.id]
                    if(teamRating > bestRating):
                        bestRating = teamRating
                        bestTeam = team
                gameTeams.append(bestTeam)
            #print(gameTeams)
            gameID += 1
            newGame = Game(gameID, champWeek, gameLocation, gameTeams)
            championshipGames.append(newGame)
            
        return(championshipGames)
    
    def simulateSeason(self, prIt, homeWeight, minWinPer):
        numTop = 5
        teamRating = collections.namedtuple('teamRating', ['teamID', 'rating'])
        rankings = [teamRating(999, -1) for _ in range(0, numTop)]

        self.simulateToWeek(prIt, homeWeight, minWinPer, self.lastPlayedWeek, 16)
        
        #make champ games
        champWeek = 17
        self.schedule.update({champWeek: self.championshipGames(prIt, champWeek)})
        
        #play champ games
        self.simulateNextWeek(16, prIt, homeWeight, minWinPer)
       
        ratings = self.getRatings(prIt, champWeek)
        for teamID, rating in enumerate(ratings):
            for i, ranking in enumerate(rankings):
                if(rating > ranking.rating):
                    for j in range(numTop-1, i, -1):
                        rankings[j] = rankings[j-1]
                    rankings[i] = teamRating(teamID, rating)
                    break
        rankedList = [team.teamID for team in rankings]
        #print(rankedList)
        return(rankedList)
    
    def getRatings(self, prIt, lpw):
        #pageRank
        mc = self.makeMC(lpw)
        prMatrix = np.matrix(mc)
        #ratingMatrix = copy.deepcopy(prMatrix)
        for _ in xrange(prIt-1):
            prMatrix *= prMatrix
            #ratingMatrix = ratingMatrix*prMatrix
        teamRatings = [rating for rating in np.sum(prMatrix, axis=0, keepdims=False).tolist()[0]]
        #teamRatings = [rating for rating in np.sum(ratingMatrix, axis=0, keepdims=False).tolist()[0]]
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
            
            #if(game.teams[0].id  == 55 or game.teams[1].id == 55):
            #    print(lpw)
            #    print("\t%s\t%s\t%f  %f  %f\t%s"   %(game.teams[0].name, game.teams[1].name, ratings[0], ratings[1], pT0Win, winner.id))

        