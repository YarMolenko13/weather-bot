from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps
from datetime import datetime



config = get_default_config()  # создали стандартный конфиг , чтобы изменить язык
config['language'] = 'ru'  # изменили язык
owm = OWM('488c435162b187b2632cda6bfe005d78', config)
mgr = owm.weather_manager()




def search_weather_data(city):
	# город , о ктором мы получим информацию о погоде
	weather = mgr.weather_at_place(city).weather

	temperature = int(weather.temperature('celsius')['temp'])  # получили температуру в градусах Цельсия
	if temperature > 25:
		temperature_smile = ' 🌡🔥'
	elif temperature >= 20 and int(temperature) <= 25:
		temperature_smile = ' 🌡🤤'
	elif temperature < 20 and int(temperature) >= 10:
		temperature_smile = ' 🌡😐'
	elif temperature < 10 and int(temperature) >= 0:
		temperature_smile = ' 🌡☹'
	else:
		temperature_smile = ' 🌡❄'

	temperature = str(temperature) + '℃' + temperature_smile

	wind_ms = str(int(weather.wind()['speed']))
	if int(wind_ms) > 6:
		wind_smile = '🌪'
	else:
		wind_smile = ' 💨'

	wind_kmh = weather.wind(unit='km_hour')['speed']
	wind_kmh = str(int(wind_kmh)) + 'км/ч' + wind_smile

	weather_status = weather.detailed_status.capitalize()
	weather_status_smile = ''
	if weather_status == 'Пасмурно':
		weather_status_smile = ' 🌥'
	if weather_status == 'Ясно':
		weather_status_smile = ' ☀'
	if weather_status == 'Небольшой дождь':
		weather_status_smile = ' 💧'
	if weather_status == 'Небольшая облачность':
		weather_status_smile = ' ⛅'
	if weather_status == 'Облачно с прояснениями':
		weather_status_smile = ' 🌤'
	if weather_status == 'Переменная облачность':
		weather_status_smile = ' ☀☁'
	if weather_status == 'Мгла':
		weather_status_smile = ' 🌫'
	if weather_status == 'Гроза с небольшим дождём':
		weather_status_smile = ' ⛈'
	if weather_status == 'Гроза с дождём':
		weather_status_smile = ' ⛈'
	if weather_status == 'Гроза':
		weather_status_smile = ' 🌩'
	weather_status = weather_status + weather_status_smile

	final_message = ('''Вот информация о погоде в городе {0}:
		Температура - {1}
		Скорость ветра - {2}м/с или же {3}
		{4}'''.format(city, temperature, wind_ms, wind_kmh, weather_status))

	return final_message

def notif_forecast(city):
	
	forecaster = mgr.forecast_at_place(city, '3h')
	weather = mgr.weather_at_place(city).weather
	temperature = int(weather.temperature('celsius')['temp'])
	temperature = str(temperature) + '℃'
	is_rain_today = forecaster.will_be_rainy_at(datetime.today())
	is_rain_today_mesasge = '[ информация не получена ]'
	try:
		if is_rain_today:
			is_rain_today_message = 'ожидается дождь'
		else:
			is_rain_today_mesasge = 'дождя не ожидается'
	except:
		is_rain_today_mesasge = '[ информация не получена ]'
	weather_status = weather.detailed_status
	# is_rain_tomorrow = forecaster.will_be_rainy_at(timestamps.tomorrow)
	final_message = '''Информация о погоде на сегодня:
{0}, {1}, {2}'''.format(weather_status, is_rain_today_mesasge, temperature)
	return final_message




# def notif_forecast(city):
# 	try:
# 		forecaster = mgr.forecast_at_place(city, '3h')
# 		weather = mgr.weather_at_place(city).weather

# 		temperature = int(weather.temperature('celsius')['temp'])
# 		temperature = str(temperature) + '℃'
# 		is_rain_today = forecaster.will_be_rainy_at(datetime.today())
# 		is_rain_today_mesasge = '[ информация не получена ]'
# 		try:
# 			if is_rain_today:
# 				is_rain_today_message = 'ожидается дождь'
# 			else:
# 				is_rain_today_mesasge = 'дождя не ожидается'
# 		except:
# 			is_rain_today_mesasge = '[ информация не получена ]'
# 		weather_status = weather.detailed_status
# 		# is_rain_tomorrow = forecaster.will_be_rainy_at(timestamps.tomorrow)

# 		final_message = '''Информация о погоде на сегодня:
# {0}, {1}, {2}'''.format(weather_status, is_rain_today_mesasge, temperature)
# 		return final_message
# 	except:
# 		return 'Ошибка. Возможны вы ввели город,\nкоторого нет в моем бд ('


# def is_soon_rain(city):
# 	try:
# 		forecast = mgr.forecast_at_place(city, '3h')

# 		hour = timestamps.next_hour()
# 		will_be_rain_next_hour = forecast.will_be_rainy_at(hour)
# 		if will_be_rain_next_hour:
# 			return True
# 	except:
# 		return 'err'