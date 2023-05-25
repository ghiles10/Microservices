import sys
sys.path.append(r"./")

from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasicCredentials

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

    username = credentials.username
    password = credentials.password

    # vérification des informations d'authentification 
    
    conn_db = get_postgres_connection() 

    with conn_db.cursor() as cur: 

        try:
            cur.execute( " INSERT INTO users (username, password) VALUES (%s, %s) "  ,          
            ( username , password )  
            )

        except : 
            logger.error( 'error in writing sql query subscribe' )
            raise HTTPException(status_code=500, detail = 'Error in Database' )

        # cheks query
        affected_rows = cur.rowcount
        if affected_rows < 1 : 
            
            logger.error('no rows affected')
            raise HTTPException(status_code=401  , detail = f"erreur insertion username : {username}") 
        
        # # test requete
        # cur.execute("SELECT * FROM users;")
        # resultat_requete = cur.fetchone()

        conn_db.commit()

        return {f"message: {username} subscribe"}


@app.post("/login")
def login(credentials: HTTPBasicCredentials): 

    """ login into api with credentials in HTTP request"""

    if not credentials:
        raise HTTPException(status_code=401, detail="Missing credentials") 
    
    # cheks subscribe 
    conn_db = get_postgres_connection()  
    with conn_db.cursor() as cur: 

        try : 
            cur.execute(f"SELECT username FROM users where username = '{credentials.username}'") 

        except:
            logger.error("error in database when retreiving username", {credentials.username}) 
            raise HTTPException(status_code=500, detail="Error in database")

        if not cur.fetchone() : 
            logger.error(f" User {credentials.username} Not Exists ")
            raise HTTPException( status_code=401, detail=f"Username {credentials.username} Invalid" ) 
    
    return {f"User {credentials.username} Logged"}