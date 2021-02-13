# -*- coding: utf-8 -*-

import os, time, random
from threading import Thread

if os.getenv("OS") in ["Windows_NT","Linux"]:
	import msvcrt as m


from req import *

# Начальные значения
x = 5
y = 3
game_thread = True
fruit_cord_x = 5
fruit_cord_y = 6
button_defult = "d"
score = 0
icon_player = "►"
tail = "o"
last2X = 0; last2Y = 0
lastX = 0; lastY = 0
elemX = [0 for i in range(100)]; elemY = [0 for i in range(100)]
api = Api()

def clear():
	if os.getenv("OS") == "Windows_NT":
		os.system("cls")
	elif os.getenv("OS") in [None,"Linux"]:
		os.system("clear")

def record(score: int):
	file = read_file()
	name = file["name"]
	try:
		for i in api.tasks()["tasks"]:
			if i["name"] == name:
				if score > i["score"]:
					api.upd_task(name=name, score=score, task_id=file["task_id"]) 
					return True
				break
	except requests.exceptions.ConnectionError: print("К сожалению ваше устройство не подключено к интернету, а это значит, что статистика не будет обновлена")



def gameover():
	global game_thread
	if record(score = score):
		print("\nGAME OVER\nВаши очки: {0} - НОВЫЙ РЕКОРД".format(score))
	else:
		print("\nGAME OVER\nВаши очки: {0}".format(score))
	game_thread = False
	exit()


def board(width: int = 40, height: int = 20, pos_player_x: int = x, pos_player_y: int = y):
	global score, fruit_cord_x, fruit_cord_y, game_thread, icon_player, last2X, lastX, lastY, last2Y, elemY, elemX
	clear()
	for i in range(height):
		for j in range(width):
			if pos_player_x == fruit_cord_x and pos_player_y == fruit_cord_y:
				fruit_cord_x = random.randint(5, width-1)
				fruit_cord_y = random.randint(5, height-1)
				score += 1

			for el in range(score):
				if pos_player_x == elemX[el] and pos_player_y == elemY[el]:
					gameover()

			if not(x in range(width-39)) and not(y in range(height-1)) or not(x in range(width-1)) and not(y in range(height-19)):
				gameover()		

			if j == 0:
				print("\t", end="")
				print('#', end='')
			elif i == 0:
				print('#', end='')
			elif i == height-1:
				print('#', end='')
			elif j == width-1:
				print('#', end='')
			elif pos_player_x == j and pos_player_y == i:
				print(icon_player, end='')
			elif fruit_cord_x == j and fruit_cord_y == i:
				print("*", end='')
			else:
				pr = True
				for ls in range(score):
					if elemX[ls] == j and elemY[ls] == i:
						print(tail, end="")
						pr = False
				if pr: print(' ', end='')

		print()
	# интерфейс
	print(f"\tОчки: {score}\n\n\t\tWASD / Стрелочки - перемещение\n\t\t\tESC - выйти")
	lastX = pos_player_x; lastY = pos_player_y
	if score > 0:
		for el in range(score):
			last2X = elemX[el]; last2Y = elemY[el]
			elemX[el] = lastX; elemY[el] = lastY
			lastX = last2X; lastY = last2Y

def button_move():	
	global button_defult
	if os.getenv("OS") in ["Windows_NT","Linux"]:
		while game_thread:
			button_defult = m.getch()[0]
	else: 
		while game_thread:
			button_defult = input("Нажмите кнопку перемещения: ")

def move():	
	global x, y, game_thread, button_defult, icon_player

	while game_thread:
		if button_defult in [""," "]: button_defult = "d"
		elif button_defult in ["w", 119, 230, 72]: y -= 1; icon_player = "▲"
		elif button_defult in ["a", 97, 228, 75]: x -= 1; icon_player = "◄"
		elif button_defult in ["s", 115, 235, 80]: y += 1; icon_player = "▼"
		elif button_defult in ["d", 100, 162, 77]: x += 1; icon_player = "►"

		elif button_defult in ["exit", 27]:
			print("Вы покинули игру\nВаши очки: {0} - выши очки не были засчитаны".format(score))
			game_thread = False
			exit()

		board(pos_player_x=x, pos_player_y=y)

		time.sleep(.2)


def main():
	board()
	Thread(target=move).start()
	Thread(target=button_move).start()

def menu():
	clear()
	print("Хех, это консольная змейка | Автор: feb\n\n\t\t1 - Играть\n\t\t2 - Рейтинговая таблица (в разработке)\n\t\t3 - Выход")
	if os.getenv("OS") in ["Windows_NT","Linux"]:
		btn = m.getch()[0]
	else: 
		btn = input("Выберите пункт: ")
	if btn in ["1", 49]:
		main()
	elif btn in ["2", 50]:
		pass
	elif btn in ["3", 51]:
		exit()

if __name__ == '__main__':
	# МЕНЮ
	try: 
		read_file()
	except: 
		status_auth = False
		while status_auth == False:
			try:
				clear()
				nickname = input("Система не обнаружила файл настроек\n\nПридумайте себе ник: ")
				if nickname not in ["", " "] and len(nickname) != 0: 
					task_id = api.new_task(name=nickname, score=0)["task_id"]
					write_file(name=nickname, task_id=task_id)
					status_auth = True
				else:
					print("ERROR: Поле осталось пустым. Исправьте это!")
					time.sleep(1.5)
			except requests.exceptions.ConnectionError: 
				print("К сожалению ваше устройство не подключено к интернету.\nПодключитесь к интернету и попробуйте ещё раз")
				time.sleep(2)


	menu()
