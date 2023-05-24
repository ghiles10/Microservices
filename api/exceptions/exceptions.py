class UserAlreadyExists(Exception):
    
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"user with ID {self.username} already exists"
    
# class UserNotExists(Exception) : 

#     def __init__(self, user_id):
#         self.user_id = user_id

#     def __str__(self): 
#         return f"user {self.user_id} not exists"