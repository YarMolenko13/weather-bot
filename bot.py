from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import asyncio
from datetime import datetime

from config import *
from weather import *
from db import Postgers
import keyboards as kb


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())

# соединение с бд
db = Postgers()


# query хэндлеры
@dp.callback_query_handler(lambda c: c.data == 'sub_yes')
async def user_choose_sub_yes(callback_query: types.CallbackQuery):
	db.set_state(callback_query.from_user.id, 5)
	await bot.answer_callback_query(callback_query.id, text='Сначала введите город!')
	await bot.send_message(callback_query.from_user.id, 'Введите город🏙 и время⌚, когда вам будут\nприходить уведомления. Например: "Москва 15:30"')


@dp.callback_query_handler(lambda c: c.data == 'sub_no')
async def user_choose_sub_no(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id, text='Теперь уведомления не будут приходить')
	db.unsubscribe(callback_query.from_user.id)
	await bot.send_message(callback_query.from_user.id, 'Вы отключили уведомления ❌')


# commands хэндлеры
@dp.message_handler(commands=['start'])
async def process_start_cmd(message: types.Message):
	text = 'Привет 😀. Чтобы я заработал нажми на кнопку )'
	db.set_state(message.from_user.id, 1)
	await message.reply(text, reply_markup=kb.kb_start)


@dp.message_handler(commands=['restart'])
async def process_restart_cmd(message: types.Message):
	text = 'Я перезапустился!'
	db.set_state(message.from_user.id, 0)
	await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['patch_notes'])
async def show_all_patch_notes(message: types.Message):
	text = ''
	for key in patches:
		text = text + key + ': \n  Дата: ' + str(patches[key]['patch_date']) \
			   + '\n  Изменения: ' + str(patches[key]['patch_innovations']) + '\n\n'
	await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['patch_actual'])
async def show_actual_patch_notes(message: types.Message):
	text = str(version)
	text = text + ': \n  Дата: ' + str(patches[version]['patch_date']) \
		   + '\n  Изменения: ' + str(patches[version]['patch_innovations'])
	await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['version'])
async def show_version(message: types.Message):
	text = 'Версия бота : ' + str(version)
	await bot.send_message(message.from_user.id, text)


# обрабатываем состояния
@dp.message_handler(lambda message: db.get_current_state(message.from_user.id) == 1)
async def all_funcs_bot(message: types.Message):
	db.set_state(message.from_user.id, 2)
	await message.reply('Вот все функции бота', reply_markup=kb.kb_main)


@dp.message_handler(lambda message: message.text == 'Узнать погоду' and db.get_current_state(message.from_user.id) == 2)
async def watch_weather_now(message: types.Message):
	text = 'Введи город 🏙, погоду в котором ты хочешь узнать'
	db.set_state(message.from_user.id, 3)
	await message.reply(text, reply_markup=kb.kb_of_cities)


@dp.message_handler(lambda message: db.get_current_state(message.from_user.id) == 3)
async def user_input_city(message: types.Message):
	# StateDb.set_state(message.from_user.id, 2)
	try:
		if message.text == 'Узнать погоду':
			text = 'Пожалуйста, введите город или нажмите на кнопку👇'
			await bot.send_message(message.from_user.id, text)

		elif message.text == 'Выйти':
			db.set_state(message.from_user.id, 2)
			# await bot.send_message(message.from_user.id, text='Вы вышли в меню с главными функциями')
			await message.reply(text='Вы вышли в меню с главными функциями', reply_markup=kb.kb_main)
		else:
			text = search_weather_data(message.text)
			await bot.send_message(message.from_user.id, text)
	except:
		text = 'В мое базе данных нет такого города 😕'
		await bot.send_message(message.from_user.id, text)


@dp.message_handler(lambda message: db.get_current_state(message.from_user.id) == 5)
async def user_input_city_notion(message: types.Message):
	# сделать проверку на город ли это
	# сделать проверку на формат времени
	city = message.text.split(' ')[0]
	time = message.text.split(' ')[1]
	text = 'Отлично! Уведомления подключены'
	db.subscribe(message.from_user.id,time, city)
	db.set_state(message.from_user.id, 2)
	await message.reply(text, reply_markup=kb.kb_main)


@dp.message_handler(lambda message: message.text == 'Настройка уведомлений' and db.get_current_state(message.from_user.id) == 2)
async def sub_on_notion(message: types.Message):
	text = 'Хотите включить или выключить уведомления о погоде 🤔?'
	await message.reply(text, reply_markup=kb.kb_sub_yes_or_no)


# таймер
# async def scheduled(wait_for):
# 	while True:
# 		await asyncio.sleep(wait_for)
# 		now_hr = int(str(datetime.today().time()).split(':')[0])
# 		now_mn = int(str(datetime.today().time()).split(':')[1])
#
# 		# попробывать совместить два цикла
# 		for user in db.get_sub_users():
# 			not_time_hr = int(db.get_not_time_list(user[0], True)[0])
# 			not_time_mn = int(db.get_not_time_list(user[0], True)[1])
#
#
# 			if now_hr == not_time_hr and now_mn == not_time_mn:
# 				text = notif_forecast(str(db.get_city(user[0])))
# 				await bot.send_message(user[0], text, disable_notification=True)


if __name__ == '__main__':
	# dp.loop.create_task(scheduled(60))
	executor.start_polling(dp)
