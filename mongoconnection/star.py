import pymongo
from mongoconnection.connect import getDatabase

def createNewStar(userId):
    dbname = getDatabase()
    collectionName = dbname["star"]
    newAfk = {
        "userId": userId,
        "total": 0,
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
    updateStarTotal(userId)
    return foundProfile

def updateStar(userId, star):
    dbname = getDatabase()
    collectionName = dbname["star"]
    foundProfile = collectionName.find_one({"userId": userId})
    if foundProfile == None:
        createNewStar(userId)
    updatedProfile = collectionName.find_one_and_update({"userId": userId}, {"$inc": {f"stars.{star}": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateStarTotal(userId)
    return updatedProfile

def updateStarTotal(userId):
    dbname = getDatabase()
    collectionName = dbname["star"]
    foundProfile = collectionName.find_one({"userId": userId})
    star0 = int(foundProfile["stars"]["0"])
    star1 = int(foundProfile["stars"]["1"])
    star2 = int(foundProfile["stars"]["2"])
    star3 = int(foundProfile["stars"]["3"])
    star4 = int(foundProfile["stars"]["4"])
    collectionName.find_one_and_update({"userId": userId}, {"$set": {"total": star0 + star1 + star2 + star3 + star4}}, return_document = pymongo.ReturnDocument.AFTER)

def getAllStars():
    dbname = getDatabase()
    collectionName = dbname["star"]
    foundProfiles = collectionName.find().sort("total", -1)
    allProfiles = list(foundProfiles)
    for profile in allProfiles:
        updateStarTotal(profile["userId"])
    return allProfiles
