'''
Created on Oct 12, 2014

@author: eotles
'''

import collections
game = collections.namedtuple('game', ['team1', 'team2', 'date'])

def main():
    fbsFP ="/Users/eotles/Documents/workspace/Bracketology/data/fbs_2014.csv"
    scoresFP = "/Users/eotles/Documents/workspace/Bracketology/data/scores_2014.csv"
    namesFP = "/Users/eotles/Documents/workspace/Bracketology/data/names.txt"
    
    scheduleFP = "/Users/eotles/Documents/workspace/Bracketology/schedule_2014.csv"
    teamsFP = "/Users/eotles/Documents/workspace/Bracketology/teams_2014.csv"
    

    teamNameDict = dict()
    names = open(namesFP)    
    teams = open(teamsFP, "w+")
    teams.write("header\n")
    teamID = 0
    for line in names:
        names = line.strip().split(",")
        for name in names:
            print name
            teamNameDict.update({name: teamID})
        teams.write("%s,%s\n" %(teamID, names[0]))
        teamID+=1
    
    #print(teamNameDict)
       
    gameDict = dict() 
    
    fbs = open(fbsFP)
    for line in fbs:
        line = line.strip().split(",")
        g = game(teamNameDict.get(line[2]), teamNameDict.get(line[4]), line[5])
        #print(g)
        gameDict.update({g : line[6]})
    
    #print(gameDict)
        
        
    scores = open(scoresFP)
    schedule = open(scheduleFP, "w+")
    schedule.write("ID,WEEK,LOC_ID,TEAM1_ID,TEAM2_ID,TEAM1_SCORE,TEAM2_SCORE\n")
    for line in scores:
        data = line
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
                    lID = tNo1
                elif(g1Loc == "Away"):
                    location = t2
                    lID = tNo2
                elif(g1Loc == "Neutral"):
                    location = "Neutral"
                    lID = -999
            elif(g2Loc != None):
                if(g2Loc == "Home"):
                    location = t2
                    lID = tNo2
                elif(g2Loc == "Away"):
                    location = t1
                    lID = tNo1
                elif(g2Loc == "Neutral"):
                    location = "Neutral"
                    lID = -999
            else:
                location = "Neutral"
                lID = -999
                    
            #if(gameDict.get(g) == "Home") else line[8] if(gameDict.get(g2) == "Home") else "Neutral"
            print("%s,%s,%s,%s,%s,%s,%s,%s" %(gNo, wNo, d, t1, s1, t2, s2, location))
            schedule.write("%s,%s,%s,%s,%s,%s,%s\n" %(gNo, wNo, lID, tNo1, tNo2, s1, s2))
    
def date(badString):
    months = {"Aug" : "8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}
    data = badString.split(" ")
    return("%s/%s/%s" %(months.get(data[0]), data[1], data[2][2:]))

def cleanName(name):
    parenPos = name.find("(")
    if(0 <= parenPos and parenPos <3):
        start = name.index(")") + 2
        return(name[start:])
    else:
        return(name)
    
    
    

if __name__ == '__main__':
    main()