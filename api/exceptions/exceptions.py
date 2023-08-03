from fastapi import  HTTPException


class UserAlreadyExists(HTTPException):
    
    def __init__(self, username):
        self.username = username
        super().__init__(status_code=400, detail=f"user with ID {self.username} already exists")


    

class UserNotExists(HTTPException) : 

    def __init__(self, username):
        self.username = username
        super().__init__(status_code = 400, detail =  f"credentials for user {self.username} not correct")



class DatabaseConnectionError(HTTPException) : 

    def __init__(self):
    
        super().__init__(status_code=500, detail="Error in database") 