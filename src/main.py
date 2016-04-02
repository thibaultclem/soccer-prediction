from soccerPrediction import *

# General
deepGameLimit = 5

# Fench Ligue 1
l1db = "./data/db/f1.sqlite"
l1Teams = "./data/result/f1-teams.csv"
l1csvRawData = "./data/raw/F1.csv"
l1csvDataModel = "./data/result/f1-data-model.csv"
l1csvDataPredict = "./data/result/f1-data-predict.csv"
l1StartDate = "150918"

extractFromCsv(l1csvRawData,l1db)
createHistoricSeasonTable(l1db)
createDataModelTable(l1db,deepGameLimit,l1StartDate)
exportDataModelToCsv(l1csvDataModel,l1db)
exportTeamsToCSV(l1Teams,l1db)
createDataPredictTable(l1db, deepGameLimit)
exportDataPredictToCsv(l1csvDataPredict,l1db)

# French Ligue 2
f2db = "./data/db/f2.sqlite"
f2Teams = "./data/result/f2-teams.csv"
f2csvRawData = "./data/raw/F2.csv"
f2csvDataModel = "./data/result/f2-data-model.csv"
f2csvDataPredict = "./data/result/f2-data-predict.csv"
f2StartDate = "150815"

extractFromCsv(f2csvRawData,f2db)
createHistoricSeasonTable(f2db)
createDataModelTable(f2db,deepGameLimit,f2StartDate)
exportDataModelToCsv(f2csvDataModel,f2db)
exportTeamsToCSV(f2Teams,f2db)
createDataPredictTable(f2db, deepGameLimit)
exportDataPredictToCsv(f2csvDataPredict,f2db)


# English Ligue 1
e0db = "./data/db/e0.sqlite"
e0Teams = "./data/result/e0-teams.csv"
e0csvRawData = "./data/raw/e0.csv"
e0csvDataModel = "./data/result/e0-data-model.csv"
e0csvDataPredict = "./data/result/e0-data-predict.csv"
e0StartDate = "150919"

extractFromCsv(e0csvRawData,e0db)
createHistoricSeasonTable(e0db)
createDataModelTable(e0db,deepGameLimit,e0StartDate)
exportDataModelToCsv(e0csvDataModel,e0db)
exportTeamsToCSV(e0Teams,e0db)
createDataPredictTable(e0db, deepGameLimit)
exportDataPredictToCsv(e0csvDataPredict,e0db)

# English Ligue 2
e1db = "./data/db/e1.sqlite"
e1Teams = "./data/result/e1-teams.csv"
e1csvRawData = "./data/raw/E1.csv"
e1csvDataModel = "./data/result/e1-data-model.csv"
e1csvDataPredict = "./data/result/e1-data-predict.csv"
e1StartDate = "150911"

extractFromCsv(e1csvRawData,e1db)
createHistoricSeasonTable(e1db)
createDataModelTable(e1db,deepGameLimit,e1StartDate)
exportDataModelToCsv(e1csvDataModel,e1db)
exportTeamsToCSV(e1Teams,e1db)
createDataPredictTable(e1db, deepGameLimit)
exportDataPredictToCsv(e1csvDataPredict,e1db)


# Italia Ligue 1
i1db = "./data/db/i1.sqlite"
i1Teams = "./data/result/i1-teams.csv"
i1csvRawData = "./data/raw/I1.csv"
i1csvDataModel = "./data/result/i1-data-model.csv"
i1csvDataPredict = "./data/result/i1-data-predict.csv"
i1StartDate = "150926"

#extractFromCsv(i1csvRawData,i1db)
#createHistoricSeasonTable(i1db)
#createDataModelTable(i1db,deepGameLimit,i1StartDate)
#exportDataModelToCsv(i1csvDataModel,i1db)
#exportTeamsToCSV(i1Teams,i1db)
#createDataPredictTable(i1db, deepGameLimit)
#exportDataPredictToCsv(i1csvDataPredict,i1db)

# Italia Ligue 2
i2db = "./data/db/i2.sqlite"
i2Teams = "./data/result/i2-teams.csv"
i2csvRawData = "./data/raw/I2.csv"
i2csvDataModel = "./data/result/i2-data-model.csv"
i2csvDataPredict = "./data/result/i2-data-predict.csv"
i2StartDate = "151002"

extractFromCsv(i2csvRawData,i2db)
createHistoricSeasonTable(i2db)
createDataModelTable(i2db,deepGameLimit,i2StartDate)
exportDataModelToCsv(i2csvDataModel,i2db)
exportTeamsToCSV(i2Teams,i2db)
createDataPredictTable(i2db, deepGameLimit)
exportDataPredictToCsv(i2csvDataPredict,i2db)


# Deutch Ligue 1
d1db = "./data/db/d1.sqlite"
d1Teams = "./data/result/d1-teams.csv"
d1csvRawData = "./data/raw/D1.csv"
d1csvDataModel = "./data/result/d1-data-model.csv"
d1csvDataPredict = "./data/result/d1-data-predict.csv"
d1StartDate = "150922"

extractFromCsv(d1csvRawData,d1db)
createHistoricSeasonTable(d1db)
createDataModelTable(d1db,deepGameLimit,d1StartDate)
exportDataModelToCsv(d1csvDataModel,d1db)
exportTeamsToCSV(d1Teams,d1db)
createDataPredictTable(d1db, deepGameLimit)
exportDataPredictToCsv(d1csvDataPredict,d1db)

# Deutch Ligue 2
d2db = "./data/db/d2.sqlite"
d2Teams = "./data/result/d2-teams.csv"
d2csvRawData = "./data/raw/D2.csv"
d2csvDataModel = "./data/result/d2-data-model.csv"
d2csvDataPredict = "./data/result/d2-data-predict.csv"
d2StartDate = "150911"

extractFromCsv(d2csvRawData,d2db)
createHistoricSeasonTable(d2db)
createDataModelTable(d2db,deepGameLimit,d2StartDate)
exportDataModelToCsv(d2csvDataModel,d2db)
exportTeamsToCSV(d2Teams,d2db)
createDataPredictTable(d2db, deepGameLimit)
exportDataPredictToCsv(d2csvDataPredict,d2db)


# Spain Ligue 1
sp1db = "./data/db/sp1.sqlite"
sp1Teams = "./data/result/sp1-teams.csv"
sp1csvRawData = "./data/raw/SP1.csv"
sp1csvDataModel = "./data/result/sp1-data-model.csv"
sp1csvDataPredict = "./data/result/sp1-data-predict.csv"
sp1StartDate = "150924"

#extractFromCsv(sp1csvRawData,sp1db)
#createHistoricSeasonTable(sp1db)
#createDataModelTable(sp1db,deepGameLimit,sp1StartDate)
#exportDataModelToCsv(sp1csvDataModel,sp1db)
#exportTeamsToCSV(sp1Teams,sp1db)
#createDataPredictTable(sp1db, deepGameLimit)
#exportDataPredictToCsv(sp1csvDataPredict,sp1db)

# Spain Ligue 2
sp2db = "./data/db/sp2.sqlite"
sp2Teams = "./data/result/sp2-teams.csv"
sp2csvRawData = "./data/raw/SP2.csv"
sp2csvDataModel = "./data/result/sp2-data-model.csv"
sp2csvDataPredict = "./data/result/sp2-data-predict.csv"
sp2StartDate = "150926"

extractFromCsv(sp2csvRawData,sp2db)
createHistoricSeasonTable(sp2db)
createDataModelTable(sp2db,deepGameLimit,sp2StartDate)
exportDataModelToCsv(sp2csvDataModel,sp2db)
exportTeamsToCSV(sp2Teams,sp2db)
createDataPredictTable(sp2db, deepGameLimit)
exportDataPredictToCsv(sp2csvDataPredict,sp2db)

def prepareNextGame():
    createNextMatchTable(l1db)
    createNextMatchTable(f2db)
    createNextMatchTable(e0db)
    createNextMatchTable(e1db)
    createNextMatchTable(d1db)
    createNextMatchTable(d2db)
    createNextMatchTable(i2db)
    createNextMatchTable(sp2db)

# Uncomment to prepare nextgame
#prepareNextGame()
