import asyncio
import logging
import math
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Files.classification import Classification
from Model.Question import questions
from Model.User import user
from Model.Category import categories
from Model.User_Answer import user_answer
from admins import admins_list, chat_id

logging.basicConfig(level=logging.INFO)

token = '6211270631:AAHjLGInSIPzGaTvEe2bWcq_L2UxNWYcq2o'
bot = Bot(token)
# Диспетчер
dp = Dispatcher(bot)
order = {}
data = questions.get_data()

print(data)


@dp.message_handler(commands=['groups_test'])
async def group_users_by_personality(message: types.Message) -> None:
    print("--------------------------------- Work ---------------------------------")
    # Перевіряємо рівень доступу
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return

    users_data_ids = user.get_users_all_questions()
    users_answers = []
    for i in range(len(users_data_ids)):
        ud = user_answer.get_data_user(users_data_ids[i])
        answer_of_user = []
        for j in ud:
            answer_of_user.append(j[3])
        users_answers.append(answer_of_user)
    print(users_data_ids)
    print(users_answers)
    batch_size = 4
    n_clusters = math.ceil(len(users_data_ids) / batch_size)  # Maximum number of clusters
    categories.insert_categories(n_clusters)

    if n_clusters > 0:
        classification = Classification(users_data_ids, users_answers, n_clusters)
        classification.classificate()
        cluster_assignments = classification.get_groups()

    else:
        cluster_assignments = []
        for _ in users_data_ids:
            cluster_assignments.append(1)
    # print(cluster_assignments)
    user.updateCategory(users_data_ids, cluster_assignments)

    await message.answer("Ready. Press /groups to see results.")


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user.insert_user(message.from_user.id, message.from_user.username)
    print(message.from_user.id)
    await message.answer("Привіт, " +
                         message.from_user.username +
                         "!\nБудь ласка, надішліть фото оплати.")

    @dp.message_handler(content_types=types.ContentType.PHOTO)
    async def process_payment_photo(message: types.Message):
        if user.is_screen_valid(message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Ви вже надіслали фото оплати.")
        else:
            await message.forward(chat_id=chat_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Валідна", callback_data="valid"))
            keyboard.add(types.InlineKeyboardButton(text="Недійсна", callback_data="invalid"))
            await bot.send_message(chat_id=chat_id,
                                   text="Будь ласка, перевірте фото оплати.",
                                   reply_markup=keyboard)

            # dp.remove_handler(process_payment_photo)

    @dp.callback_query_handler(lambda c: c.data == "invalid" or c.data == "valid")
    async def process_verification_result(callback_query: types.CallbackQuery):
        if callback_query.data == "valid":
            user.set_screen_valid(message.from_user.id)
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від @{message.from_user.username} прийнято!")
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Дякуємо! Скриншот прийнято! Ви можете розпочати відповідати на питання.")
            order[str(message.from_user.id)] = 0
            await ask_question(message, message.from_user.id)
        elif callback_query.data == "invalid":
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від @{message.from_user.username} відхилено!")
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Фото оплати недійсне. Будь ласка, надішліть валідне фото оплати.")

        # dp.remove_handler(process_verification_result)


# @dp.message_handler(commands=['next'])
# async def next(message: types.Message):
#     user.insert_user(message.from_user.id, message.from_user.username)
#     print(message.from_user.id)
#     # await message.answer(user.get_data())
#     order[str(message.from_user.id)] = 0
#     await ask_question(message, message.from_user.id)


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


async def ask_question(message: types.Message, user_id):
    # print(message.from_user.id, user_id)
    try:
        row = data[order[str(user_id)]]
    except IndexError:
        row = None
    if row is not None:
        answer_buttons = [
            InlineKeyboardButton(answer['title'], callback_data=
            f"{row['id_question']} {answer['id']} {user_id}") for answer in row['answers']
        ]
        reply_markup = InlineKeyboardMarkup().add(*answer_buttons)
        await message.answer(row["title"], reply_markup=reply_markup)
    else:
        await message.answer(f"Дякую за відповідь!\nВаші відповіді:\n{user_answer.print(user_id)}\n")


@dp.callback_query_handler(lambda c: re.match("\d+\s+\d+\s+\d+", c.data))
async def process_callback_query(callback_query: types.CallbackQuery):
    global order

    await callback_query.answer()
    answer_user = callback_query.data.split()
    question_id = answer_user[0]
    answer_id = answer_user[1]
    user_id = answer_user[2]
    user_answer.insert_data(question_id, user_id, answer_id)
    order[str(user_id)] += 1
    await ask_question(callback_query.message, user_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
