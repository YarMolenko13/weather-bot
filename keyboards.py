from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# стартовая кнопка
btn_start = KeyboardButton('Начать')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_start)

# кнопки со входами в функции бота
btn_weather_now = KeyboardButton('Узнать погоду')
btn_sub_on_notion_menu = KeyboardButton('Настройка уведомлений')
kb_main = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_weather_now, btn_sub_on_notion_menu)

# кнопки для работы с уведомлениями
btn_sub_yes = InlineKeyboardButton('Включить ✅', callback_data='sub_yes')
btn_sub_no= InlineKeyboardButton('Выключить ❌', callback_data='sub_no')
kb_sub_yes_or_no = InlineKeyboardMarkup(row_width=2).row(btn_sub_yes, btn_sub_no)

# инлайн клавиатура городов
btn_city_1 = KeyboardButton('Москва')
btn_city_2 = KeyboardButton('Санкт-Петербург')
btn_city_3 = KeyboardButton('Калининград')
btn_city_4 = KeyboardButton('Нижний Новгород')
btn_city_exite = KeyboardButton('Выйти')

kb_of_cities = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(btn_city_1, btn_city_2).row(btn_city_3, btn_city_4).add(btn_city_exite)

# инлайн кнопка подтверждения
# btn_confirm_city = InlineKeyboardButton('Подтверидть', callback_data='btn_confirm_city')
# kb_confirm_city = InlineKeyboardMarkup(row_width=1).add(btn_confirm_city)
