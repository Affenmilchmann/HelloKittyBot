from myWebFuncs import sendMessage

#this func is a bit useless but it makes code understandable
def sendMessageToOwner(token, owner_id, text):
	sendMessage(token, owner_id, text)