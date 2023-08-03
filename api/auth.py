import sys
sys.path.append(r"./")

from fastapi import Depends, FastAPI
from api.services.user_services import UserService 
from api.utils.dependencies import get_api_user_service, get_db_connexion
from api.conf import log_conf


# Initialisation de la configuration de logging
logger = log_conf.logger

app = FastAPI()                       
                                                                  
@app.post("/subscribe")
def subscribe(user_api_service : UserService = Depends(get_api_user_service), conn_db = Depends(get_db_connexion)):

    """ subscribe into service by providing unique username + password """

    return user_api_service.subscribe(conn_db) 


@app.post("/login")
def login(user_api_service : UserService = Depends(get_api_user_service) , conn_db = Depends(get_db_connexion)): 

    """ login into api with credentials in HTTP request"""
    
    return user_api_service.login(conn_db) 