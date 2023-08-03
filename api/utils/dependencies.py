from fastapi import HTTPException
from fastapi.security import  HTTPBasicCredentials
from api.services.user_services import UserService 
from database.conn import get_postgres_connection 


# injection dependance 
def get_api_user_service(credentials : HTTPBasicCredentials) -> UserService: 

    """ get user service class"""

    if not credentials : 
        raise HTTPException(status_code=401, detail="Missing credentials")

    credentials_dict  = dict(credentials)

    return UserService(credentials_dict) 


def get_db_connexion() : 

    """ get postgres connexion"""

    return get_postgres_connection()