from pymongo import MongoClient

def get_client_mongodb() :

    """ connect to mongo db client"""

    client = MongoClient("mongodb://mongodb:27017/")
    return client 