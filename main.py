import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('6605211662:AAFG69LG5eruHg0nOrx6YheE_XdDsr3U8hw')
PM_lips = ''
PM_brows = ''
PM_lashes = ''
Lashes = ''
Brows = ''
Name = ''
Phone = ''
Username = ''

markup_check = types.InlineKeyboardMarkup()
check = types.InlineKeyboardButton(text='Проверить отправленные данные', callback_data='check_in')
markup_check.add(check)

choice = types.InlineKeyboardMarkup()
yes = types.InlineKeyboardButton(text='Да ✅', callback_data='yes')
no = types.InlineKeyboardButton(text='Нет ❌', callback_data='no')
choice.add(yes, no)

mainmenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
note = types.KeyboardButton('Запись на процедуру')
contacts = types.KeyboardButton('Контакты и режим работы')
price = types.KeyboardButton('Прайс')
mainmenu.add(note, contacts, price)

one_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
back = types.KeyboardButton('Назад ↩')
one_button.add(back)

menu_procedure = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
pm = types.KeyboardButton('Перманентный макияж')
brows = types.KeyboardButton('Архитектура, окрашивание, ламинирование бровей')
lash = types.KeyboardButton('Окрашивание и ламинирование ресниц')
back1 = types.KeyboardButton('Назад ↩')
menu_procedure.add(pm, brows, lash, back1)


print("Bot started")


@bot.message_handler(commands=['start'])
def menu(message):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS requests (id int auto_increment primary key, username varchar(50), "
                "name varchar(50), phone varchar(13), procedure varchar(60))")

    img = open('logo_L.png', 'rb')
    text = '<b>Здравствуйте!</b> 🌿\n\nВ этом боте Вы можете записаться на процедуру к Екатерине Лоренгель'
    bot.send_photo(message.from_user.id, img, caption=text, parse_mode='html', reply_markup=mainmenu)

    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(content_types=['text'])
def services(message):
    if message.text == 'Запись на процедуру':
        msg = bot.send_message(message.from_user.id, 'Выберите тип процедуры', parse_mode='html',
                               reply_markup=menu_procedure)
        bot.register_next_step_handler(msg, entry)

    elif message.text == 'Контакты и режим работы':
        bot.send_message(message.chat.id, 'Услуги осуществляются по адресу:\n\n_Северное Шоссе, 10, Plaza '
                                          'Ramstars, кабинет 204, 2 этаж_\n\nЗапись с 10 до 20 пн-сб\nЗвоните'
                                          ' +7(958)639-39-20\nВКонтакте: [lorengel_pm]'
                                          '(https://vk.com/lorengel_pm)',
                         parse_mode='Markdown', reply_markup=one_button)
    elif message.text == 'Прайс':
        pricelist = open('priceweb.png', 'rb')
        bot.send_photo(message.chat.id, pricelist, reply_markup=one_button)
    elif message.text == 'Назад ↩':
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню ✔', reply_markup=mainmenu)


def entry(message):
    if message.text == 'Перманентный макияж':
        butt = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        lips = types.KeyboardButton('Губы')
        brow_but = types.KeyboardButton('Брови')
        lashes_but = types.KeyboardButton('Заполнение межресничного пространства')
        back2 = types.KeyboardButton('Назад ↩')
        butt.add(lips, brow_but, lashes_but, back2)
        msg = bot.send_message(message.chat.id, 'Выберите вид перманентного макияжа', parse_mode='html',
                               reply_markup=butt)
        bot.register_next_step_handler(msg, typepm)
    elif message.text == 'Архитектура, окрашивание, ламинирование бровей':
        global Brows
        Brows = message.text
        msg = bot.send_message(message.chat.id, 'Напишите, как я могу к Вам обращаться')
        bot.register_next_step_handler(msg, request_phone)
    elif message.text == 'Окрашивание и ламинирование ресниц':
        global Lashes
        Lashes = message.text
        msg = bot.send_message(message.chat.id, 'Напишите, как я могу к Вам обращаться')
        bot.register_next_step_handler(msg, request_phone)
    elif message.text == 'Назад ↩':
        msg = bot.send_message(message.chat.id, 'Вы вернулись в главное меню ✔', parse_mode='html',
                               reply_markup=mainmenu)
        bot.register_next_step_handler(msg, entry)


def typepm(message):
    if message.text == 'Губы':
        global PM_lips
        PM_lips = 'Перманентный макияж губ'
        msg = bot.send_message(message.chat.id, 'Напишите, как я могу к Вам обращаться')
        bot.register_next_step_handler(msg, request_phone)

    elif message.text == 'Брови':
        global PM_brows
        PM_brows = 'Перманентный макияж бровей'
        msg = bot.send_message(message.chat.id, 'Напишите, как я могу к Вам обращаться')
        bot.register_next_step_handler(msg, request_phone)

    elif message.text == 'Заполнение межресничного пространства':
        global PM_lashes
        PM_lashes = message.text
        msg = bot.send_message(message.chat.id, 'Напишите, как я могу к Вам обращаться')
        bot.register_next_step_handler(msg, request_phone)

    elif message.text == 'Назад ↩':
        msg = bot.send_message(message.chat.id, 'Выберите тип процедуры', parse_mode='html',
                               reply_markup=menu_procedure)
        bot.register_next_step_handler(msg, entry)


def request_phone(message):
    global Name
    global Username
    Name = message.text
    Username = message.from_user.username
    number = bot.send_message(message.chat.id, 'Введите, пожалуйста, Ваш номер телефона для связи в формате '
                                               '+7(XXX)XXX-XX-XX')
    bot.register_next_step_handler(number, create_request)


def create_request(message):
    global Phone
    Phone = message.text
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO requests (username, name, phone, procedure) VALUES ('%s', '%s', '%s', '%s')"
                % (Username, Name, Phone, PM_lips or PM_brows or PM_lashes or Brows or Lashes))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Отлично! Давайте проверим Ваши данные.', parse_mode='html',
                     reply_markup=markup_check)

    if message.text == 'Назад ↩':
        bot.send_message(message.chat.id, 'Вы вернулись в главное меню ✔', reply_markup=mainmenu)


@bot.callback_query_handler(func=lambda call: True)
def check_in(call):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM requests ORDER BY id DESC LIMIT 1')
    request = cur.fetchone()
    username = request[1]
    name = request[2]
    phone = request[3]
    procedure = request[4]

    if call.data == "check_in":
        bot.answer_callback_query(callback_query_id=call.id, text='Секунду...')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'<b>Ваше имя:</b> {name}\n<b>Ваш номер телефона:</b> {phone}\n'
                                   f'<b>'f'Тип процедуры:</b> {procedure}\n\nВсё верно?', parse_mode='html',
                              reply_markup=choice)
    elif call.data == 'yes':
        bot.answer_callback_query(callback_query_id=call.id, text='Отлично, Ваша заявка доставлена!', show_alert=True)
        keyboard_3 = types.InlineKeyboardMarkup()
        callback_button_1 = types.InlineKeyboardButton(text="В главное меню", callback_data="mainmenu")
        keyboard_3.add(callback_button_1)
        bot.send_message(call.from_user.id, '<b>Спасибо за заявку!</b> 🌿 \nЯ свяжусь с Вами в ближайшее время для '
                                            'выбора даты и времени записи!', parse_mode='html', reply_markup=keyboard_3)
        bot.send_message(-1001887088441, f'<b>Новая заявка!</b>\nTelegram: @{username}\nИмя: {name}\nТелефон: '
                                         f'{phone}\nТип процедуры: '
                                         f'{procedure}', parse_mode='html')
    elif call.data == 'no':
        text = 'Вернуться в главное меню'
        keyboard_3 = types.InlineKeyboardMarkup()
        callback_button_1 = types.InlineKeyboardButton(text="В главное меню", callback_data="mainmenu")
        keyboard_3.add(callback_button_1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                              reply_markup=keyboard_3)
    elif call.data == 'mainmenu':
        bot.send_message(call.message.chat.id, 'Вы вернулись в главное меню ✔', reply_markup=mainmenu)

    cur.close()
    conn.close()


bot.polling(none_stop=True)
