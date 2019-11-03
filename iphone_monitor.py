#	iPhone Manager bot by Oldmole
#	No support will be provided, this code is provided "as is" without warranty of any kind, either express or implied. Use at your own risk.
#	The use of the software and scripts is done at your own discretion and risk and with agreement that you will be solely responsible for any damage
#   to your computer system or loss of data that results from such activities.
#

#	If you like the bot and would like buy me a pint, DM @oldmole#3895 and ask for my Paypal info
#	If you update the bot, please send me a copy! :-)

import sys
import yaml
import sqlite3
import hashlib
import discord
import psutil
from discord.ext import commands
import subprocess
import asyncio
from subprocess import Popen, PIPE
from sqlite3 import OperationalError


class IPhone:
	def __init__(self, device_uuid, iphone_name, iphone_id):
		self.device_uuid = device_uuid
		self.iphone_name = iphone_name
		self.iphone_id = iphone_id
#   A list of the commands
command_list = [
	"!sc {name of iphone} or !sc {iphone ID}",
	 "Screenshots an iphone and uploads that screenshot to discord\n",
	 "!list iphones", "Lists the name and ID of all the available iphones\n",
	 "!kill usb","Finds the proccess ID for usbmuxd and kill's it\n",
	 "!mac grab",
	 "Takes a screengrab of your Mac and uploads that screengrab to discord\n",
	 "!reboot {name of iphone} or !reboot {iphone ID}",
	 "Reboot's an iPhone\n",
	 "!reload {name of iphone} or !reload {iphone ID}",
	 "Find's and kill's the PID for an iPhone's Xcode. Pogo will start again\n",
	 "!help",
	 "Displays this list"
 ]

print("The iPhone Manager by Oldmole ready!")


try:
	with open(r'config.yaml') as file:
		documents = yaml.safe_load(file)
except FileNotFoundError:
	print ("**** FULL STOP! ***** db_path.yaml NOT FOUND! ****")
	sys.exit()

token = documents.get("token")
role = documents.get("role")
channel = documents.get("channel")
iphone_list = []
database_list = documents.get("paths")
db_count = len(database_list)
db_error = 0

for dpath in database_list:
	try:
		connection = sqlite3.connect(dpath)
		cursor = connection.cursor()
		cursor.execute('SELECT * FROM device LIMIT 1,100')
		rows = cursor.fetchall()
		for row in rows:
			uuid, name = row[0], row[1]
			digest = hashlib.sha1((uuid + name).encode()).hexdigest()
			iphone_list.append(IPhone(uuid, name, digest[:4]))
			connection.commit()
	except sqlite3.OperationalError:
		db_error += 1
		print ("*** Error reading from %s database" % dpath)
		print ("*** Wrong database name or path? ***")
		print ("\n")
	finally:
		connection.close()
		if db_error == db_count:
			print ("**** FULL STOP! ***** Can't read from any database ****")
			sys.exit()


async def reboot_command(params, message):
	params = ''.join(params)
	for x in iphone_list:
		if params == x.iphone_name or params == x.iphone_id:
			a = x.iphone_name
			b = x.device_uuid
			cp = subprocess.run(["idevicediagnostics", "-u", b, "restart"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			if cp.returncode == 0:
				await message.channel.send("%s is rebooting" % a)

			else:
				await message.channel.send("Sorry, something has gone wrong... is the device connected?")

async def reload_command(params, message):
	params = ''.join(params)
	await message.channel.send("Can I get a reload")
	for x in iphone_list:
		if params == x.iphone_name or params == x.iphone_id:
			a = x.iphone_name
			b_device_uuid = x.device_uuid
			for proc in psutil.process_iter(): 

				try:
					pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
				except psutil.NoSuchProcess:
					pass
				else:
					if pinfo["name"] == "xcodebuild":
						cmdline = " ".join(pinfo["cmdline"])
						if (b_device_uuid) in cmdline:
							p = psutil.Process(pinfo["pid"])
							p.kill()
							await message.channel.send("Yes, Done")
							return

	await message.channel.send("Something has gone wrong")

async def kill_command(params, message):
	params = ''.join(params)
	if params == "usb":
		name = ""
		await message.channel.send("Trying to finding and Kill usbmuxd. If I find it I will let you know")
		for proc in psutil.process_iter(): 

			try:
				pinfo = proc.as_dict(attrs=['pid', 'name'])
			except psutil.NoSuchProcess:
				pass
			else:
				if pinfo["name"] == "usbmuxd":
					p = psutil.Process(pinfo["pid"])
					p.kill()
					await message.channel.send("Found and Killed it")
					return

	else:
		await message.channel.send("Sorry, something has gone wrong")
		return				

async def help_command(params,message):
	params = ''.join(params)
	if len(params) ==0:
		await message.channel.send("You have these commands available: \n")
		await message.channel.send("\n".join(command_list))

async def mac_command(params, message):
	params = ''.join(params)
	if params == "grab":
		cp = subprocess.run(["screencapture", "mac.jpg"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		if cp.returncode == 0:
			await message.channel.send("Taken a Mac Screengrab")
			await asyncio.sleep(1)
			await message.channel.send(file=discord.File('mac.jpg'))

async def list_iphones_command(params,message):
	params = ''.join(params)
	if params != "iphones":
		return
	else:
		await message.channel.send("You have these iphones in your list:")
		name_list = []
		for x in iphone_list:
			name_and_id = " with an ID of ".join([x.iphone_name,x.iphone_id])
			name_list.append(name_and_id)
		await message.channel.send("\n".join(name_list))

		
async def screengrab_command(params, message):
	params = ''.join(params)
	for x in iphone_list:
		if params == x.iphone_name or params == x.iphone_id:
			a = x.iphone_name
			b = x.device_uuid

			cp = subprocess.run(["idevicescreenshot", "-u", b, "phone.jpg"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			if cp.returncode == 0:
				await message.channel.send("Taken a screenshot")
				await asyncio.sleep(1)
				await message.channel.send(file=discord.File('phone.jpg'))
				return

			else:
				await message.channel.send("Sorry, something has gone wrong... is the device connected?")
				return
		
	await message.channel.send("Sorry, something has gone wrong... can't find this device")


command_dict = {

"!sc": screengrab_command,
"!help": help_command,
"!reboot": reboot_command,
"!reload": reload_command,
"!mac": mac_command,
"!list" : list_iphones_command,
"!kill" : kill_command
}

async def check_command(message_text,message):
	parts = message_text.split(" ",1)
	cmd = parts[0]
	params = parts[1:]

	if cmd in command_dict:
		await command_dict[cmd](params,message)
	else:
		return


	
client = discord.Client()
@client.event
async def on_ready():
	
	activity = discord.Game(name="Taking Selfies")
	await client.change_presence(status=discord.Status.online, activity=activity)	

async def send_message(message):
	await message.channel.send(message)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if str(message.channel) != channel:
		return
	author_roles = map(lambda x: x.name, message.author.roles)
	if role not in author_roles:
		return

	message_text = message.content
	await check_command(message_text,message)

						
client.run(token)
