import os 
import sys 
sys.path.append(r'./' )

from psycopg2.extensions import connection

from database.conn import get_postgres_connection 


conn_db = get_postgres_connection() 

def create_table( conn: connection = conn_db ) -> None : 

    """ create table for user registration """

    with conn.cursor() as cur:

        cur.execute( """
            CREATE TABLE IF NOT EXISTS users (
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                username VARCHAR(20) NOT NULL,
                password VARCHAR NOT NULL );
                    """
                )

        conn.commit()

if __name__ == "__main__" : 

    create_table(conn = conn_db)