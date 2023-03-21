from aiogram import Bot, Dispatcher, types, executor

class Client(): 
    dispatcher: Dispatcher

    def __init__(self, bot_api_token, database, message_resolver): 
        self.database = database 
        self.bot = Bot(bot_api_token, parse_mode='MarkdownV2')
        self.dispatcher = Dispatcher(self.bot)
        self.message_resolver = message_resolver

        @self.dispatcher.message_handler(commands=["start"])
        async def handle_start(message: types.Message): 
            await message.answer(self.message_resolver.get("start"))

        @self.dispatcher.message_handler(commands=["info"])
        async def handle_info(message: types.Message):
            await message.answer(self.message_resolver.get("info"))

        @self.dispatcher.message_handler(commands=["help"])
        async def handle_info(message: types.Message):
            await message.answer(self.message_resolver.get("help"))
    
    def run(self): 
        executor.start_polling(self.dispatcher, skip_updates=True)
