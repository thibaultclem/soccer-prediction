# - *- coding: utf- 8 - *-

import difflib
import urllib
import json
import sqlite3
import requests

#loadDataToDB("./data/raw/F1.csv","./data/db/ligue1.sqlite")
def extractFromWebSite(leagueId, season, db):

    maxColumn = 26

    website = "http://www.football-data.co.uk/mmz4281"
    currentSeason = season[2:4]+str(int(season[2:4])+1)
    url = website+"/"+currentSeason+"/"+leagueId+".csv"

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Drop the table
    cur.execute('DROP TABLE IF EXISTS RAWDATAS')

    # Create the table
    l1csv = urllib.urlopen(url)
    columns = l1csv.readline().strip().replace('<','MINOR').replace('>','MAJOR').replace('.','POINT').replace('AS','ASX')
    columnsList = columns.split(',')
    columnDef = ""
    counter = 0
    for column in columnsList:
        #Get only 25 five first column
        counter += 1
        if (counter > maxColumn): break
        columnDef = columnDef+column+" TEXT, "

    query = "CREATE TABLE RAWDATAS ("+columnDef.rstrip().rstrip(',')+")"

    cur.execute(query)

    conn.commit()

    #Get only the 25 first result of the column list
    columns = columnsList[0]
    for nb in range(1,maxColumn):
        columns += ","+columnsList[nb]

    #Get historic data for last 3 seasons
    for x in range(0, 1):

        seasonRawData = str(int(season[2:4])-x)+str(int(season[2:4])-x+1)
        url = website+"/"+seasonRawData+"/"+leagueId+".csv"

        ## Download csv containing historic data
        l1csv = urllib.urlopen(url)

        # Skip the first line
        l1csv.readline()

        # Insert data into table
        for row in l1csv:
            valuesDef = ""
            values = row.strip().split(',')
            count = 0
            for value in values:
                count += 1
                if (count > maxColumn): break
                valuesDef = valuesDef + "'"+value.replace("'",'')+"', "
            #print valuesDef.strip().strip(",")
            queryRow = "INSERT INTO RAWDATAS (" + columns.strip() + ") VALUES (" + valuesDef.strip().strip(",") + ")"
            cur.execute(queryRow)

        conn.commit()

    conn.close()

#loadDataToDB("./data/raw/F1.csv","./data/db/ligue1.sqlite")
def extractFromCsv(csvInputPath, db):
    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Drop the table
    cur.execute('DROP TABLE IF EXISTS RAWDATAS')

    ## Open F1.csv containing ligue 1 historic data
    l1csv = open(csvInputPath)

    # Create the table
    columns = l1csv.readline().strip().replace('<','MINOR').replace('>','MAJOR').replace('.','POINT').replace('AS','ASX')
    columnsList = columns.split(',')
    columnDef = ""
    for column in columnsList:
        columnDef = columnDef+column+" TEXT, "

    query = "CREATE TABLE RAWDATAS ("+columnDef.rstrip().rstrip(',')+")"

    cur.execute(query)

    conn.commit()

    # Insert data into table
    for row in l1csv:
        valuesDef = ""
        values = row.strip().split(',')
        for value in values:
            valuesDef = valuesDef + "'"+value.replace("'",'')+"', "
        #print valuesDef.strip().strip(",")
        queryRow = "INSERT INTO RAWDATAS (" + columns.strip() + ") VALUES (" + valuesDef.strip().strip(",") + ")"
        cur.execute(queryRow)

    conn.commit()
    conn.close()


#
# Get All Teams and add them to a TEAM table
#
#createHistoricSeasonTable("./data/db/ligue1.sqlite","RAWDATAS")
def createHistoricSeasonTable(db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Drop the table
    cur.execute('DROP TABLE IF EXISTS TEAMS')
    cur.execute('CREATE TABLE TEAMS (Name TEXT)')
    conn.commit()

    cur.execute('SELECT DISTINCT HomeTeam FROM RAWDATAS ORDER BY HomeTeam')
    for row in cur.fetchall():
        cur.execute('INSERT INTO TEAMS(Name) VALUES (?)',(row[0], ))

    conn.commit()

    #
    # Get stats for all matchs
    #
    cur.execute('DROP TABLE IF EXISTS MATCHS')
    cur.execute('''
        CREATE TABLE MATCHS (
            MatchDate DATE,
            DateInt DATE,
            HomeTeam TEXT,
            AwayTeam TEXT,
            FTHG INTEGER,
            FTAG INTEGER,
            FTR CHAR,
            BetH INTEGER,
            BetD INTEGER,
            BetA INTEGER
            )
    ''')
    #FTHG = Full Time Home Team Goals
    #FTAG = Full Time Away Team Goals
    #FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
    conn.commit()

    cur.execute('''
    SELECT Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR, B365H, B365A, B365D
    FROM RAWDATAS
    ''')

    for row in cur.fetchall():

        #Get the bet associate to the Result
        bet = row[6]
        if (row[5] == 'A'): bet = row[7]
        elif (row[5] == 'D'): bet = row[8]

        cur.execute('''
            INSERT INTO
                MATCHS(MatchDate, DateInt, HomeTeam, AwayTeam, FTHG, FTAG, FTR, BetH, BetD, BetA)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
        ,(row[0],
        row[0][6:]+row[0][3:5]+row[0][:2],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[8],
        row[7] ))
    conn.commit()

    conn.close()

#
#
#
# createDataModelTable("./data/db/ligue1.sqlite",5,"151022")
def createDataModelTable(db, deepLimit, firstDateMatch):

    # 10-30 50-70 80-...
    # Where (dateInt > 80) OR (dateInt > 50 AND dateInt < 70) OR (dateInt > 10 AND dateInt < 30)

    #Calcul for remove interseason
    inter1 = "(DateInt >= "+firstDateMatch+")"
    inter2 = "(DateInt >= "+str(int(firstDateMatch)-10000)+" AND DateInt < "+str(int(firstDateMatch)-300)+")"
    inter3 = "(DateInt >= "+str(int(firstDateMatch)-20000)+" AND DateInt < "+str(int(firstDateMatch)-10300)+")"

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    homeVictory = 0
    awayVictory = 0
    draw = 0
    total = 0.0
    cur.execute('SELECT FTR FROM MATCHS')
    for row in cur.fetchall():
        total += 1
        if (row[0] == 'H'): homeVictory += 1
        elif (row[0] == 'D'): draw += 1
        elif (row[0] == 'A'): awayVictory += 1

    print "League:",db
    print "Number of Home victory: ",homeVictory,"-",homeVictory/total*100,"%"
    print "Number of Away victory: ",awayVictory,"-",awayVictory/total*100,"%"
    print "Number of Draw: ",draw,"-",draw/total*100,"%"

    ## Fill prematch table

    cur.execute('DROP TABLE IF EXISTS PREMATCHS')
    cur.execute('''
    CREATE TABLE PREMATCHS (
        HomeVictory INTEGER,
        HomeDefeat INTEGER,
        HomeDraw INTEGER,
        HomeGoal INTEGER,
        ExtVictory INTEGER,
        ExtDefeat INTEGER,
        ExtDraw INTEGER,
        ExtGoal INTEGER,
        Result CHAR,
        BetH INTEGER,
        BetD INTEGER,
        BetA INTEGER,
        DateInt DATE
        )
    ''')

    # We don't use the first 5 games (date format is AAMMDD)
    query = '''
        SELECT MatchDate, DateInt, HomeTeam, AwayTeam, FTR, BetH, BetD, BetA, DateInt
        FROM MATCHS
        WHERE '''+inter1+''' OR '''+inter2+''' OR '''+inter3+''' ORDER BY DateInt'''
    cur.execute(query)
    matchs = cur.fetchall()

    for match in matchs:

        # Get 5 previous matchs of Home Teams
        #print match
        cur.execute('''
            SELECT FTHG, FTR
            FROM MATCHS
            WHERE DateInt < ? AND HomeTeam = ? ORDER BY DateInt DESC LIMIT ?'''
        ,(match[1], match[2].strip(), deepLimit, ))
        matchsHome = cur.fetchall()
        countHome = 0.0
        nbHomeVictory = 0
        nbHomeDefeat = 0
        nbHomeDraw = 0
        nbHomeGoal = 0
        for matchHome in matchsHome:
            countHome += 1
            nbHomeGoal += matchHome[0]
            if (matchHome[1] == 'H'): nbHomeVictory += 1
            elif (matchHome[1] == 'D'): nbHomeDraw += 1
            elif (matchHome[1] == 'A'): nbHomeDefeat += 1

        # Get 5 previous matchs of Away Teams
        cur.execute('''
            SELECT FTAG, FTR
            FROM MATCHS
            WHERE DateInt < ? AND AwayTeam = ? ORDER BY DateInt DESC LIMIT ?'''
            ,(match[1], match[3].strip(), deepLimit, ))
        matchsExt = cur.fetchall()
        countExt = 0.0
        nbExtVictory = 0
        nbExtDefeat = 0
        nbExtDraw = 0
        nbExtGoal = 0
        for matchExt in matchsExt:
            countExt += 1
            nbExtGoal += matchExt[0]
            if (matchExt[1] == 'A'): nbExtVictory += 1
            elif (matchExt[1] == 'D'): nbExtDraw += 1
            elif (matchExt[1] == 'H'): nbExtDefeat += 1
        cur.execute('''
        INSERT INTO PREMATCHS(
            HomeVictory,
            HomeDefeat,
            HomeDraw,
            HomeGoal,
            ExtVictory,
            ExtDefeat,
            ExtDraw,
            ExtGoal,
            Result,
            BetH,
            BetD,
            BetA,
            DateInt)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',
        (nbHomeVictory/countHome,
        nbHomeDefeat/countHome,
        nbHomeDraw/countHome,
        nbHomeGoal/countHome,
        nbExtVictory/countExt,
        nbExtDefeat/countExt,
        nbExtDraw/countExt,
        nbExtGoal/countExt,
        match[4],
        match[5],
        match[6],
        match[7],
        match[8], ))
        conn.commit()
        #print nbHomeVictory/countHome, nbHomeDefeat/countHome, nbHomeDraw/countHome, nbHomeGoal/countHome, nbExtVictory/countExt, nbExtDefeat/countExt, nbExtDraw/countExt, nbExtGoal/countExt, match[4], match[5]

    conn.close()

#
#
#
# exportDataModelToCsv("./data/result/l1-data.csv"","./data/db/ligue1.sqlite")
def exportDataModelToCsv(csvModelOutputPath,db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Print all to csv
    #l1Result = open("./data/result/L1-toPredict.csv",'w')
    dataModel = open(csvModelOutputPath,'w')

    dataModel.write("HomeVictory,HomeDefeat,HomeDraw,HomeGoal,ExtVictory,ExtDefeat,ExtDraw,ExtGoal,Result\n")
    #l1Result.write("HomeVictory,HomeDefeat,HomeDraw,HomeGoal,ExtVictory,ExtDefeat,ExtDraw,ExtGoal\n")

    cur.execute('SELECT * FROM PREMATCHS')
    for match in cur.fetchall():
        line = str(match[0])+','+str(match[1])+','+str(match[2])+','+str(match[3])+','+str(match[4])+','+str(match[5])+','+str(match[6])+','+str(match[7])+','+str(match[8])
        #line = str(match[0])+','+str(match[1])+','+str(match[2])+','+str(match[3])+','+str(match[4])+','+str(match[5])+','+str(match[6])+','+str(match[7])
        dataModel.write(line+'\n')
    dataModel.close

    conn.close()

#
#
#
# exportDataModelToCsv("./data/result/l1-data.csv"","./data/db/ligue1.sqlite")
def exportDataModelWithBetToCsv(csvModelOutputPath,db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Print all to csv
    dataModel = open(csvModelOutputPath,'w')

    dataModel.write("HomeVictory,HomeDefeat,HomeDraw,HomeGoal,ExtVictory,ExtDefeat,ExtDraw,ExtGoal,Date,TrueResult,BetH, BetD, BetA\n")

    cur.execute('SELECT * FROM PREMATCHS')
    for match in cur.fetchall():
        line = str(match[0])+','+str(match[1])+','+str(match[2])+','+str(match[3])+','+str(match[4])+','+str(match[5])+','+str(match[6])+','+str(match[7])+','+str(match[12])+','+str(match[8])+','+str(match[9])+','+str(match[10])+','+str(match[11])
        #line = str(match[0])+','+str(match[1])+','+str(match[2])+','+str(match[3])+','+str(match[4])+','+str(match[5])+','+str(match[6])+','+str(match[7])
        dataModel.write(line+'\n')
    dataModel.close

    conn.close()


#
#
# createDataModelTable("./data/db/ligue1.sqlite",5)
def createDataPredictTable(db, deepLimit):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    ## Fill prenextmatch table

    cur.execute('DROP TABLE IF EXISTS PRENEXTMATCHS')
    cur.execute('''
        CREATE TABLE PRENEXTMATCHS (
            Home TEXT,
            Away TEXT,
            HomeVictory INTEGER,
            HomeDefeat INTEGER,
            HomeDraw INTEGER,
            HomeGoal INTEGER,
            ExtVictory INTEGER,
            ExtDefeat INTEGER,
            ExtDraw INTEGER,
            ExtGoal INTEGER
            )
    ''')

    # We don't use the first 5 games (date format is AAMMDD)
    cur.execute('SELECT MatchDate, DateInt, HomeTeam, AwayTeam FROM NEXTMATCHS')
    matchs = cur.fetchall()

    for match in matchs:

        # Get 5 previous matchs of Home Teams
        #print match
        cur.execute('''
            SELECT FTHG, FTR
            FROM MATCHS
            WHERE DateInt < ? AND HomeTeam = ? ORDER BY DateInt DESC LIMIT ?
        ''',
        (match[1], match[2], deepLimit, ))
        matchsHome = cur.fetchall()
        countHome = 0.0
        nbHomeVictory = 0
        nbHomeDefeat = 0
        nbHomeDraw = 0
        nbHomeGoal = 0
        for matchHome in matchsHome:
            countHome += 1
            nbHomeGoal += matchHome[0]
            if (matchHome[1] == 'H'): nbHomeVictory += 1
            elif (matchHome[1] == 'D'): nbHomeDraw += 1
            elif (matchHome[1] == 'A'): nbHomeDefeat += 1

        # Get 5 previous matchs of Away Teams
        cur.execute('''
            SELECT FTAG, FTR
            FROM MATCHS
            WHERE DateInt < ? AND AwayTeam = ? ORDER BY DateInt DESC LIMIT ?''',
        (match[1], match[3], deepLimit, ))
        matchsExt = cur.fetchall()
        countExt = 0.0
        nbExtVictory = 0
        nbExtDefeat = 0
        nbExtDraw = 0
        nbExtGoal = 0
        for matchExt in matchsExt:
            countExt += 1
            nbExtGoal += matchExt[0]
            if (matchExt[1] == 'A'): nbExtVictory += 1
            elif (matchExt[1] == 'D'): nbExtDraw += 1
            elif (matchExt[1] == 'H'): nbExtDefeat += 1
        cur.execute('''
            INSERT INTO PRENEXTMATCHS(
                Home,
                Away,
                HomeVictory,
                HomeDefeat,
                HomeDraw,
                HomeGoal,
                ExtVictory,
                ExtDefeat,
                ExtDraw,
                ExtGoal)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        ''',
        (match[2],
        match[3],
        nbHomeVictory/countHome,
        nbHomeDefeat/countHome,
        nbHomeDraw/countHome,
        nbHomeGoal/countHome,
        nbExtVictory/countExt,
        nbExtDefeat/countExt,
        nbExtDraw/countExt,
        nbExtGoal/countExt, ))
        conn.commit()
        #print match[2], match[3], nbHomeVictory/countHome, nbHomeDefeat/countHome, nbHomeDraw/countHome, nbHomeGoal/countHome, nbExtVictory/countExt, nbExtDefeat/countExt, nbExtDraw/countExt, nbExtGoal/countExt

    conn.close()


#exportDataPredictToCsv("./data/result/L1-predict.csv","./data/db/ligue1.sqlite")
def exportDataPredictToCsv(csvPredictOutputPath,db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Print all to csv
    #l1Result = open("./data/result/L1-predict.csv",'w')
    resultNextmatch = open(csvPredictOutputPath,'w')

    resultNextmatch.write("Home,Away,HomeVictory,HomeDefeat,HomeDraw,HomeGoal,ExtVictory,ExtDefeat,ExtDraw,ExtGoal\n")

    cur.execute('SELECT * FROM PRENEXTMATCHS')
    for match in cur.fetchall():
        line = str(match[0])+','+str(match[1])+','+str(match[2])+','+str(match[3])+','+str(match[4])+','+str(match[5])+','+str(match[6])+','+str(match[7])+','+str(match[8])+','+str(match[9])
        newLine = line.rstrip('None')
        #print newLine
        resultNextmatch.write(newLine+'\n')
    resultNextmatch.close

    conn.close()

def exportTeamsToCSV(csvOutputPath, db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Print all to csv
    #l1Result = open("./data/result/L1-predict.csv",'w')
    teamsCsv = open(csvOutputPath,'w')

    cur.execute('SELECT * FROM TEAMS')
    for match in cur.fetchall():
        teamsCsv.write(str(match[0])+'\n')
    teamsCsv.close

    conn.close()

def createNextMatchTable(season,leagueId,db):

    seasonInfoURL = "http://api.football-data.org/v1/soccerseasons/?season="+str(season)
    urlNextMatch = "http://api.football-data.org/v1/fixtures"

    headers = { 'X-Auth-Token': 'c6d148de587f4db99f0495b9babe50fd', 'X-Response-Control': 'minified' }

    # Get the current match day
    seasonInfo = json.loads(requests.get(seasonInfoURL,headers=headers).text)
    for leagueInfo in seasonInfo:
        if (leagueInfo['league'] == leagueId):
            matchDay = str(leagueInfo["currentMatchday"])
            url = "http://api.football-data.org/v1/fixtures?matchday="+matchDay+"&league="+leagueId

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS NEXTMATCHS')
    cur.execute('''
    CREATE TABLE NEXTMATCHS (
        MatchDate DATE,
        DateInt DATE,
        HomeTeam TEXT,
        AwayTeam TEXT
        )
    ''')

    teams = list()
    cur.execute('SELECT * FROM TEAMS')
    for match in cur.fetchall():
        teams.append(str(match[0]))

    nextGamesInfo = json.loads(requests.get(url,headers=headers).text)

    for nextGameInfo in nextGamesInfo["fixtures"]:
        # Match Teams name different from soccer API
        homeTeam = difflib.get_close_matches(nextGameInfo['homeTeamName'],teams,1,0.3)[0]
        awayTeam = difflib.get_close_matches(nextGameInfo['awayTeamName'],teams,1,0.3)[0]

        # Trick for bad named teams (not good code :) )
        if (leagueId == "BL2"):
            if (nextGameInfo['homeTeamName'][:8] == "TSV 1860"): homeTeam = "Munich 1860"
            if (nextGameInfo['awayTeamName'][:8] == "TSV 1860"): awayTeam = "Munich 1860"
        elif (leagueId == "FL2"):
            if (nextGameInfo['homeTeamName'] == "FC Stade Lavallois Mayenne"): homeTeam = "Laval"
            if (nextGameInfo['awayTeamName'] == "FC Stade Lavallois Mayenne"): awayTeam = "Laval"
            if (nextGameInfo['homeTeamName'] == "Chamois Niortais FC"): homeTeam = "Niort"
            if (nextGameInfo['awayTeamName'] == "Chamois Niortais FC"): awayTeam = "Niort"
        elif (leagueId == "SA"):
            if (nextGameInfo['homeTeamName'] == "FC Internazionale Milano"): homeTeam = "Inter"
            if (nextGameInfo['awayTeamName'] == "FC Internazionale Milano"): awayTeam = "Inter"
        elif (leagueId == "SD"):
            if (nextGameInfo['homeTeamName'][:5].startswith("Depor")): homeTeam = "Alaves"
            if (nextGameInfo['awayTeamName'][:5].startswith("Depor")): awayTeam = "Alaves"

        matchDate = nextGameInfo['date'][10]
        matchDateInt = nextGameInfo['date'][2:4]+nextGameInfo['date'][5:7]+nextGameInfo['date'][8:10]
        #print homeTeam,"-",awayTeam,"the",matchDateInt
        #Insert the game in DB
        cur.execute('''
            INSERT INTO NEXTMATCHS(
                HomeTeam,
                AwayTeam,
                MatchDate,
                DateInt)
            VALUES(?,?,?,?)
        ''',
        (homeTeam, awayTeam, matchDate, matchDateInt, ))
        conn.commit()

    conn.commit()
    conn.close()


def createEmptyNextMatchTable(db):

    # Connect to database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE NEXTMATCHS (
        MatchDate DATE,
        DateInt DATE,
        HomeTeam TEXT,
        AwayTeam TEXT
        )
    ''')

    conn.commit()
    conn.close()
