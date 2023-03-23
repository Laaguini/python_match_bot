from .user import UsersFactory

class Core():
    users: UsersFactory

    def __init__(self, users): 
        self.users = users