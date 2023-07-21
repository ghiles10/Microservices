import sys 
sys.path.append(r"./")

from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime
from bson.objectid import ObjectId

from app.mp3_to_text import convert_mp3_to_text 
from utils.validate_login import login
from utils.conn_mongodb import get_client_mongodb
from app.mongodb_user import DbMongo, PyMongoClientDatabase
from conf.log_conf import setup_logger



logger = setup_logger(__name__)

app = FastAPI()


@app.post("/convert")
async def convert(mp3_file: UploadFile, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):

    """ Convert MP3 to text route and send it to mongoBD database """

    # identification dans l'API
    data_credentials = dict(credentials)
    response = login(data_credentials)

    logger.info(f"credentials user : {data_credentials}")
    logger.info(f"response status code for login : {response.status_code}")

    # Vérifier les informations d'identification
    if not response.status_code == 200 : 
        raise HTTPException(response.status_code,  'probleme authenification')

    #Traiter le fichier MP3

    file_converted = await convert_mp3_to_text(mp3_file) 
    logger.info("MP3 file is converted to text")


    #Mongo db connexion
    client = get_client_mongodb()
    logger.info("MongoDB client is connected")

    client_test = PyMongoClientDatabase(client)
    logger.info("MongoDB client is connected to database interface")

    # cheks health mongo db
    db_mongodb = DbMongo(client_test)
    db_mongodb.check_db_health()
    
    logger.info("MongoDB database is connected, health OK")
    

    # mettre le fichier dans mongodb
    result = db_mongodb.insert_test_document({
                                    "text": str(file_converted) , 
                                    "username": str(credentials.username) ,
                                    "date": str( datetime.datetime.now() ) ,
                                    "file_name": str (mp3_file.filename )
                                    }) 

    logger.info(f' file inserted ok with ID : { result.inserted_id } ')

    document  = db_mongodb.collection_db.collection.find_one({"_id": ObjectId(result.inserted_id)} , {"_id": 0})
    logger.info(f' document found in collection with ID : { result.inserted_id } ')

    return document


