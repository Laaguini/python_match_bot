from core.database.sqlite import SQLiteDatabase
from core.user import UsersFactory


database = SQLiteDatabase("./data.db", "./sql")
users = UsersFactory(database)

u = users.get(12)

print(u.info["bio"])