import sys 
sys.path.append(r"./")

from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime
from bson.objectid import ObjectId
import json

from app.mp3_to_text import convert_mp3_to_text 
from utils.validate_login import login
from utils.conn_mongodb import get_client_mongodb
from app.mongodb_check import create_db

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
    client = get_client_mongodb()

    print('-------------------------dans mongo----------------------------')

    # cheks health mongo db
    try : 
        db_mongodb = create_db(client)

    except Exception :
        raise HTTPException(status_code=500 , detail="Error in mongo db connexion")
    

    # mettre le fichier dans mongodb
    result = db_mongodb.insert_one({
                                    "text": str(file_converted) , 
                                    "username": str(credentials.username) ,
                                    "date": str( datetime.datetime.now() ) ,
                                    "file_name": str (mp3_file.filename )
                                    }) 

    print(f' ----------------- result insertion : { result.inserted_id } --------------------------')

    document  = db_mongodb.find_one({"_id": ObjectId(result.inserted_id)} , {"_id": 0})

    return document


