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


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    print(message.from_user.id)
    print(message.from_user.username)
    if not message.from_user.username:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Поділитися номером",
                                            request_contact=True)
        keyboard.add(button_phone)
        await bot.send_message(message.chat.id, 'Надішліть номер телефону.',
                               reply_markup=keyboard)
    else:
        user.insert_user(message.from_user.id, message.from_user.username)
        await message.answer("Привіт, " +
                             message.from_user.username +
                             "!\nБудь ласка, надішліть фото оплати.")


@dp.message_handler(content_types=['contact'])
async def contact(message):
    print("here i am")
    if message.contact is not None:
        phone_number = str(message.contact.phone_number)
        user.updateUsernameNumber(message.contact.user_id, phone_number)
        keyboard2 = types.ReplyKeyboardRemove()
        await message.answer('Ви успішно відправили свій номер.\nБудь ласка, надішліть фото оплати.',
                             reply_markup=keyboard2)


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


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_payment_photo(message: types.Message):
    print("here", user.getUsernameId(message.from_user.id))
    if user.getUsernameId(message.from_user.id) is not None:
        if user.is_screen_valid(message.from_user.id):
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Ви вже надіслали фото оплати.")
        else:
            await message.forward(chat_id=chat_id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Валідна", callback_data=f"valid {message.from_user.id} "))
            keyboard.add(
                types.InlineKeyboardButton(text="Недійсна", callback_data=f"invalid {message.from_user.id} "))
            await bot.send_message(chat_id=chat_id,
                                   text="Будь ласка, перевірте фото оплати.",
                                   reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Надішліть номер телефону.')


@dp.callback_query_handler(lambda c: "valid" in c.data)
async def process_verification_result(callback_query: types.CallbackQuery):
    print(callback_query.from_user.id)
    print(callback_query.from_user.username)
    data_user = callback_query.data.split(' ')
    answer = data_user[0]
    user_id = data_user[1]
    username = user.getUsernameId(user_id)
    if answer == "valid":
        user.set_screen_valid(user_id)
        if username:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від @{username} прийнято!")
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот прийнято!")

        await bot.send_message(chat_id=user_id,
                               text="Дякуємо! Скриншот прийнято! Ви можете розпочати відповідати на питання.")
        order[str(user_id)] = 0
        await ask_question(user_id)
    elif answer == "invalid":
        if username:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від @{username} відхилено!")
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від відхилено!")
        await bot.send_message(chat_id=user_id,
                               text="Фото оплати недійсне. Будь ласка, надішліть валідне фото оплати.")


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


async def ask_question(user_id):
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
        await bot.send_message(text=f"{row['title']}", reply_markup=reply_markup, chat_id=user_id)
    else:
        await bot.send_message(text=f"Дякую за відповідь!\nВаші відповіді:\n{user_answer.print(user_id)}\n",
                               chat_id=user_id)
        await bot.send_message(text=f"Повідомлення",
                               chat_id=user_id)


@dp.callback_query_handler(lambda c: re.match("\d+\s+\d+\s+\d+", c.data))
async def process_callback_query(callback_query: types.CallbackQuery):
    global order

    # await callback_query.answer()
    answer_user = callback_query.data.split()
    question_id = answer_user[0]
    answer_id = answer_user[1]
    user_id = answer_user[2]
    # print(question_id)
    # print(type(question_id))
    # print(data[order[str(callback_query.from_user.id)]]["id_question"])
    # print(type(data[order[str(callback_query.from_user.id)]]["id_question"]))
    try:
        if int(data[order[str(callback_query.from_user.id)]]["id_question"]) == int(question_id):
            print("here")

            user_answer.insert_data(question_id, user_id, answer_id)
            order[str(user_id)] += 1
            await ask_question(user_id)
        else:
            print("else")
            user_answer.insert_data(question_id, user_id, answer_id)
    except IndexError as e:
        print("except")
        user_answer.insert_data(question_id, user_id, answer_id)
        await bot.send_message(text=f"Дякую за відповідь!\nВаші відповіді:\n{user_answer.print(user_id)}\n",
                               chat_id=user_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
