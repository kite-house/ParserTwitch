from parserTwitch import get_streamers, get_game_id
from src.createExcelTable import save_in_excel
import asyncio
import os
from art import tprint

try:
	tprint('WELCOME')
	game_name = input("Введите название игры: ")

	os.system('cls')
	print('Формируем ответ, ожидайте!')
	data = asyncio.run(get_streamers(get_game_id(game_name)))

	os.system('cls')
	print('Ответ получен! Создаем Excel таблицу, и записываем туда ответ')
	save_in_excel(game_name, data)

	os.system('cls')
	print(f'Данные успешно сохранены в Excel Таблицу {game_name}.xlsx')

except Exception as error:
	os.system('cls')
	print(f"Ошибочка: {error}")
      
input()