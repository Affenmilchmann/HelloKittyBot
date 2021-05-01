import requests
import json, os

from log import reqLog, consoleOutput, errLog, msgLog

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
		consoleOutput(response_string)
		errLog("getRequest() " + str(response_string))
	if len(response_string['result']) > 0:
		consoleOutput("Responses:" + str(len(response_string['result'])))
		reqLog(response_string)

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
		errLog("sendDocument() " + str(response_string))
		return response_string
	else:
		msgLog("Document " + str(file_id) + "\nCaption " + str(caption),
		"Bot", 
		chat_id)
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
		errLog("sendPhoto()" + str(response_string))
		return response_string
	else:
		msgLog("Photo " + str(photo_link) + "\nCaption " + str(caption),
		"Bot", 
		chat_id)
		return True

def sendMessage(token, chat_id, text):
	data = {
		'chat_id': chat_id,
		'text': text
	}

	response_string = postRequest(token, chat_id, "sendMessage", data)

	if response_string['ok'] == False:
		errLog("sendMessage()" + str(response_string))
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

def getMessages(token):
	req_result = getUpdates(token, 0)["result"]

	out_dict = {}

	for upd in req_result:
		if "message" in upd:
			message = upd["message"]

			user_id = message["from"]["id"]
			text = message["text"]

			if user_id in out_dict:
				out_dict[user_id].append(text)
			else:
				out_dict[user_id] = [text]

	return out_dict