import sys
sys.path.append(r"./")

from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database.conn import get_postgres_connection 
from api.exceptions.exceptions import UserAlreadyExists 

app = FastAPI()


@app.post("/subscribe")
def login(credentials: HTTPBasicCredentials):

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


        except Exception as e : 
            print('*' * 1000)
            print(e)
            print( type( ( username, password ) ))

        affected_rows = cur.rowcount
        if affected_rows < 1 : 
            print('-' * 1000)

        cur.execute( " SELECT * FROM users " ) 

        
        

        return {f"message: {cur.fetchall()}"}




