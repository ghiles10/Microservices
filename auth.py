from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database.conn import get_postgres_connection 

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
        cur.execute( f""" 
        INSERT INTO users (username, password) VALUES ('{username}', '{password}');
         """ ) 

        affected_rows = cur.rowcount
        if affected_rows < 1: 
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        row = cur.execute(""" SELECT * FROM users """)
        row = cur.fetchone() 
            

    return {f"message: {row}"}




