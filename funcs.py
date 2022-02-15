from telebot import types
from string import ascii_letters, digits
import secrets
import random
from sheets import get_questions

alphabet = ascii_letters + digits


# показать меню с кнопками - если меню вызывается не в первый раз, то в аргументе передается True и показывается
# другой текст
def show_menu(flag=False):
    keyboard = types.InlineKeyboardMarkup()
    key_registration = types.InlineKeyboardButton(text='Регистрация на мероприятие', callback_data='registration')
    keyboard.add(key_registration)
    key_time_and_place = types.InlineKeyboardButton(text='Уточнить время и место', callback_data='time_and_place')
    keyboard.add(key_time_and_place)
    key_regulations = types.InlineKeyboardButton(text='Изучить регламент проведения', callback_data='regulations')
    keyboard.add(key_regulations)
    knowledge = types.InlineKeyboardButton(text='Проверить свои знания', callback_data='knowledge')
    keyboard.add(knowledge)

    if not flag:
        greeting = 'Здравствуйте! Вы можете зарегистрироваться на мероприятие, узнать время и место проведения или' \
                   ' изучить регламент'
    else:
        greeting = 'Как еще я могу Вам помочь?'
    return greeting, keyboard


# генерация пароля
def generate_password():
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    return password


def get_next_answer(maxie, number, chat_id, bot):
    kb = types.InlineKeyboardMarkup()
    if number != maxie:
        ans = list(get_questions()[0].values())[number]
        right = ans[0]
        random.shuffle(ans)
        if len(max(list(get_questions()[0].values())[number], key=len)) < 45:
            for q in ans:
                if q != right:
                    kb.add(types.InlineKeyboardButton(q, callback_data='false_answer'))
                else:
                    kb.add(types.InlineKeyboardButton(q, callback_data='right_answer'))
            bot.send_message(chat_id,
                             f'*{number+1}*. {list(get_questions()[0].keys())[number]}',
                             reply_markup=kb, parse_mode='Markdown')
        else:
            for i, q in enumerate(ans):
                if q != right:
                    kb.add(types.InlineKeyboardButton(i+1, callback_data='false_answer'))
                else:
                    kb.add(types.InlineKeyboardButton(i+1, callback_data='right_answer'))
            output = ''
            for i, q in enumerate(ans):
                output += f'{i+1} - {q}\n'
            bot.send_message(chat_id,
                             f'*{number}*. {list(get_questions()[0].keys())[number]}\n{output}',
                             reply_markup=kb, parse_mode='Markdown')

    else:
        kb.add(types.InlineKeyboardButton('Узнать результат'
                                          , callback_data='finish'))
        bot.send_message(chat_id,
                         'Вопросы закончились!',
                         reply_markup=kb)
