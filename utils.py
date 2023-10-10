import json


def read_file():
	file = open('settings.txt', 'r+')
	read = file.read()
	return json.loads(read)


def write_file(name: str, task_id: int = 0):
	file = open('settings.txt', 'w+')
	file.write('{"name": "'+name+'", "task_id": '+str(task_id)+'}')
	return True
