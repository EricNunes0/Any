import pymongo
from mongoconnection.connect import getDatabase

def createNewAfk(userId, active, reason, time):
    dbname = getDatabase()
    collectionName = dbname["afk"]
    if reason == None:
        reason = "Não informado"
    newAfk = {
        "userId": userId,
        "active": active,
        "reason": reason,
        "time": time
    }
    collectionName.insert_one(newAfk)

async def searchForAfk(message):
    try:
        dbname = getDatabase()
        collectionName = dbname["afk"]
        afkUsers = collectionName.find({})
        for afkUser in afkUsers:
            if int(message.author.id) == int(afkUser["userId"]):
                if afkUser["active"] == True:
                    collectionName.find_one_and_update({"userId": message.author.id}, {"$set": {"active": False, "reason": "Não informado"}}, return_document = pymongo.ReturnDocument.AFTER)
                    return 0
            elif f"<@{afkUser['userId']}>" in message.content:
                if afkUser["active"] == True:
                    return afkUser["reason"]
            else:
                if message.reference != None:
                    repliedMsg = await message.channel.fetch_message(message.reference.message_id)
                    if int(repliedMsg.author.id) == int(afkUser["userId"]):
                        if afkUser["active"] == True:
                            return afkUser["reason"]
        return 1
    except Exception as e:
        print(e)

async def reactionSearchForAfk(userId):
    try:
        print(userId)
        dbname = getDatabase()
        collectionName = dbname["afk"]
        foundProfile = collectionName.find_one({"userId": userId})
        if foundProfile == None:
            print("reactionSearchForAfk() -> profile not found")
            return 0
        if foundProfile["active"] == True:
            collectionName.find_one_and_update({"userId": userId}, {"$set": {"active": False}}, return_document = pymongo.ReturnDocument.AFTER)
            return 1
        return 0
    except Exception as e:
        print(e)


def findOneAfkAndUpdate(userId, active, reason, time):
    dbname = getDatabase()
    collectionName = dbname["afk"]
    if reason == None:
        reason = "Não informado"
    foundProfile = collectionName.find_one({"userId": userId})
    if foundProfile == None:
        createNewAfk(userId, active, reason, time)
    else:
        collectionName.find_one_and_update({"userId": userId}, {"$set": {"active": active, "reason": reason, "time": time}}, return_document = pymongo.ReturnDocument.AFTER)

def disableAfk(userId):
    dbname = getDatabase()
    collectionName = dbname["afk"]
    foundProfile = collectionName.find_one({"userId": userId})
    if foundProfile == None:
        print("disableAfk() - Usuário não encontrado: ", userId)
        return
    else:
        print("disableAfk() - Usuário encontrado: ", userId)
        collectionName.find_one_and_update({"userId": userId}, {"$set": {"active": False}}, return_document = pymongo.ReturnDocument.AFTER)