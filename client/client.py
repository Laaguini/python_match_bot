from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
class Registration(StatesGroup):
    name = State()
    age = State()
    preferred_age = State()
    gender = State()
    preferred_gender = State()
    bio = State()

class Client(): 
    dispatcher: Dispatcher

    def __init__(self, bot_api_token, core, message_resolver, storage=MemoryStorage()):
        self.core = core 
        self.bot = Bot(bot_api_token)
        self.dispatcher = Dispatcher(self.bot, storage=storage)
        self.message_resolver = message_resolver

        @self.dispatcher.message_handler(commands=["start"])
        async def handle_start(message: types.Message): 
            try: 
                await message.answer(**self.message_resolver.get("start"))
            except Exception as e: 
                print(e)

        @self.dispatcher.message_handler(commands=["info"])
        async def handle_info(message: types.Message):
            await message.answer(**self.message_resolver.get("info"))

        @self.dispatcher.message_handler(commands=["help"])
        async def handle_info(message: types.Message):
            await message.answer(**self.message_resolver.get("help"))

        @self.dispatcher.callback_query_handler(lambda c: c.data == "register")
        async def handle_register_cb(cb: types.CallbackQuery):
            await Registration.name.set()
            await cb.message.answer(**self.message_resolver.get("register_name"))

        @self.dispatcher.message_handler(commands=["register"])
        async def handle_register_cmd(message: types.Message):
            await Registration.name.set()
            await message.answer(**self.message_resolver.get("register_name"))

        @self.dispatcher.message_handler(state=Registration.name)
        async def handle_register_age(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['name'] = message.text

            await Registration.next()
            await message.answer(**self.message_resolver.get("register_age"))

        @self.dispatcher.message_handler(state=Registration.age)
        async def handle_register_preferred_age(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['age'] = message.text

            await Registration.next()
            await message.answer(**self.message_resolver.get("register_preferred_age"))

        @self.dispatcher.message_handler(state=Registration.preferred_age)
        async def handle_register_gender(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['preferred_age_min'], data['preferred_age_max'] = message.text.split('-')

            await Registration.next()
            await message.answer(**self.message_resolver.get("register_gender"))

        @self.dispatcher.message_handler(state=Registration.gender)
        async def handle_register_gender(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['gender'] = message.text

            await Registration.next()
            await message.answer(**self.message_resolver.get("register_preferred_gender"))

        @self.dispatcher.message_handler(state=Registration.preferred_gender)
        async def handle_register_preferred_gender(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['preferred_gender'] = message.text

            await Registration.next()
            await message.answer(**self.message_resolver.get("register_bio"))

        @self.dispatcher.message_handler(state=Registration.bio)
        async def handle_register_bio(message: types.Message, state: FSMContext): 

            async with state.proxy() as data: 
                data['bio'] = message.text

            user_data = data.as_dict()
            id, username = message.from_id, message.from_user.username
            self.core.users.get(id).register({**user_data, 'username': username, 'id': id})

            await message.answer(user_data)
            await state.finish()
            
    
    def run(self): 
        executor.start_polling(self.dispatcher, skip_updates=True)
