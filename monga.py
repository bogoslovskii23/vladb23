import matplotlib.pyplot as plt
from pymongo import mongo_client
import pprint
import time


uri = "mongodb+srv://github_reader:YfeU2PWUqwbiaS16@cryptomood-prod-hxlo9.gcp.mongodb.net/admin?ssl=true&authSource=admin&retryWrites=true&w=majority"


client = mongo_client.MongoClient( "mongodb+srv://github_reader:YfeU2PWUqwbiaS16@cryptomood-prod-hxlo9.gcp.mongodb.net/admin?ssl=true&authSource=admin&retryWrites=true&w=majority"
)

db = client['cryptomood']


collection = db.get_collection('github')
symbols = set()
print("1")
for document in collection.find():
    if document["symbol"] not in symbols:
        symbols.add(document["symbol"])
        sym = document["symbol"]
        print(sym)