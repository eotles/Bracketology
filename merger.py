'''
Created on Oct 12, 2014

@author: eotles
'''

import collections
game = collections.namedtuple('game', ['team1', 'team2', 'date'])

def main():
    fbsFP ="/Users/eotles/Documents/workspace/Bracketology/fbs.csv"
    scoresFP = "/Users/eotles/Documents/workspace/Bracketology/scores.csv"
    namesFP = "/Users/eotles/Documents/workspace/Bracketology/names.txt"
    
    teamNameDict = dict()
    names = open(namesFP)
    teamID = 0
    for line in names:
        for name in line.strip().split(","):
            teamNameDict.update({name: teamID})
        teamID+=1
    
    #print(teamNameDict)
       
    gameDict = dict() 
    
    fbs = open(fbsFP)
    for line in fbs:
        line = line.strip().split(",")
        g = game(teamNameDict.get(line[2]), teamNameDict.get(line[4]), line[5])
        gameDict.update({g : line[6]})
    
    #print(gameDict)
        
        
    scores = open(scoresFP)
    for line in scores:
        data = []
        line = line.strip().split(",")
        #print(line)
        if(line[0] != "Rk"):
            gNo = line[0]
            wNo = line[1]
            d = date(line[2])
            t1 = cleanName(line[5])
            tNo1 = teamNameDict.get(t1)
            s1 = line[6]
            t2 = cleanName(line[8])
            tNo2 = teamNameDict.get(t2)
            s2 = line[9]
            g = game(tNo1, tNo2, d)
            g2 = game(tNo2, tNo1, d)
            #print(g)
            #print(date(line[2]))
            g1Loc = gameDict.get(g)
            g2Loc = gameDict.get(g2)
            if(g1Loc != None):
                if(g1Loc == "Home"):
                    location = t1 
                elif(g1Loc == "Away"):
                    location = t2
                elif(g1Loc == "Neutral"):
                    location = "Neutral"
            elif(g2Loc != None):
                if(g2Loc == "Home"):
                    location = t2
                elif(g2Loc == "Away"):
                    location = t1
                elif(g2Loc == "Neutral"):
                    location = "Neutral"
            else:
                location = "Neutral"
                    
            #if(gameDict.get(g) == "Home") else line[8] if(gameDict.get(g2) == "Home") else "Neutral"
            print("%s,%s,%s,%s,%s,%s,%s,%s" %(gNo, wNo, d, t1, s1, t2, s2, location))
    
def date(badString):
    months = {"Aug" : "8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}
    data = badString.split(" ")
    return("%s/%s/%s" %(months.get(data[0]), data[1], data[2][2:]))

def cleanName(name):
    if("(" in name):
        start = name.index(")") + 2
        return(name[start:])
    else:
        return(name)
    
    
    

if __name__ == '__main__':
    main()