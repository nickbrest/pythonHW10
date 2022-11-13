import telebot
from telebot import types
from access import token

bot = telebot.TeleBot(token)

user_num1 = ''
user_num2 = ''
user_operation = ''
user_result = None


@bot.message_handler(commands = ['start'] )

def send_first_message(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Вы в чате бота-калькулятора!\n\
Для получения результата вводите числа и нажимайте на кнопки действия.')
    msg = bot.send_message(message.chat.id, 'Введите первое число:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)


def process_num1_step(message, user_result = None):
    try:
        global user_num1
        if user_result == None:
            user_num1 = int(message.text)
        else:
            user_num1 = str(user_result)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        itembutton1 = types.KeyboardButton('+')
        itembutton2 = types.KeyboardButton('-')
        itembutton3 = types.KeyboardButton('*')
        itembutton4 = types.KeyboardButton('/')
        itembutton5 = types.KeyboardButton('**')
        markup.add(itembutton1, itembutton2, itembutton3, itembutton4, itembutton5)

        msg = bot.send_message(message.chat.id, 'Выберите операцию', reply_markup=markup)
        bot.register_next_step_handler(msg, process_operation_step)
    except Exception:
        bot.reply_to(message, 'Вводите число!')
        msg = bot.send_message(message.chat.id, 'Введите первое число:')
        bot.register_next_step_handler(msg, process_num1_step)


def process_operation_step(message):
    global user_operation
    user_operation = message.text
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Введите еще число:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num2_step)


def process_num2_step(message):
    try:
        global user_num2
        user_num2 = int(message.text)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembutton1 = types.KeyboardButton('Результат')
        itembutton2 = types.KeyboardButton('Дополнительная операция')
        markup.add(itembutton1, itembutton2)

        msg = bot.send_message(message.chat.id, "Выводим результат или необходима дополнительная операция?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception:
        bot.reply_to(message, "Вводите число!")
        msg = bot.send_message(message.chat.id, "Введите еще число:")
        bot.register_next_step_handler(msg, process_num2_step)


def process_alternative_step(message):
    try:
        calc()
        
        markup = types.ReplyKeyboardRemove(selective=False)
        
        if message.text == 'Результат':
            bot.send_message(message.chat.id, print_calculator(), reply_markup=markup)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembutton1 = types.KeyboardButton('Продолжаем')
            itembutton2 = types.KeyboardButton('Выход')
            markup.add(itembutton1, itembutton2)
            msg = bot.send_message(message.chat.id, "Продолжаем или выходим?", reply_markup=markup)
            bot.register_next_step_handler(msg, choice)
        elif message.text == 'Дополнительная операция':
            process_num1_step(message, user_result)
    except Exception:
        bot.reply_to(message, "Ошибка!")


def print_calculator():
    global user_num1, user_num2, user_operation, user_result
    return f'Результат: {str(user_num1)} {user_operation} {str(user_num2)} = {str(user_result)}'


def calc():
    global user_num1, user_num2, user_operation, user_result
    user_result = eval(str(user_num1) + user_operation + str(user_num2))
    return user_result


def choice(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text == 'Продолжаем':
        msg = bot.send_message(message.chat.id, 'Введите первое число:')
        bot.register_next_step_handler(msg, process_num1_step)
    else:
        bot.reply_to(message, "Чао, бамбини!", reply_markup=markup)
        exit()

print('start bot')

bot.polling(none_stop=True, interval=0)

