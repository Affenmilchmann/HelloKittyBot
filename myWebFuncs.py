import requests
import json

log_file = "log.txt"

#it returns response string
#its used in POST requests
def postRequest(token, chat_id, method, data):
	#making url
	url = "https://api.telegram.org/bot" + token + "/" + method
	#filling data
	files = []
	headers = {}

	#sending request
	response = requests.request("POST", url, headers = headers, data = data, files = files)
	#getting response text
	response_string = json.loads(response.text.encode('utf8'))


	return response_string

def getRequest(token, method, data = {}):
	url = "https://api.telegram.org/bot" + token + "/" + method

	data = data
	headers = {}
	files = []

	response = requests.request("GET", url, headers = headers, data = data, files = files)

	response_string = json.loads(response.text.encode('utf8'))

	if not response_string['ok']:
		print(response_string)
	if len(response_string['result']) > 0:
		print("Responses:", len(response_string['result']))
		with open(log_file, "a") as f:
		    f.write(str(response_string) + "\n")

	return response_string

def sendDocument(token, chat_id, file_id, caption = "", disable_notifications = False):
	data = {
		'chat_id': chat_id,
		'document': file_id,
		'caption': caption,
		'disable_notification': disable_notifications
	}
	response_string = postRequest(token, chat_id, "sendDocument", data)
	
	if response_string['ok'] == False:
		return response_string
	else:
		return True
	
#it returns response text in case of an error or True if all is ok
def sendPhoto(token, chat_id, photo_link, caption, disable_notifications = False):
	data = {
		'chat_id': chat_id,
		'photo': photo_link,
		'caption': caption,
		'disable_notifications': disable_notifications
	}

	response_string = postRequest(token, chat_id, "sendPhoto", data)

	if response_string['ok'] == False:
		return response_string
	else:
		return True

def sendMessage(token, chat_id, text):
	data = {
		'chat_id': chat_id,
		'text': text
	}

	response_string = postRequest(token, chat_id, "sendMessage", data)

	if response_string['ok'] == False:
		return response_string
	else:
		return True

#it returns updates string or False if there is an error
def getUpdates(token, last_update_id):
	data = {
		"offset": last_update_id
	}

	return getRequest(token, "getUpdates", data)

#if bot is ok...
def getMe(token):
	return getRequest(token, "getMe")