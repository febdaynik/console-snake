import requests, json

class Api:

	def __init__(self):
		self.url = "http://febday.pythonanywhere.com/"
		self.username = "admin"
		self.password = "12223admin"

	def signin(self):
		res = requests.post(self.url+"signin/", {"username":self.username, "password":self.password})
		return res.json()

	def tasks(self):
		res = requests.get(self.url+"all/", headers={"Authorization":self.signin()["token"]})
		return res.json()

	def new_task(self, name: str, score: int):
		res = requests.post(self.url+"new/", {"name": name, "due_in": 0, "score": score}, headers={"Authorization":self.signin()["token"]})
		return res.json()

	def upd_task(self, name: str, score: int, task_id: int):
		res = requests.post(self.url+"update/", {"task_id":task_id, "name": name, "due_in": 0, "score": score}, headers={"Authorization":self.signin()["token"]})
		return res.json()

def read_file():
	file = open('settings.txt', 'r+')
	read = file.read()
	return json.loads(read)

def write_file(name: str, task_id: int = 0):
	file = open('settings.txt', 'w+')
	file.write('{"name": "'+name+'", "task_id": '+str(task_id)+'}')
	return True

if __name__ == '__main__':
	# print(read_file()["name"])
	api = Api()
	for i in api.tasks()["tasks"]:
		print(i)

