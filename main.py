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
from sklearn.cluster import KMeans

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

    # Взаємодіємо з ДБ:
    # -- отримуємо список айді юзерів(users)
    # -- формуємо 2-d масив вигляду [[user_id, first_answer_id, second_answer_id...], [user_id, first_answer_id, second_answer_id...]] (users_data)
    users = user.getUsersId()
    users_data = []
    for i in range(len(users)):
        ud = user_answer.get_data_user(users[i])
        users_data.append([])
        users_data[i].append(users[i])
        for j in ud:
            users_data[i].append(j[3])
    # Позбуваємося зайвих користувачів(тих, хто не відповів на всі питання) ------------------------------- Ось тут, як додамо всі питання, потрібно буде змінити 4 на кількість питань+1
    for i in users_data:
        if len(i) != 4:
            users_data.remove(i)

    # Основна робота коду Саші
    kmeans_model = KMeans(n_clusters=2, random_state=42).fit(users_data)
    cluster_assignments = kmeans_model.predict(users_data)
    # Формуємо результати
    labels = {0: 'Introverted', 1: 'Extroverted'}
    results = []
    print(f"{users} --- {cluster_assignments}")
    for i in range(len(users_data)):
        results.append([users_data[i][0], labels[cluster_assignments[i]]])

    # Групуємо по 4 юзера "Extroverted"
    # extroverted_groups: list[tuple[str, pd.DataFrame]] = []
    # for i in range(0, len(extroverted_users), 4):
    #     extroverted_group = extroverted_users.iloc[i:i+4]
    #     extroverted_group_name = f'Extroverted{i//4 + 1}'
    #     extroverted_groups.append((extroverted_group_name, extroverted_group))

    # Групуємо по 4 юзера в "Introverted"
    # introverted_groups: list[tuple[str, pd.DataFrame]] = []
    # for i in range(0, len(introverted_users), 4):
    #     introverted_group = introverted_users.iloc[i:i+4]
    #     introverted_group_name = f'Introverted{i//4 + 1}'
    #     introverted_groups.append((introverted_group_name, introverted_group))

    # Прінтимо в консольку(Треба придумати норм спосіб)
    # result = 'Introverted Groups:\n'
    # for group_name, group in introverted_groups:
    #     result += f"{group_name}\n{group.to_string(index=False)}\n\n"
    #
    # result += 'Extroverted Groups:\n'
    # for group_name, group in extroverted_groups:
    #     result += f"{group_name}\n{group.to_string(index=False)}\n\n"

    await message.answer(results)


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_message = "Hello " + message.from_user.username
    await message.answer(user_message)


@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    user.insert_user(message.from_user.id, message.from_user.username)
    print(message.from_user.id)
    await message.answer(user.get_data())
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
    print(message.from_user.id, user_id)
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
