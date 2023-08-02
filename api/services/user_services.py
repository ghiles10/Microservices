from psycopg2.extensions import connection
from api.conf import log_conf
from fastapi import  HTTPException

logger = log_conf.logger

class UserService : 

    """ this class is used to manage acces for the users services of the api """

    # count the number of visitors api 
    nb_visitors = 0 

    def __init__(self, credentials : dict  ): 

        self.__username = credentials['username']
        self.__password = credentials['password']
        UserService.nb_visitors += 1 


    def subscribe(self, conn_db: connection )  :  
            
        with conn_db.cursor() as cur: 

            try:
                cur.execute( 
                "INSERT INTO users (username, password) VALUES (%s, %s) "  ,          
                 (self.__username, self.__password)

                )
                
                conn_db.commit() 

            except : 
                logger.error( 'error in writing sql query subscribe' )

                conn_db.rollback()
                raise HTTPException(status_code=500, detail = 'Error in Database' )

            # cheks query
            affected_rows = cur.rowcount
            if affected_rows < 1 : 
                
                logger.error('no rows affected')
                raise HTTPException(status_code=401  , detail = f"erreur insertion username : {username}") 
            
            conn_db.commit()

            return {f"message: {self.__username} subscribe"}


    def login(self, conn_db: connection) : 
        
        # cheks subscribe  
        with conn_db.cursor() as cur: 

            try : 
                cur.execute(f"SELECT username FROM users where username = '{self.__username}'") 

            except:
                logger.error(f"error in database when retreiving username {self.__username}") 
                raise HTTPException(status_code=500, detail="Error in database")

            if not cur.fetchone() : 
                
                logger.error(f" User {self.__username} Not Exists ")
                raise HTTPException( status_code=401, detail=f"Username {self.__username} Invalid" ) 
        
        return {f"User {self.__username} Logged"}