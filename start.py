import telebot
from telebot import types
import time
from funcs import show_menu, generate_password, get_next_answer
from getimagemap import data as image
from handlers import valid_name, check_team_count, check_number
from validate_email import validate_email
import re
from sheets import save_data, get_info, get_questions
from config import token, MIN_PARTICIPANTS, MAX_PARTICIPANTS, doc_name

# устанавливаем соединение с апи телеграма
bot = telebot.TeleBot(token)

# создаем словарь, в котором будут храниться промежуточные данные, которые потом перенесем в гугл-док
# добавлять данные будем по ключу id переписки, чтобы была возможность работы с ботом
# нескольких пользователей одновременно
data = {}

answers = {}


# обработчик команды старт и хелп для открытия меню
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, text=show_menu()[0], reply_markup=show_menu()[1])


def get_team_name(message):  # получаем название команды
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    # проверка на правильность введенных данных - все правильно, значит, переходим, к следующему шагу
    if valid_name(message.text):
        data[message.from_user.id] = {}
        data[message.from_user.id]['team_name'] = message.text
        bot.send_message(message.from_user.id, "Сколько человек у вас в команде?")
        bot.register_next_step_handler(message, get_team_count)
    else:
        bot.send_message(message.from_user.id, "Так команду нельзя назвать, попробуйте выбрать другое имя")
        bot.register_next_step_handler(message, get_team_name)


def get_team_count(message):  # получаем количество человек
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    if check_team_count(message.text, MIN_PARTICIPANTS, MAX_PARTICIPANTS):
        data[message.chat.id]['team_count'] = int(message.text.strip())
        # временные данные для записи всех участников
        data[message.chat.id]['temp_count'] = 0
        data[message.chat.id]['participants'] = []
        bot.send_message(message.from_user.id, "Введите ФИО участника 1")
        bot.register_next_step_handler(message, get_participants)
    else:
        bot.send_message(message.from_user.id, f"Количество участников может быть от {MIN_PARTICIPANTS}"
                                               f" до {MAX_PARTICIPANTS}")
        bot.register_next_step_handler(message, get_team_count)


def get_participants(message):  # получаем ФИО участников
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    # проверяем, соответствует ли ФИО шаблону - имена собственные начинаются с большой буквы,
    # должны быть хотя бы имя и фамилия - 2 слова, все данные вводятся только с помощью кириллицы
    # если все в порядке - добавляем данные в словарь data
    if re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', f"{message.text.strip()}"):
        if data[message.chat.id]['temp_count'] + 1 != data[message.chat.id]['team_count']:
            data[message.chat.id]['temp_count'] += 1
            data[message.chat.id]['participants'].append(message.text.strip())
            if data[message.chat.id]['temp_count'] != data[message.chat.id]['team_count']:
                bot.send_message(message.from_user.id,
                                 f'Введите ФИО участника {data[message.chat.id]["temp_count"] + 1}')

            bot.register_next_step_handler(message, get_participants)
        else:
            data[message.chat.id]['participants'].append(message.text.strip())
            bot.send_message(message.from_user.id, "Введите мобильный номер капитана команды в формате 7XXXXXXXXXX")
            bot.register_next_step_handler(message, get_number)
    else:
        bot.send_message(message.from_user.id, "Введите ФИО участника, пожалуйста!")
        bot.register_next_step_handler(message, get_participants)


def get_number(message):
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    # проверка номера по шаблону
    # если все в порядке - добавляем данные в словарь data
    if check_number(message.text):
        data[message.chat.id]['number'] = message.text.strip()
        bot.send_message(message.from_user.id, "Введите электронную почту капитана")
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.from_user.id, "Введите номер в правильном формате!")
        bot.register_next_step_handler(message, get_number)


def get_email(message):
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    # проверка почты по шаблону, если все в порядке - добавляем данные в словарь data
    if validate_email(message.text):
        data[message.chat.id]['email'] = message.text.strip()
        bot.send_message(message.from_user.id, "Введите название вашего учебного заведения")
        bot.register_next_step_handler(message, get_institution)
    else:
        bot.send_message(message.from_user.id, "Введите почту в правильном формате!")
        bot.register_next_step_handler(message, get_email)


def get_institution(message):
    # проверка, не написал ли пользователь команду /start или /help
    if message.text in ('/start', '/help'):
        bot.send_message(message.from_user.id, text=show_menu(True)[0], reply_markup=show_menu()[1])
        return

    if valid_name(message.text):  # проверка на правильность данных
        data[message.chat.id]['institution'] = message.text.strip()
        kb = types.InlineKeyboardMarkup()
        # здесь добавляем 2 кнопки - подтверждение анкеты и просьба переделать, в первом случае
        # переходим к отправке данных, иначе - начинаем опрос с начала
        kb.add(types.InlineKeyboardButton('Подтвердить', callback_data="approved"),
               types.InlineKeyboardButton('Переделать', callback_data="start_registration"))

        # показываем полученные данные пользователю для проверки
        bot.send_message(message.from_user.id,
                         text=f"""*Это правильные данные?*\n
*Название команды*:\n{data[message.from_user.id]['team_name']}
*Количество участников*:\n{data[message.from_user.id]['team_count']}
*Участники*:\n{", ".join(data[message.from_user.id]['participants'])}
*Номер капитана*:\n{data[message.from_user.id]['number']}
*Почта капитана*:\n{data[message.from_user.id]['email']}
*Учебное заведение*:\n{data[message.from_user.id]['institution']}
""", reply_markup=kb, parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Введите учебное заведение в правильном формате!")
        bot.register_next_step_handler(message, get_institution)


# работа с кнопками - callback_inline
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # обработчик кнопки уточнения места
    if call.data == "time_and_place":
        back_btn = types.InlineKeyboardMarkup()
        back_btn.add(types.InlineKeyboardButton(text='Назад', callback_data="back"))
        information = get_info()
        bot.edit_message_text(f'Мероприятие: {information[1]}\n'
                              f'Адрес: {information[0]}'
                              f'\nВремя проведения: {information[2]}',
                              call.message.chat.id, call.message.message_id)
        # отправляем фото, переменную image получаем с помощью яндекс.геокодера
        # яндекс Static Maps API - все в файле getimagemap.py
        bot.send_photo(call.message.chat.id, image, reply_markup=back_btn)

    # высылаем документ из папки files
    elif call.data == "regulations":
        regulations = open(f'files/{doc_name}', 'rb')
        bot.send_document(call.message.chat.id, regulations)

    # пользователь нажал на регистрацию, спрашиваем подтверждение
    elif call.data == "registration":
        yesno = types.InlineKeyboardMarkup()
        # добавляем кнопки подтверждения, на случай, если пользователь случайно нажал
        yesno.add(types.InlineKeyboardButton("Да", callback_data='start_registration'),
                  types.InlineKeyboardButton("Нет", callback_data='abort'))
        bot.edit_message_text("Вы хотите начать регистрацию?", call.message.chat.id,
                              call.message.message_id, reply_markup=yesno)

    # возвращение к меню, интерфейс появляется в новом сообщении
    elif call.data == "back":
        bot.send_message(call.message.chat.id, show_menu(True)[0], reply_markup=show_menu()[1])

    # возвращение к меню, прошлое сообщение редактируется
    elif call.data == "abort":
        bot.edit_message_text(show_menu(True)[0], call.message.chat.id,
                              call.message.message_id, reply_markup=show_menu()[1])

    # пользователь подтвердил продолжение регистрации, задаем первый вопрос
    elif call.data == "start_registration":
        msg = bot.edit_message_text("Какое название у вашей команды?", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, get_team_name)

    # пользователь подтвердил данные
    elif call.data == "approved":
        # добавление кнопки возвращения в меню
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('Назад в меню', callback_data='abort'))

        # удаляем промежуточный счетчик количества участников
        del data[call.message.chat.id]['temp_count']
        # получаем сгенерированный пароль и заносим его в словарь
        password = generate_password()
        data[call.message.chat.id]['password'] = password
        # запускаем функцию сохранения данных в БД (гугл-док)
        save_data(list(data[call.message.chat.id].values()))
        # уведомляем пользователя об отправлении данных и просим запомнить пароль
        bot.edit_message_text("Ваши данные отправлены!", call.message.chat.id, call.message.message_id, reply_markup=kb)
        bot.send_message(call.message.chat.id, f"Обязательно запомните пароль вашей команды!\n*{password}*",
                         parse_mode='Markdown')

    elif call.data == 'knowledge':
        answers[call.message.chat.id] = {}
        answers[call.message.chat.id]['count'] = 1
        answers[call.message.chat.id]['right'] = []
        answers[call.message.chat.id]['max'] = get_questions()[1]

        get_next_answer(answers[call.message.chat.id]['max'], 0, call.message.chat.id, bot)

    elif call.data == 'right_answer':
        answers[call.message.chat.id]['right'].append(answers[call.message.chat.id]['count'])
        answers[call.message.chat.id]['count'] += 1
        number = answers[call.message.chat.id]['count']
        get_next_answer(answers[call.message.chat.id]['max'], number-1, call.message.chat.id, bot)

    elif call.data == 'false_answer':
        answers[call.message.chat.id]['count'] += 1
        number = answers[call.message.chat.id]['count']
        get_next_answer(answers[call.message.chat.id]['max'], number-1, call.message.chat.id, bot)

    elif call.data == 'finish':
        output = ''
        for i in range(1, answers[call.message.chat.id]['max']+1):
            if i in answers[call.message.chat.id]['right']:
                output += f'Вопрос {i}: *Верно*\n'
            else:
                output += f'Вопрос {i}: *Неверно*\n'
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('В меню', callback_data='back'))
        bot.send_message(call.message.chat.id, f"{output}",
                         parse_mode='Markdown', reply_markup=kb)


# запуска бота, каждые 15 секунд проверка: не упал ли бот, если что, запускаем заново
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
