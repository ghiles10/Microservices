from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from converter.utils.validate_login import login

app = FastAPI()
security = HTTPBasic()

@app.post("/convert")
def convert(credentials: HTTPBasicCredentials , mp3_file: UploadFile ):


    data_credentials = dict(credentials)
    response = login(data_credentials)

    # Vérifier les informations d'identification
    if not response.status_code == 200 : 
        raise response.raise_for_status()

    # Traiter le fichier MP3
    file_converted = app.convert.function() 
    mongo_db.put(file_converted) 

    file_id = mongo_db.id()
    return file_id
