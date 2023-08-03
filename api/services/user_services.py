from psycopg2.extensions import connection
from api.conf import log_conf
from api.exceptions.exceptions import UserAlreadyExists, UserNotExists, DatabaseConnectionError 

logger = log_conf.logger

class UserService:
    """ this class is used to manage acces for the users services of the api """

    # count the number of visitors api 
    nb_visitors = 0 


    def __init__(self, credentials: dict): 
        self.__username = credentials['username']
        self.__password = credentials['password']
        UserService.nb_visitors += 1 

    def subscribe(self, conn_db: connection):  
        with conn_db:
            with conn_db.cursor() as cur: 
                try:

                    # Insert new user into the database
                    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (self.__username, self.__password))
                    affected_rows = cur.rowcount
                    if affected_rows < 1 : 
                        logger.error('no rows affected')
                        conn_db.rollback()
                        raise DatabaseConnectionError()
                    conn_db.commit() 

                except : 

                    logger.error('user already exists')
                    conn_db.rollback()
                    raise UserAlreadyExists(self.__username)
                

        return {f"message: {self.__username} subscribe"}


    def login(self, conn_db: connection): 

        with conn_db:   
            # Check if user exists in the database
            with conn_db.cursor() as cur: 

                try : 

                    cur.execute("SELECT username FROM users where username = %s and password = %s", (self.__username,self.__password)) 

                except:
                    logger.error(f"error in database when retreiving username {self.__username}") 
                    raise DatabaseConnectionError()
                
                if not cur.fetchone() : 
                    logger.error(f" User {self.__username} error in connexion")
                    raise UserNotExists(self.__username)
                
        return {f"User {self.__username} Logged"}