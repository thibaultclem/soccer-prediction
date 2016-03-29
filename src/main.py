from soccerPrediction import *

# General
deepGameLimit = 5

# Fench Ligue 1
l1db = "./data/db/ligue1.sqlite"
l1Teams = "./data/result/l1-teams.csv"
l1csvRawData = "./data/raw/F1.csv"
l1csvDataModel = "./data/result/l1-data-model.csv"
l1csvDataPredict = "./data/result/l1-data-predict.csv"
l1StartDate = "150918"

extractFromCsv(l1csvRawData,l1db)
createHistoricSeasonTable(l1db)
createDataModelTable(l1db,deepGameLimit,l1StartDate)
exportDataModelToCsv(l1csvDataModel,l1db)
exportTeamsToCSV(l1Teams,l1db)
createDataPredictTable(l1db, deepGameLimit)
exportDataPredictToCsv(l1csvDataPredict,l1db)


# English Championship
e1db = "./data/db/e1.sqlite"
e1Teams = "./data/result/e1-teams.csv"
e1csvRawData = "./data/raw/E1.csv"
e1csvDataModel = "./data/result/e1-data-model.csv"
e1csvDataPredict = "./data/result/e1-data-predict.csv"
e1StartDate = "150829"

extractFromCsv(e1csvRawData,e1db)
createHistoricSeasonTable(e1db)
createDataModelTable(e1db,deepGameLimit,e1StartDate)
exportDataModelToCsv(e1csvDataModel,e1db)
exportTeamsToCSV(e1Teams,e1db)
createDataPredictTable(e1db, deepGameLimit)
exportDataPredictToCsv(e1csvDataPredict,e1db)


# English Premier League
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
