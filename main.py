import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Model.Question import questions
from Model.User import user
from Model.Category import categories
from Model.User_Answer import user_answer
from Model.Answer import answer
from admins import admins_list

logging.basicConfig(level=logging.INFO)


token = '6211270631:AAHjLGInSIPzGaTvEe2bWcq_L2UxNWYcq2o'
bot = Bot(token)
# Диспетчер
dp = Dispatcher(bot)
order = 0
data = questions.get_data()

print(data)


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_message = "Hello " + message.from_user.username
    await message.answer(user_message)


@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    user.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(user.get_data())
    await ask_question(message)


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


async def ask_question(message: types.Message):
    try:
        row = data[order]
    except IndexError:
        row = None
    if row is not None:
        answer_buttons = [
            InlineKeyboardButton(answer['title'], callback_data=f"{row['id_question']} {answer['id']}") for answer in row['answers']
        ]
        reply_markup = InlineKeyboardMarkup().add(*answer_buttons)
        await message.answer(row["title"], reply_markup=reply_markup)
    else:
        await message.answer(f"Дякую за відповідь!\nВаші відповіді: {user_answer}\n")


@dp.callback_query_handler(lambda c: True)
async def process_callback_query(callback_query: types.CallbackQuery):
    global order
    await callback_query.answer()
    answer_user = callback_query.data.split()
    question_id = answer_user[0]
    answer_id = answer_user[1]

    user_id = callback_query.message.from_user.id
    user_answer.insert_data(question_id, user_id, answer_id)
    order += 1
    await ask_question(callback_query.message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
