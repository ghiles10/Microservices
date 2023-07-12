import sys 
sys.path.append(r"./")

print('ok 1')

from fastapi import FastAPI, HTTPException, UploadFile,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient

print('ok 2')


from app.mp3_to_text import convert_mp3_to_text 
from utils.validate_login import login

app = FastAPI()
# security = HTTPBasic()



print('------------------------- bientot dans post /convert --------------------------------' )
@app.post("/convert")
async def convert(mp3_file: UploadFile, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):

    """ Convert MP3 to text route and send it to mongoBD database """

    # identification dans l'API
    data_credentials = dict(credentials)
    response = login(data_credentials)

    print('-------------------------verfication login --------------------------------' )

    # Vérifier les informations d'identification
    if not response.status_code == 200 : 
        raise HTTPException(response.status_code,  'probleme authenification')

    #Traiter le fichier MP3

    print('-------------------------dans post /convert --------------------------------' )
    file_converted = await convert_mp3_to_text(mp3_file) 


    print('-------------------------essaye connexion mongo----------------------------')
    #Mongo db connexion
    client = MongoClient("mongodb://mongodb:27017/")

    print('-------------------------dans mongo----------------------------')

    # crée la base de données
    db_text_mp3 = client["mp3_text"]

    # crée une collection
    mp3_text_collection = db_text_mp3["mp3_text_collection"]

    # insertion d'un document pour verifier 
    document = {"key": "value"}
    mp3_text_collection.insert_one(document)

    #  verifier la base de données 
    db_list = client.list_databases()
    
    database_list = []  
    for db_info in list(db_list) : 
        database_list.append(db_info.values()) 
    
    print(database_list)
    
    db_list_finale = []
    for db_values in database_list:
        for value_db in db_values:
            db_list_finale.append(value_db)


    if  "mp3_text" not in db_list_finale :
        raise HTTPException(500,  'la base de données na pas été crée')
    
    # verifier la collection 
    col_list = db_text_mp3.list_collection_names()
    if not "mp3_text_collection" in col_list:
        raise HTTPException(500,  'la collection na pas été crée')
    
    return file_converted




    # mettre le fichier dans mongodb
    # mongo_db.put(file_converted) 

    # file_id = mongo_db.id()
    # return file_id
