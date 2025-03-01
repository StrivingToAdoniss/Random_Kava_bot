import asyncio
import logging
import math
import re
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.exceptions import BotBlocked

from Files.classification import Classification
from Model.Question import questions
from Model.User import user
from Model.Category import categories
from Model.User_Answer import user_answer
from admins import admins_list, chat_id

logging.basicConfig(level=logging.INFO)

kava_token = '6105836630:AAGLIAYZH5xO2UH8C5cmKqXv_7YalKh-5dU'
roll_token = '6499628008:AAGfenfjHSrUd5M7Ix4h6jc1Why1LLiPUsU'
bot = Bot(kava_token)
# Диспетчер
dp = Dispatcher(bot)
order = {}
data = questions.get_data()
deadline = datetime.date(2024, 6, 24)

print(data)


@dp.message_handler(commands=['send_test'])
async def test(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return
    else:
        await bot.send_message("677181730", text=f"Наш проєкт добігає кінця!\n"
                                                 f"Будемо тобі дуже вдячні, якщо ти заповниш "
                                                 f"<a href='https://docs.google.com/forms/d/e/1FAIpQLSerfyK2dgDkYD_1HJHAyTBDdgY-5eFlPGr_n2fEmxRVRm7C2A/viewform?usp=sf_link'>форму фідбеку</a>💕 "
                                                 f"для майбутнього розвитку і вдосконалення проєкту!",
                               parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['send_form'])
async def test(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return
    else:
        for user_id in user.get_users_all_questions():
            try:
                print("sent")
                await bot.send_message(user_id, text=f"Наш проєкт добігає кінця!\n"
                                                     f"Будемо тобі дуже вдячні, якщо ти заповниш "
                                                     f"<a href='https://docs.google.com/forms/d/e/1FAIpQLSerfyK2dgDkYD_1HJHAyTBDdgY-5eFlPGr_n2fEmxRVRm7C2A/viewform?usp=sf_link'>форму фідбеку</a>💕 "
                                                     f"для майбутнього розвитку і вдосконалення проєкту!",
                                       parse_mode=ParseMode.HTML)
            except BotBlocked as e:
                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(
                    message.chat.id))


@dp.message_handler(commands=['send_discount'])
async def test(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return
    else:
        for user_id in user.get_users_all_questions():
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_send_discount = types.KeyboardButton(text="Так, надіслати знижку.")
            keyboard.add(button_send_discount)

            await bot.send_message(user_id,
                                   f"Ти вже на фінішній прямій! Домовляйся зі своєю групою щодо дня зустрічі в «Кофі Шоп».\n"
                                   f"Ти зможеш скористатися знижкою один раз з 25.06 до 02.07. "
                                   f"Щоб отримати знижку — натисни «Так, надіслати знижку» і покажи фото на касі.\n\n"
                                   f"УВАГА! Фото знижки зникаюче, тому кнопку натискати треба вже безпосередньо в закладі!",
                                   reply_markup=keyboard)


@dp.message_handler(commands=['send_reminder'])
async def test(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return
    else:
        for user_id in user.get_users_all_questions():
            try:
                await bot.send_message(user_id, f"Привіт це <b>RandomKava бот</b>\n\n"
                                                f"Нагадую тобі, що <b>2 липня</b> закінчується дія знижки в закладі "
                                                f"<a href='https://www.instagram.com/kofi._.shop?igsh=MTY3ZDQ5N280NXk2bA=='>«Кофі Шоп»</a>. "
                                                f"Встигни зібратися зі своєю групою.\n\n"
                                                f"Якщо ти вже зустрівся з групою, то "
                                                f"<a href='https://docs.google.com/forms/d/e/1FAIpQLSerfyK2dgDkYD_1HJHAyTBDdgY-5eFlPGr_n2fEmxRVRm7C2A/viewform?usp=sf_link'>поділись враженнями</a>, "
                                                f"щоб з кожним разом проєкт ставав краще.",
                                       parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            except BotBlocked as e:
                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(
                    message.chat.id))


@dp.message_handler(commands=['send_reminder_test'])
async def test(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return
    else:
        await bot.send_message("677181730", f"Привіт це <b>RandomKava бот</b>\n\n"
                                                f"Нагадую тобі, що <b>2 липня</b> закінчується дія знижки в закладі "
                                                f"<a href='https://www.instagram.com/kofi._.shop?igsh=MTY3ZDQ5N280NXk2bA=='>«Кофі Шоп»</a>. "
                                                f"Встигни зібратися зі своєю групою.\n\n"
                                                f"Якщо ти вже зустрівся з групою, то "
                                                f"<a href='https://docs.google.com/forms/d/e/1FAIpQLSerfyK2dgDkYD_1HJHAyTBDdgY-5eFlPGr_n2fEmxRVRm7C2A/viewform?usp=sf_link'>поділись враженнями</a>, "
                                                f"щоб з кожним разом проєкт ставав краще.",
                               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text == "Так, надіслати знижку.")
async def process_send_discount(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if str(user_id) in user.get_users_id_with_valid_screen():
        if not user.is_discount_set(user_id):
            keyboard2 = types.ReplyKeyboardRemove()
            photo_file = "Знижка.png"
            photo_msg = await bot.send_photo(chat_id=user_id, photo=open(photo_file, 'rb'), reply_markup=keyboard2)
            await asyncio.sleep(60)
            await bot.delete_message(user_id, photo_msg.message_id)
            user.set_discount_sent(user_id)
            await bot.send_message(user_id, "Фото зі знижкою було надіслане!")
        else:
            await bot.send_message(user_id, "Знижку вже було надіслано!")


# Хендлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if datetime.date.today() < deadline:
        if not message.from_user.username:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Поділитися номером",
                                                request_contact=True)
            keyboard.add(button_phone)
            await bot.send_message(message.chat.id, 'Надішли свій номер телефону.',
                                   reply_markup=keyboard)
        else:
            user.insert_user(message.from_user.id, message.from_user.username)
            await message.answer("Привіт, " +
                                 message.from_user.username +
                                 "!\nБудь ласка, надішли фото донату від 50 грн."
                                 f"\n\nНа скриншоті має бути видно дату, отримувача і суму."
                                 f"\n\n\U0001F517Посилання на банку"
                                 f"\nhttps://send.monobank.ua/jar/A6JPNT1b3e"
                                 f"\n\n\U0001F4B3Номер картки банки"
                                 f"\n5375 4112 1932 5888")
    else:
        await message.answer(
            "На жаль, подія вже закінчилася. Очікуй нових запусків проєкту, та не забувай підтримувати ЗСУ!"
            f"\nhttps://send.monobank.ua/jar/A6JPNT1b3e"
            f"\n\n\U0001F4B3Номер картки банки"
            f"\n5375 4112 1932 5888")


@dp.message_handler(content_types=['contact'])
async def contact(message):
    if datetime.date.today() < deadline:
        if message.contact is not None:
            phone_number = str(message.contact.phone_number)
            user.updateUsernameNumber(message.contact.user_id, phone_number)
            keyboard2 = types.ReplyKeyboardRemove()
            await message.answer(f"Номер успішно відправлено."
                                 f"\nБудь ласка, надішли фото донату від 50 грн."
                                 f"\n\nНа скриншоті має бути видно дату, отримувача і суму."
                                 f"\n\n\U0001F517Посилання на банку"
                                 f"\nhttps://send.monobank.ua/jar/A6JPNT1b3e"
                                 f"\n\n\U0001F4B3Номер картки банки"
                                 f"\n5375 4112 1932 5888",
                                 reply_markup=keyboard2)
    else:
        await message.answer(
            "На жаль, подія вже закінчилася. Очікуй нових запусків проєкту, та не забувай підтримувати ЗСУ!"
            f" тут буде банка ")


@dp.message_handler(commands=['groups_test'])
async def group_users_by_personality(message: types.Message) -> None:
    print("--------------------------------- Work ---------------------------------")
    # Перевіряємо рівень доступу
    if str(message.from_user.id) not in admins_list:
        await message.answer("No access.")
        return

    users_data_ids = user.get_users_all_questions()
    print(users_data_ids)
    users_answers = []
    for i in range(len(users_data_ids)):
        ud = user_answer.get_data_user(users_data_ids[i])
        answer_of_user = []
        for j in ud:
            answer_of_user.append(j[3])
        users_answers.append(answer_of_user)
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
    if datetime.date.today() < deadline:
        print("here", user.getUsernameId(message.from_user.id))
        if user.getUsernameId(message.from_user.id) is not None:
            if user.is_screen_valid(message.from_user.id):
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Ти вже надіслав своє фото оплати.")
            else:
                await message.forward(chat_id=chat_id)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="Валідна", callback_data=f"valid {message.from_user.id} "))
                keyboard.add(
                    types.InlineKeyboardButton(text="Недійсна", callback_data=f"invalid {message.from_user.id} "))
                await bot.send_message(chat_id=chat_id,
                                       text="Будь ласка, перевір фото оплати.",
                                       reply_markup=keyboard)
        else:
            await bot.send_message(message.from_user.id, 'Надішли свій номер телефону.')
    else:
        await message.answer(
            "На жаль, подія вже закінчилася. Очікуй нових запусків проєкту та не забувай підтримувати ЗСУ!"
            f"\n\n\U0001F517Посилання на банку"
            f"\nhttps://send.monobank.ua/jar/A6JPNT1b3e"
            f"\n\n\U0001F4B3Номер картки банки"
            f"\n5375 4112 1932 5888")


@dp.callback_query_handler(lambda c: "valid" in c.data)
async def process_verification_result(callback_query: types.CallbackQuery):
    data_user = callback_query.data.split(' ')
    answer = data_user[0]
    user_id = data_user[1]
    username = user.getUsernameId(user_id)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=None)

    if answer == "valid":
        user.set_screen_valid(user_id)
        if username:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот від @{username} прийнято!")
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Скриншот прийнято!")

        await bot.send_message(chat_id=user_id,
                               text="Дякуємо! Скриншот прийнято! Ти можеш розпочати відповідати на питання.\n"
                                    "Щоб змінити відповідь, натисни на варіант, який хочеш обрати.")
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
                               text="Фото оплати недійсне. Будь ласка, надішли валідне фото оплати.")


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
        reply_markup = InlineKeyboardMarkup()
        for answer in row['answers']:
            reply_markup.add(InlineKeyboardButton(answer['title'], callback_data=
            f"{row['id_question']} {answer['id']} {user_id}"))

        await bot.send_message(text=f"{row['title']}", reply_markup=reply_markup, chat_id=user_id)
    else:
        await bot.send_message(text=f"Дякую за відповідь!\nТвої відповіді:\n{user_answer.print(user_id)}\n",
                               chat_id=user_id)
        await bot.send_message(text=f"Чудово, тепер бот опрацює твої відповіді! Незабаром ти дізнаєшся про свою "
                                    f"групу та знижки в закладі «Кофі Шоп»."
                                    f"\n\nЩиро дякуємо, що ти з нами в цьому проєкті!",
                               chat_id=user_id)


@dp.callback_query_handler(lambda c: re.match("\d+\s+\d+\s+\d+", c.data))
async def process_callback_query(callback_query: types.CallbackQuery):
    global order
    answer_user = callback_query.data.split()
    question_id = answer_user[0]
    answer_id = answer_user[1]
    user_id = answer_user[2]
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
        await bot.send_message(text=f"Дякую за відповідь!\nТвої відповіді:\n{user_answer.print(user_id)}\n",
                               chat_id=user_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
