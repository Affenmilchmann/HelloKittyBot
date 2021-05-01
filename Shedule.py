import json, os
import operator
from time import strftime

from Post import Post

script_dir = os.path.dirname(__file__)

json_file = os.path.join(script_dir, "shedule.json")
history_file = os.path.join(script_dir, "logs/posted.txt")

class Shedule:
	def __init__(self):
		self.list = []
		self.loadList()

	def addPost(self, photo, caption, post_time_string):
		self.list.append(Post(photo, caption, post_time_string))

		self.saveList()

		if self.isAlreadyPosted(photo):
			return "There is already same posted photo. Post has been added to shedule though."

		return "Post has been sheduled."

	def delPost(self, index):
		del self.list[index]

		self.saveList()

		return "Post has been deleted."

	def showList(self):
		answer_string = ""

		for i in range(len(self.list)):
			answer_string += "\n"
			answer_string += "[Post " + str(i) + "]" + "\n"
			answer_string += "Time: " + self.list[i].post_time_string + "\n"
			answer_string += "Caption: " + self.list[i].caption + "\n"
			answer_string += "Photo: " + self.list[i].photo + "\n"

		if answer_string == "":
			answer_string = "There is no sheduled posts!\n"

		answer_string += "LocalTime: " + strftime("%Y-%m-%d %H:%M:%S") + "\n"

		return answer_string

	#this check all posts if its time to post them
	def checkPosts(self, token, channel_id):
		return_string = ""

		self.loadList()

		for i in range(len(self.list)):
			if self.list[i].isTime():
				result = self.list[i].sendPost(token, channel_id)
				if result == False:
					print(result)
				else:
					self.addToHistory(self.list[i].photo)

					return_string += "[Posted]\n"
					return_string += str(self.list[i].photo) + "\n"
					return_string += str(self.list[i].caption) + "\n"

					self.delPost(i)
					self.saveList()

					break

		return return_string

	def saveList(self):
		dicts = []

		self.sortListByDate()

		for p in self.list:
			dicts.append(p.toDict())

		json_string = json.dumps(dicts)

		f = open(json_file, "w")
		f.write(json_string)
		f.close()

	def loadList(self):
		self.list.clear()

		f = open(json_file, "r")
		json_string = f.read()
		f.close()

		if json_string != "":
			for d in json.loads(json_string):
				self.list.append(Post(d['photo'], d['caption'], d['post_time_string']))

	def sortListByDate(self):
		self.list.sort(key=operator.attrgetter('post_time_string'))

	def addToHistory(self, photo):
		with open(history_file, "a") as f:
			f.write("\n")
			f.write(photo)

	def isAlreadyPosted(self, photo):
		with open(history_file) as f:
			if photo in f.read():
				return True
		return False
