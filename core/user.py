class UsersFactory(): 
    def __init__(self, database) -> None:
        self.database = database

    def get(self,id):
        return User(self.database, id)

def registered(f): 
    def wrapper(*args): 
        user = args[0]

        if user.info is None: 
            user.register()
        
        return f(*args)
    return wrapper

class User(): 
    info = {
        "id": int,
        "username": str,
        "name": str,
        "age": int,
        "preferred_age_min": int,
        "preferred_age_max": int, 
        "gender": "male" or "female",
        "preferred_gender": "male" or "female" or "all",
        "pictures": [str],
        "bio": str,
        "registration_state": str, 
    }

    def __init__(self, database, id) -> None:
        self.id = id
        self.database = database
        self.info = database.get_user(id)

    @registered
    def get_recommended(self):
        return self.database.get_user_recomendations(self.id)
    
    @registered
    def get_replies(self):
        return self.database.get_user_replies(self.id)

    @registered
    def get_next_reply(self):
        return self.database.get_user_next_reply(self.id)

    @registered 
    def send_reply(self, to, message):
        self.database.create_user_reply(self.id, to, message)

    def register(self, info): 
        self.info = self.database.create_user(info)