import os
import dotenv
import pymongo

dotenv.load_dotenv()
MONGO_TOKEN = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_TOKEN)

def getDatabase():
    return client["any_bot"]

if __name__ == "__main__":
   dbname = getDatabase()