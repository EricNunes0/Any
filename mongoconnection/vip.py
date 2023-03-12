import pymongo
from mongoconnection.connect import getDatabase
import asyncio

def createNewVip(userId, vip, duration, channel):
    dbname = getDatabase()
    collectionName = dbname["vip"]
    newVip = {
        "userId": userId,
        "Vip": vip,
        "Duration": duration,
        "Channel": channel
    }
    newProfile = collectionName.insert_one(newVip)
    return newProfile