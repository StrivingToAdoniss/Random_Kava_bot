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
    row = questions.get_by_id(question_number)
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


@dp.callback_query_handler(lambda c: True)
async def process_callback_query(message: types.Message, callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    question_id = await state.get_data('question_id')
    answer = callback_query.data

    user_answer.insert_data(message.from_user.id, question_id, answer)

    row = questions.get_one(question_id)
    if row is not None:
        await ask_question(callback_query.message, row[0])
    else:
        await Question.end.set()
        await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
