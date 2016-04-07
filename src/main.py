from soccerPrediction import *

# To modify if needed
deepGameLimit = 5
season = "2015"


def processLeague(leagueId,leagueApiId,starDate):

    db = "./data/db/"+leagueId+".sqlite"
    teams = "./data/result/"+leagueId+"-teams.csv"
    csvDataModel = "./data/result/"+leagueId+"-data-model.csv"
    csvDataModelWithBet = "./data/result/"+leagueId+"-data-model-bet.csv"
    csvDataPredict = "./data/result/"+leagueId+"-data-predict.csv"

    extractFromWebSite(leagueId,season,db)
    createHistoricSeasonTable(db)
    createDataModelTable(db,deepGameLimit,starDate)
    exportDataModelToCsv(csvDataModel,db)
    exportDataModelWithBetToCsv(csvDataModelWithBet,db)
    createNextMatchTable(season,leagueApiId,db)
    createDataPredictTable(db, deepGameLimit)
    exportDataPredictToCsv(csvDataPredict,db)

# Fench Ligue 1
#processLeague('F1','FL1',"150918")
# Fench Ligue 2
processLeague('F2','FL2',"150815")
# English Ligue 1
processLeague('E0','PL',"150919")
# Deutchsland Ligue 1
processLeague('D1','BL1',"150922")
# Deutchsland Ligue 2
processLeague('D2','BL2',"150911")
# Spain Ligue 1
#processLeague('SP1','PD',"150924")
# Spain Ligue 2
processLeague('SP2','SD',"150926")
# Italia Ligue 1
#processLeague('I1','SA',"150926")
# Portuguese Ligue 1
#processLeague('P1','PPL',"150925")
# Netherlands Ligue 1
processLeague('N1','DED',"150918")







########
# Manual league (to delete..?) :
########

# English Ligue 2
e1db = "./data/db/e1.sqlite"
e1Teams = "./data/result/e1-teams.csv"
e1csvRawData = "./data/raw/E1.csv"
e1csvDataModel = "./data/result/e1-data-model.csv"
e1csvDataPredict = "./data/result/e1-data-predict.csv"
e1StartDate = "150911"

#extractFromCsv(e1csvRawData,e1db)
extractFromWebSite("E1",season,e1db)
createHistoricSeasonTable(e1db)
createDataModelTable(e1db,deepGameLimit,e1StartDate)
exportDataModelToCsv(e1csvDataModel,e1db)
exportTeamsToCSV(e1Teams,e1db)
#createDataPredictTable(e1db, deepGameLimit)
#exportDataPredictToCsv(e1csvDataPredict,e1db)

# Italia Ligue 2
i2db = "./data/db/i2.sqlite"
i2Teams = "./data/result/i2-teams.csv"
i2csvRawData = "./data/raw/I2.csv"
i2csvDataModel = "./data/result/i2-data-model.csv"
i2csvDataPredict = "./data/result/i2-data-predict.csv"
i2StartDate = "151002"

#extractFromCsv(i2csvRawData,i2db)
extractFromWebSite("I2",season,i2db)
createHistoricSeasonTable(i2db)
createDataModelTable(i2db,deepGameLimit,i2StartDate)
exportDataModelToCsv(i2csvDataModel,i2db)
exportTeamsToCSV(i2Teams,i2db)
#createDataPredictTable(i2db, deepGameLimit)
#exportDataPredictToCsv(i2csvDataPredict,i2db)


# Some league need manual enter for next match because not available online:
def prepareNextGame():
    createNextMatchTable(e1db)
    createNextMatchTable(i2db)

# Uncomment to prepare next match (erase current row in NEXTMATCHS table)
prepareNextGame()
