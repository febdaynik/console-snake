import os, time, random
from threading import Thread
import msvcrt as m

from req import *

# Начальные значения
game_thread = True
delay = .2
px = 9
py = 7
icon_player = "►"
icon_player_dop = "o"
icon_object = "@"
button_defult = "d"
score = 0
spawn_object = False
api = Api()

arr = [
	["\t\t#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],[" "],["#\n"],
	["\t\t#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#"],["#\n"],
]


# Старая версия границ
def border():
	width = 35
	height = 15

	for bh in range(height):
		if bh in [0, 14]:
			for bw in range(width):
				if bw == 34:
					print("#")
				else:
					print("#", end="")
		else:
			for bw in range(width):
				if bw == 0:
					print("#", end="")
				elif bw == 34:
					print("#")
				else:
					print(" ",end="")

def position_player():
	return random.randint(7,12), random.randint(3,9)

def position_object():
	return random.randint(7,25), random.randint(3,9)

def find_object():
	global spawn_object
	for i in arr:
		if i[0].find(icon_object) != -1:
			spawn_object = True

# Новая версия границ
def board(pos_player: int = px*py):
	# начинается с 28
	# размер 27x13 (27 - ширина, 13 - высота)

	pox, poy = position_object()
	find_object() # вкусняшка
	# генерация игрока
	if arr[pos_player][0] == " ":
		# Голова
		arr[pos_player].remove(" ")			
		arr[pos_player].append(icon_player)

	# генерация вкусняшки
	if arr[pox*poy][0] == " " and not spawn_object:
		arr[pox*poy].remove(" ")			
		arr[pox*poy].append(icon_object)

	os.system('cls') #clear
	print("\n\n")
	for i in arr:
		print(i[0],end="")

def record(score: int):
	file = read_file()
	name = file["name"]
	for i in api.tasks()["tasks"]:
		if i["name"] == name:
			if score > i["score"]:
				api.upd_task(name=name, score=score, task_id=file["task_id"]) 
				return True
			break


def button_move():
	global button_defult
	while game_thread:
		button_defult = m.getch()[0]

def move():
	sumxy = px*py
	global button_defult, game_thread, score, spawn_object, delay, icon_player
	while game_thread:
		# проверка на текующее положение игрока и границы
		if arr[sumxy][0] == icon_player:
			arr[sumxy].remove(icon_player)
			arr[sumxy].append(" ")
		elif arr[sumxy][0] in ["#","\t\t#", "#\n"]:
			if record(score = score):
				print("\nGAME OVER\nВаши очки: {0} - НОВЫЙ РЕКОРД".format(score))
			else:
				print("\nGAME OVER\nВаши очки: {0}".format(score))
			game_thread = False
			exit()
		elif arr[sumxy][0] == icon_object:
			arr[sumxy].remove(icon_object)
			arr[sumxy].append(" ")
			score += 1
			if score%10 == 0 and score != 0:
				delay -= .01
			spawn_object = False

		# w - 119, a - 97, s - 115, d - 100, esc - 27
		# |w - 72, < - 75, |s - 80, > - 77
		# ц - 230,ф - 228,ы - 235,в - 162
		# перемещение змейки по полю
		if button_defult in [""," "]: button_defult = "d"
		elif button_defult in ["w", 119, 230, 72]: sumxy -= 27; icon_player = "▲"
		elif button_defult in ["a", 97, 228, 75]: sumxy -= 1; icon_player = "◄"
		elif button_defult in ["s", 115, 235, 80]: sumxy += 27; icon_player = "▼"
		elif button_defult in ["d", 100, 162, 77]: sumxy += 1; icon_player = "►"
		elif button_defult in ["exit", 27]:
			print("Вы покинули игру\nВаши очки: {0} - выши очки не были засчитаны".format(score))
			game_thread = False
			exit()
		else: button_defult = "d"

		board(pos_player=sumxy)

		# Интерфейс
		print(f"\n\t\t\tОчки: {score}\n\n\t\tWASD / Стрелочки - перемещение\n\t\t\tESC - выйти")

		time.sleep(delay)


def main():
	Thread(target=move).start()
	Thread(target=button_move).start()

def menu():
	os.system('cls') #clear
	print("Хех, это консольная змейка | Автор: feb\n\n\t\t1 - Играть\n\t\t2 - Рейтинговая таблица (в разработке)\n\t\t3 - Выход")
	btn = m.getch()[0]
	if btn == 49:
		main()
	elif btn == 50:
		pass
	elif btn == 51:
		exit()

if __name__ == '__main__':
	# МЕНЮ
	try: 
		read_file()
	except: 
		status_auth = False
		while status_auth == False:
			os.system('cls')
			nickname = input("Система не обнаружила файл настроек\n\nПридумайте себе ник: ")
			if nickname not in ["", " "] and len(nickname) != 0: 
				task_id = api.new_task(name=nickname, score=0)["task_id"]
				write_file(name=nickname, task_id=task_id)
				status_auth = True
			else:
				print("ERROR: Поле осталось пустым. Исправьте это!")
				time.sleep(1.5)

	menu()



