import os 

import psycopg2
from psycopg2.extensions import connection


HOST = os.environ.get('POSTGRES_HOST', 'postgresdb') 
PORT = os.environ.get('POSTGRES_PORT', '5432')
DBNAME = os.environ.get('POSTGRES_DBN', 'postgres')
USER = os.environ.get('POSTGRES_USER', 'postgres') 
PASSWORD = os.environ.get('POSTGRES_PASSWORD' , 'postgres') 

def get_postgres_connection( host = HOST, port = PORT,
                            dbname= DBNAME, user = USER, password = PASSWORD ) -> connection : 

    """ get posstgres connection object  """

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    return conn

