import os, time
from Bot import Bot
from myWebFuncs import getMe, sendMessage, getMessages
from log import *
from random import choices
from string import digits

##Setting timezone
os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

##Defining init vars
script_dir = os.path.dirname(__file__)

config_file = os.path.join(script_dir, "config.cfg")
json_file = os.path.join(script_dir, "shedule.json")
history_file = os.path.join(script_dir, "posted.txt")
is_set_up = False
token = ""
owner_id = ""
channel_id = ""

##Check if Bot is set up
#if file exists
try:
	with open(config_file, 'r') as f:
		is_set_up = not (len(f.read()) == 0)
except IOError:
	is_set_up = False

##Creating missing files
with open(json_file, "a") as f:
	pass

with open(history_file, "a") as f:
	pass
###################################
#selling up token and ids values
#if bot is set then just load data from config file
if is_set_up:
	with open(config_file) as f:
		token = f.readline().rstrip()
		owner_id = f.readline().rstrip()
		channel_id = f.readline().rstrip()
#else asking user to fill data
else:
	#########
	#Starting chat to set setting up
	print("Looks like you are new here. Lets set your bot up...")
	#Setting Token
	print("Please, input your access token:")
	while True:
		token = input(">> ")
		if getMe(token)['ok']:
			break
		else:
			print("Something wrong with this token... Please try again")

	#Setting owner chat:
	secret = ''.join(choices(digits, k=5))
	print("Great, now pls sent this code to the bot: " + secret)
	input("Hit enter when you are ready.")
	is_ready = False
	while not is_ready:
		msgs = getMessages(token)
		for user in msgs:
			for msg in msgs[user]:
				if msg == secret:
					is_ready = True
					owner_id = user
					break
			if is_ready:
				break
		if is_ready:
			break
		else:
			input("I havent got right message :( try again")

	#setting channel chat
	print("Amazing! Now add a bot to your channel and give gim post premissions.")
	print("And then input your channel id (its usually in the format '@<your_channel_name>'):")
	while True:
		channel_id = input(">> ")
		respond = sendMessage(token, channel_id, "Hello!")
		if respond != True:
			print("Something wrong with this id... Please try again")
			print("[ErrorMessage]", respond)
			continue
		else:
			print("Have you recieved message from the bot (y/n)?")
			if input(">> ") == "y":
				break
			else:
				print("Then input the correct one:")
	#########
	#Saving data
	with open(config_file, "w") as f:
		f.write(token)
		f.write("\n")
		f.write(str(owner_id))
		f.write("\n")
		f.write(channel_id)

	print("Awesome! Your settings were saved!")

#############################################################################
#Run section
#############################################################################

botLog("Started.")

hello_kitty = Bot(token, owner_id, channel_id)

consoleOutput("Bot is running with settings:\n		- admin id: " +  str(owner_id) + "\n" + "		- channel id:" + str(channel_id))
try:
	while True:
		hello_kitty.mainLoop()
except BaseException as e:
	errLog(str(format(e)))
	botLog("Crashed.")
	respond = sendMessage(token, owner_id, "[Crash]\n\n" + str(format(e)))
