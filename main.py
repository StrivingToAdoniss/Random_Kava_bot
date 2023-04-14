import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Model.Question import questions
from Model.User import user
from Model.Category import categories
from Model.User_Answer import user_answer
from admins import admins_list
import pandas as pd
from sklearn.cluster import MiniBatchKMeans

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
    # print(users_data_ids)
    # print(users_answers)
    batch_size = 4
    n_clusters = round(len(users_data_ids) / batch_size)  # Maximum number of clusters

    if n_clusters > 0:
        model = MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size)
        # print(n_clusters)
        categories.insert_categories(n_clusters)
        model.fit(users_answers)
        cluster_assignments = model.predict(users_answers)
    else:
        cluster_assignments = []
        for _ in users_data_ids:
            cluster_assignments.append(0)
    # print(cluster_assignments)
    user.updateCategory(users_data_ids, cluster_assignments)

    await message.answer("Ready. Press /groups to see results.")


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_message = "Привіт, " + message.from_user.username + "\nДля продовження натисни /next."
    await message.answer(user_message)


@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    user.insert_user(message.from_user.id, message.from_user.username)
    print(message.from_user.id)
    # await message.answer(user.get_data())
    order[str(message.from_user.id)] = 0
    await ask_question(message, message.from_user.id)


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


@dp.callback_query_handler(lambda c: True)
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
