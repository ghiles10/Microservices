from pymongo import MongoClient
from fastapi import  HTTPException 
from pymongo.database import Database
from pymongo.collection import Collection

class DbMongo() : 
    """ this class create a database and a collection test in mongo db"""


    def __init__(self, client : MongoClient ) -> None:
        
        self.client = client 
        self.db = None
        self.collection = None

    def create_db(self, db_name :str = "mp3_text") -> None  : 
        ''' create mongo db database''' 

        db_text_mp3 = self.client[ db_name ] 

        # modify databse attribue 
        self.db = db_text_mp3 

        return self  
    
    def create_collection(self ,collection_name : str = "mp3_text_collection") -> None : 
        ''' create a test collection in mongo db database '''

        mp3_text_collection = self.db[ collection_name ] 
        self.collection = mp3_text_collection

        return self

    def insert_test_document(self ) -> None :
        ''' insert a test document in a collection '''

        try :
            self.collection.insert_one({"key": "value"})  
            return None 
        
        except Exception  :
            raise HTTPException(500,  'la collection na pas été crée') 
        

    def check_db(self ) -> None: 
        ''' check if the database is created '''

        db_list = self.client.list_databases()
        
        db_list_values = [db_info.values() for db_info in db_list]  

        db_list_finale = []
        for db_values in db_list_values:
            for value_db in db_values:
                db_list_finale.append(value_db)


        if "mp3_text" not in db_list_finale :
            raise HTTPException(500,  'la base de données na pas été crée')
    
    
    def check_collection(self ) -> None :

        ''' check if the collection is created '''

        collection_list = self.db.list_collection_names()
        if not "mp3_text_collection" in collection_list:
            raise HTTPException(500,  'la collection na pas été crée') 
        

    
    
