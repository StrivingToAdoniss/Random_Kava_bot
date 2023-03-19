import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from Question import questions
from User import user

logging.basicConfig(level=logging.INFO)


token = '6211270631:AAHjLGInSIPzGaTvEe2bWcq_L2UxNWYcq2o'
bot = Bot(token)
# Диспетчер
dp = Dispatcher(bot)


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_message = "Hello " + message.from_user.username
    await message.answer(user_message)


@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    user.insert_data(message.from_user.id)
    # print(user.get_data()[0][0])
    await message.answer(user.get_data())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())