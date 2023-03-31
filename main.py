import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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

#Sasha's code start
    
class Question(StatesGroup):
    end = State()

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    user.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(user.get_data())
    await ask_question(message, 1)


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

async def ask_question(message: types.Message, question_number):
    cur = conn.cursor()
    cur.execute('SELECT id, question, answer1, answer2 FROM questions WHERE id=%s', (question_number,))
    row = cur.fetchone()
    if row is not None:
        question_id, question_text, answer1, answer2 = row

       
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(question_id=question_id)


        answer_buttons = [
            InlineKeyboardButton(answer, callback_data=answer) for answer in [answer1, answer2]
        ]
        reply_markup = InlineKeyboardMarkup().add(*answer_buttons)
        await message.answer(question_text, reply_markup=reply_markup)
    else:
        await state.finish()

    cur.close()


@dp.callback_query_handler(lambda c: True)
async def process_callback_query(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()


    question_id = await state.get_data('question_id')
    answer = callback_query.data


    cur = conn.cursor()
    cur.execute('INSERT INTO answers (question_id, answer) VALUES (%s, %s)', (question_id, answer))
    conn.commit()
    cur.close()

 
    cur = conn.cursor()
    cur.execute('SELECT id FROM questions WHERE id > %s ORDER BY id ASC LIMIT 1', (question_id,))
    row = cur.fetchone()
    if row is not None:
        await ask_question(callback_query.message, row[0])
    else:
        await Question.end.set()
        await state.finish()
    cur.close()
    
#Sasha's code End

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
