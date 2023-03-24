import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from Model.Question import questions
from Model.User import user
from Model.Category import categories
from admins import admins_list

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
    user.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(user.get_data())


@dp.message_handler(commands=['groups'])
async def groups(message: types.Message):
    if str(message.from_user.id) in admins_list:
        result_users_in_groups = ""
        category_ids = categories.get_categories_ids()
        for category_id in category_ids:
            result_users_in_groups += f"Категорія {category_id}: {str(user.get_usernames_by_category_id(category_id))}\n"
        await message.answer(result_users_in_groups)
    else:
        await message.answer("No access.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())