from Shedule import Shedule
from time import strftime
from myWebFuncs import getUpdates, sendMessage, sendPhoto, sendDocument
from log import *

from time import sleep

ANSWER_INTERVAL = 3 #seconds
POST_CHECK_INTERVAL = 1000 #seconds

class Bot:
	def __init__(self, token, owner_id, channel_id):
		self.token = token
		self.owner_id = owner_id
		self.channel_id = channel_id
		#keep track of the lst update to request only new updates
		self.last_update_id = 0
		#Shedule loads shedule from file defined in Shedule.py
		self.shedule = Shedule()

		#to manage stage of photoAddFunc is going
		self.photo_add_stage = 0
		self.photo_add_data = {}

		#to manage stage of delSheduledPostFunc
		self.del_stage = 0
		self.del_id = -1

		#time managment
		self.time_passed_since_post_check = POST_CHECK_INTERVAL

		consoleOutput("Bot is active.")
		self.sendMessageToOwner("Bot is active.")

	def mainLoop(self):
		self.updatesHandler()

		if self.time_passed_since_post_check >= POST_CHECK_INTERVAL:
			self.postingHandler()
			self.time_passed_since_post_check -= POST_CHECK_INTERVAL

		self.time_passed_since_post_check += ANSWER_INTERVAL
		sleep(max(ANSWER_INTERVAL, 0))

	def postingHandler(self):
		result = self.shedule.checkPosts(self.token, self.channel_id)

		if result != "":
		    self.sendMessageToOwner(result)
		    consoleOutput(str(result))
		else:
		    consoleOutput("Nothing posted")

	def updatesHandler(self):
		#getting updates
		# + 1 means that we are requesting updates only after the last one
		updates = getUpdates(self.token, self.last_update_id + 1)
		
		#checking if there an error
		if not updates['ok']:
			self.sendMessageToOwner("[" + strftime("%Y-%m-%d %H:%M:%S") + "] Error while trying to get updates here is telegram`s answer.\n" + updates)
		else:
			#leaving only needed part
			updates = updates["result"]
			#running through all updates
			for upd in updates:
				#answer them only if update has a text
				if "message" in upd:
					if str(upd["message"]["from"]["id"]) == str(self.owner_id):
						self.adminUpdates(upd)
					else:
						self.userUpdates(upd)

			#getting last update`s id bc we dont want to run it twice
			if len(updates) > 0:
				self.last_update_id = updates[-1]["update_id"]

	def adminUpdates(self, upd):
		if "text" in upd["message"]:
			#sending text to the next step. Recognising the command
			self.replyHandler(upd["message"]["text"])
			
	def userUpdates(self, upd):
		user_id = upd["message"]["from"]["id"]
		if "username" in upd["message"]["from"]:
			user_name = "@" + str(upd["message"]["from"]["username"])
		else:
			user_name = "UID:" + user_id
		
		if ("photo" not in upd["message"]) and ("document" not in upd["message"]) or ("document" in upd["message"] and "photo" in upd["message"]): #its just xor
			msgLog(upd["message"], str(user_name) + "(" + str(user_id) + ")", "Bot")
			self.sendMessageToUser(user_id, "Это не похоже на фото... \nПросто отправьте мне фото. Можно файлом.\n \n" + 
								   "Если вы считаете, что отправили фото, но видите это сообщение, можете стукнуть админа(@affenmilchmann) по голове ибо он плохой кодер. " + 
								   "Просто перешлите ему наши сообщения")
			return
			
		if "photo" in upd["message"]:
			photo_obj = upd["message"]["photo"]
			msgLog("Photo " + str(photo_obj), str(user_name) + "(" + str(user_id) + ")", "Bot")
			#there are a row of photos in different size. Last one is the biggest one
			photo = photo_obj[-1]
			result = sendPhoto(self.token, self.owner_id, photo["file_id"], str(user_name) + "\n" + str(photo["file_id"]))
			
		elif "document" in upd["message"]:
			document = upd["message"]["document"]
			msgLog("Document " + str(document), str(user_name) + "(" + str(user_id) + ")", "Bot")
			result = sendDocument(self.token, self.owner_id, document["file_id"], str(user_name) + "\n" + str(document["file_id"]))
			
		else:
			self.sendMessageToOwner("Чел как так\n" + str(upd))
			self.sendMessageToUser(user_id, "Произошла очень странная вещь в коде, ибо админ плохо меня закодил. Я уже сказал ему об этой ошибке")
			
		if result == False:
			consoleOutput(str(result))
			self.sendMessageToOwner("I`ve tried to send you a user photo, but smthg went wrong.\n User " + str(user_name) + "\n" + result)
			self.sendMessageToUser(user_id, "Something went wrong. I`ve sent a message to admin about it\nЧто-то пошло не так, я уже уведомил админа об этом")
		else:
			self.sendMessageToUser(user_id, "Я отправил фото админу!\nСпасибо большое!")
				
	def replyHandler(self, command):
		consoleOutput("OwnerMessage " + str(command))

	

		if command.lower() == "help":
			self.sendMessageToOwner(self.formHelpMenu())

		elif command.lower() == "add" or self.photo_add_stage > 0:
			self.photoAddFunc(command)

		elif command.lower() == "show":
			self.sendMessageToOwner(self.shedule.showList())

		elif command.lower() == "del" or self.del_stage > 0:
			self.delSheduledPostFunc(command)

		#elif command.lower() 

		else:
			self.sendMessageToOwner("I cant understand you...")


	def formHelpMenu(self):
		out_string = ""

		out_string += "Here is some commands I can recognize:\n"
		out_string += "	show (to see the shedule)\n"
		out_string += "	add (to add a new post to the shedule)\n"
		out_string += "	del (to edelete a new post from the shedule)\n"

		out_string += "	help (to show this menu)"

		return out_string

	def delSheduledPostFunc(self, command):
		if command.lower() == "del":
			self.sendMessageToOwner("Send me an id of the post")
			self.del_stage = 1

		elif self.del_stage == 1:
			try:
				self.del_id = int(command)
			except ValueError:
				self.sendMessageToOwner("Its not a number!")
			else:
				if self.del_id < 0 or self.del_id >= len(self.shedule.list):
					self.sendMessageToOwner("Its not a valid id!")
				else:
					self.del_stage = 2
					self.sendMessageToOwner("Are you shure that you want to delete it? (y/n)")

		elif self.del_stage == 2:
			if command.lower() == "y":
				self.shedule.delPost(self.del_id)
				self.sendMessageToOwner("Post has been deleted!")
			else:
				self.sendMessageToOwner("Ok! Nothing will be deleted!")

			self.del_stage == 0
			self.del_id = -1


	def photoAddFunc(self, command):
		if command.lower() == "add":
			self.sendMessageToOwner("Send me a photo link please")
			self.photo_add_stage = 1

		elif self.photo_add_stage == 1:
			self.photo_add_data["photo"] = command
			self.photo_add_stage = 2
			self.sendMessageToOwner("Send me a caption please")

		elif self.photo_add_stage == 2:
			self.photo_add_data["caption"] = command
			self.photo_add_stage = 3
			self.sendMessageToOwner("Send me when the post must be posted. In format Year-Mounth-Day Hours:Minutes:Seconds")

		elif self.photo_add_stage == 3:
			self.photo_add_data["post_time_string"] = command
			self.photo_add_stage = 0

			answer = self.shedule.addPost(
				self.photo_add_data["photo"],
				self.photo_add_data["caption"],
				self.photo_add_data["post_time_string"]
			)

			self.sendMessageToOwner(answer)

	def sendMessageToUser(self, user_id, text):
		sendMessage(self.token, user_id, text)
		msgLog(text, "Bot", str(user_id))
		consoleOutput("Message sent to user " + str(user_id) + ". Message: '" + text + "'")

	def sendMessageToOwner(self, text):
		sendMessage(self.token, self.owner_id, text)
