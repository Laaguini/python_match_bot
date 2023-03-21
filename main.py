from core.database.sqlite import SQLiteDatabase
from core.user import UsersFactory
from client.client import Client
from client.message_resolver import FilesystemMessageResolver

import config 

database = SQLiteDatabase(config.DATABASE_PATH, config.QUERIES_PATH)
message_resolver = FilesystemMessageResolver(config.MESSAGES_PATH)
client = Client(config.BOT_API_TOKEN, database, message_resolver)

client.run()