import pymongo
from mongoconnection.connect import getDatabase
import asyncio

def createTicketStats():
    try:
        dbname = getDatabase()
        collectionName = dbname["ticket"]
        ticketStats = {
            "Id": 1,
            "Total": 0,
            "Vips": 0,
            "VipAmetista": 0,
            "VipJade": 0,
            "VipSafira": 0,
            "Boost": 0,
            "Patrocinio": 0,
        }
        newStats = collectionName.insert_one(ticketStats)
        return newStats
    except Exception as e:
        print(e)

def getTicketVipStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    ticketStats = collectionName.find_one({"Id": 1})
    return ticketStats

def updateTicketVipAmetistaStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$inc": {"VipAmetista": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def updateTicketVipJadeStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$inc": {"VipJade": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def updateTicketVipSaphireStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$inc": {"VipSafira": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def updateTicketBoosterStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$inc": {"Boost": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def updateTicketPatrocinioStats():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$inc": {"Patrocinio": 1}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def setVipAmetistaStats(i):
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    updatedStats = collectionName.find_one_and_update({"Id": 1}, {"$set": {"VipAmetista": int(i)}}, return_document = pymongo.ReturnDocument.AFTER)
    updateTicketStatsTotal()
    return updatedStats

def updateTicketStatsTotal():
    dbname = getDatabase()
    collectionName = dbname["ticket"]
    foundProfile = collectionName.find_one({"Id": 1})
    vipAmetista = int(foundProfile["VipAmetista"])
    vipJade = int(foundProfile["VipJade"])
    vipSafira = int(foundProfile["VipSafira"])
    boosts = int(foundProfile["Boost"])
    patrocinios = int(foundProfile["Patrocinio"])
    collectionName.find_one_and_update({"Id": 1}, {"$set": {"Vips": vipAmetista + vipJade + vipSafira, "Total": vipAmetista + vipJade + vipSafira + boosts + patrocinios}}, return_document = pymongo.ReturnDocument.AFTER)