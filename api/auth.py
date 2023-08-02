import sys
sys.path.append(r"./")

from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasicCredentials

from api.services.user_services import UserService 
from database.conn import get_postgres_connection 
from api.exceptions.exceptions import UserAlreadyExists, UserNotExists
from api.conf import log_conf

app = FastAPI()

# Initialisation de la configuration de logging
logger = log_conf.logger

@app.post("/subscribe")
def subscribe(credentials: HTTPBasicCredentials):

    """ subscribe into service by providing unique username + password """

    if not credentials:
        raise HTTPException(status_code=401, detail="Missing credentials")

    credentials_dict  = dict(credentials)

    user_api_service = UserService(credentials_dict) 

    # cheks subscribe 
    conn_db = get_postgres_connection()

    return user_api_service.subscribe(conn_db) 

@app.post("/login")
def login(credentials: HTTPBasicCredentials): 

    """ login into api with credentials in HTTP request"""

    if not credentials:
        raise HTTPException(status_code=401, detail="Missing credentials") 
    
    credentials_dict  = dict(credentials) 

    # create user service
    user_api_service = UserService(credentials_dict)

    # cheks subscribe 
    conn_db = get_postgres_connection()  
    

    return user_api_service.login(conn_db) 