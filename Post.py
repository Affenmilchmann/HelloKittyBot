from time import strftime
from datetime import datetime
from myWebFuncs import sendPhoto

class Post:
	def __init__(self, photo, caption, post_time_string): #string format %Y-%m-%d %H:%M:%S
		self.photo = photo
		self.caption = caption
		self.post_time_string = post_time_string

	def sendPost(self, token, channel_id):
		res = sendPhoto(token, channel_id, self.photo, self.caption)
		if res == False:
			return res
		else:
			return True

	def isTime(self):
		#getting current time
		current_time_string = strftime("%Y-%m-%d %H:%M:%S")
		current_time = datetime.strptime(current_time_string, "%Y-%m-%d %H:%M:%S")
		post_time = datetime.strptime(self.post_time_string, "%Y-%m-%d %H:%M:%S")

		return (current_time >= post_time)

	def toDict(self):
		return {"photo": self.photo, "caption": self.caption, "post_time_string": self.post_time_string}