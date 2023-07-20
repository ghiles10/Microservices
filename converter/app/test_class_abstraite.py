import pymongo 
from fastapi import  HTTPException 
from abc import ABC, abstractmethod 


# creating interfaces for database & collections 

class DatabaseClient(ABC) : 

    """ in order to create an interface that allows you to oversee the creation of a database. """

    @abstractmethod 
    def create_db(self, name : str) :
        pass 


class UseDatabase(ABC) :

    """ creates a database client for the purpose of manipulating data structures """

    @abstractmethod 
    def create_data_structure(self , collection_name : str ) : 
        pass 


class UseDataStructure(ABC) : 

    """  creates record for testing purpose """


    @abstractmethod 
    def add_test_record(self, document : dict ) : 
        pass


# create class that inherate from interfaces

class PyMongoClientDatabase(DatabaseClient) : 

    def __init__(self, client: pymongo.MongoClient ) -> None:

        self.mongo_client  = client

    def create_db(self, name : str) : 

        print('-------------------------base créee !!---------------------------')
        return PyMongoUseDatabase( self.mongo_client[name] ) 
    

class PyMongoUseDatabase(UseDatabase) : 
    
    def __init__(self, database : pymongo.database.Database ) -> None:
        self.database_mongodb =  database

    def create_data_structure(self, collection_name ) : 

        mp3_text_collection = self.database_mongodb[ collection_name ] 

        return PyMongoUseCollection(mp3_text_collection)
    
    
class PyMongoUseCollection(UseDataStructure) : 

    def __init__(self, collection: pymongo.collection.Collection) -> None:
        
        self.collection = collection 

    def add_test_record(self, document  ) :

        self.collection.insert_one(document) 
        


# main class 

class DbMongo : 
    """ this class create a database and a collection test in mongo db"""


    def __init__(self, client : DatabaseClient ) :
        
        self.client = client 
        self.db = None
        self.collection = None

        

    def create_db(self, db_name :str = "mp3_text")   : 
        ''' create mongo db database''' 
        print('-------------------------dans create_db----------------------------')
        self.db = self.client.create_db(db_name)
        print('-------------------------dans create_db fait----------------------------')
        return self  
    
    def create_collection(self ,collection_name : str = "mp3_text_collection")  : 
        ''' create a test collection in mongo db database '''
        print('-------------------------dans create_collection----------------------------')
        self.collection = self.db.create_data_structure(collection_name) 


        return self

    def insert_test_document(self )  :
        ''' insert a test document in a collection '''
        print('-------------------------dans insert_test_document----------------------------')
        try :
            self.collection.add_test_record({"key": "value"})  
            return None 
        
        except Exception  :
            raise HTTPException(500,  'la collection na pas été crée') 
        

    def check_db(self ) : 
        ''' check if the database is created '''
        print('-------------------------dans check_db----------------------------')
        db_list = self.client.mongo_client.list_databases()
        
        db_list_values = [db_info.values() for db_info in db_list]  

        db_list_finale = []
        for db_values in db_list_values:
            for value_db in db_values:
                db_list_finale.append(value_db)


        if "mp3_text" not in db_list_finale :
            raise HTTPException(500,  'la base de données na pas été crée')
    
    
    def check_collection(self )  :
        print('-------------------------dans check_collection ----------------------------')
        ''' check if the collection is created '''

        collection_list = self.db.list_collection_names()
        if not "mp3_text_collection" in collection_list:
            raise HTTPException(500,  'la collection na pas été crée') 
        print('-------------------------fin check_collection----------------------------')

    def check_db_health(self ) : 
        ''' check if the database and collection are created '''

        self.create_db().check_db()
        self.create_collection().check_collection()
        self.insert_test_document()
        
    
