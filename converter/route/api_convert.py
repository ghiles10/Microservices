import sys 
sys.path.append(r"./")

print('ok 1')

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient

print('ok 2')


from app.mp3_to_text import convert_mp3_to_text 
from utils.validate_login import login

app = FastAPI()
# security = HTTPBasic()

print('------------------------- bientot dans post /convert --------------------------------' )
@app.post("/convert")
async def convert( mp3_file: UploadFile, credentials: dict  ):

    """ Convert MP3 to text route and send it to mongoBD database """

    # identification dans l'API
    # data_credentials = dict(credentials)
    response = login(credentials)

    # Vérifier les informations d'identification
    if not response.status_code == 200 : 
        raise response.raise_for_status()

    #Traiter le fichier MP3

    print('------------------------- dans post /convert --------------------------------' )
    file_converted = await convert_mp3_to_text(mp3_file) 

    #Mongo db connexion
    client = MongoClient("mongodb://mongodb:27017/")

    print('-------------------------------dans mongo----------------------------')

    # crée la base de données
    db_text_mp3 = client["mp3_text"]

    # crée une collection
    mp3_text_collection = db_text_mp3["mp3_text_collection"]

    # # verifier la base de données 
    db_list = client.list_database_names()
    if not "mp3_text" in db_list :
        raise HTTPException(500,  'la base de données na pas été crée')
    
    # verifier la collection 
    col_list = client.list_collection_names()
    if not "mp3_text_collection" in col_list:
        raise HTTPException(500,  'la collection na pas été crée')
    
    return file_converted




    # mettre le fichier dans mongodb
    # mongo_db.put(file_converted) 

    # file_id = mongo_db.id()
    # return file_id
