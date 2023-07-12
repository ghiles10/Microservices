from pymongo import MongoClient
from fastapi import  HTTPException

def create_db(client : MongoClient)  : 

    ''' create mongo db databse and collection and test it '''

    # crée la base de données
    db_text_mp3 = client["mp3_text"]

    # crée une collection
    mp3_text_collection = db_text_mp3["mp3_text_collection"]

    # insertion d'un document 
    document = {"key": "value"}
    mp3_text_collection.insert_one(document)

    #  verifier la base de données 
    db_list = client.list_databases()
    
    db_list_values = [db_info.values() for db_info in db_list]  

    db_list_finale = []
    for db_values in db_list_values:
        for value_db in db_values:
            db_list_finale.append(value_db)


    if "mp3_text" not in db_list_finale :
        raise HTTPException(500,  'la base de données na pas été crée')
    
    # verifier la collection 
    collection_list = db_text_mp3.list_collection_names()
    if not "mp3_text_collection" in collection_list:
        raise HTTPException(500,  'la collection na pas été crée')
    
    return db_text_mp3.mp3_text_collection 