class UserAlreadyExists(Exception):
    
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"user with ID {self.username} already exists"
    
class UserNotExists(Exception) : 

    def __init__(self, username):
        self.username = username

    def __str__(self): 
        return f"user {self.username} not exists"