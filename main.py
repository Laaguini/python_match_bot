from core.database.sqlite import SQLiteDatabase
from core.core import Core
from core.user import UsersFactory
from client.client import Client
from client.message_resolver import XMLMessageResolver
from aiogram.contrib.fsm_storage.files import JSONStorage

import config 

database = SQLiteDatabase(config.DATABASE_PATH, config.QUERIES_PATH)
message_resolver = XMLMessageResolver(config.MESSAGES_PATH)
users = UsersFactory(database)
core = Core(users)

storage = JSONStorage(config.STATE_STORAGE_PATH)
client = Client(config.BOT_API_TOKEN, core, message_resolver, storage)

client.run()
