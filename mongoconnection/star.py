import pymongo
from mongoconnection.connect import getDatabase

def createNewStar(userId):
    dbname = getDatabase()
    collectionName = dbname["star"]
    newAfk = {
        "userId": userId,
        "stars": {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0
        }
    }
    newProfile = collectionName.insert_one(newAfk)
    return newProfile

def getStar(userId):
    dbname = getDatabase()
    collectionName = dbname["star"]
    foundProfile = collectionName.find_one({"userId": userId})
    if foundProfile == None:
        foundProfile = createNewStar(userId)
    return foundProfile

def updateStar(userId, star):
    dbname = getDatabase()
    collectionName = dbname["star"]
    foundProfile = collectionName.find_one({"userId": userId})
    if foundProfile == None:
        createNewStar(userId)
    collectionName.find_one_and_update({"userId": userId}, {"$inc": {f"stars.{star}": 1}}, return_document = pymongo.ReturnDocument.AFTER)