from abc import ABC, abstractmethod
from fastapi import HTTPException
import pymongo 


class DatabaseClient(ABC):

    @abstractmethod
    def get_database(self, name: str):
        pass

class Database(ABC):

    @abstractmethod
    def get_collection(self, name: str):
        pass

class Collection(ABC):

    @abstractmethod
    def insert_one(self, document: dict):
        pass

class PyMongoClient(DatabaseClient):

    def __init__(self, client: pymongo.MongoClient):
        self.client = client
            
    def get_database(self, name: str) -> Database:
        return PyMongoDatabase(self.client[name])

class PyMongoDatabase(Database):
    def __init__(self, db: pymongo.database.Database):
        self.db = db

    def get_collection(self, name: str) -> Collection:
        return PyMongoCollection(self.db[name])

class PyMongoCollection(Collection):
    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection

    def insert_one(self, document: dict):
        self.collection.insert_one(document)

class DbMongo:


    def __init__(self, client: DatabaseClient) -> None:
        
        self.client = client
        self.db = None
        self.collection = None

    def create_db(self, db_name: str = "mp3_text") -> None:
        db_text_mp3 = self.client.get_database(db_name)
        self.db = db_text_mp3
        return self

    def create_collection(self, collection_name: str = "mp3_text_collection") -> None:
        mp3_text_collection = self.db.get_collection(collection_name)
        self.collection = mp3_text_collection
        return self

    def insert_test_document(self) -> None:
        try:
            self.collection.insert_one({"key": "value"})
            return None
        except Exception:
            raise HTTPException(500, 'la collection na pas été crée')

    def check_db(self) -> None:
        db_list = self.client.list_database_names()
        if "mp3_text" not in db_list:
            raise HTTPException(500, 'la base de données na pas été crée')

    def check_collection(self) -> None:
        collection_list = self.db.list_collection_names()
        if not "mp3_text_collection" in collection_list:
            raise HTTPException(500, 'la collection na pas été crée')
