import socket
import discord
import time
import datetime
import threading

token = "Nzg2MzA5ODg5NjIxNDkxNzUy.X9EiJg.PUuNWUYBf2W8iPWn0SqMfNYI3k0"
textkanalid = 851900460867911690
messageid = 860582224423419995
ipadresse = 'mc.finnkrause.com'
checkaddr = '192.168.178.42'
neu = ''
port = 25565
port_testserver = 3000
path = "/home/pi/started.txt"
startedby = "" 
laststate = ""

Durchlauf = 0

class MyClient(discord.Client):
    async def on_ready(self):
        global laststate
        global neu
        global Durchlauf
        print("Bot is online")
        channel = client.get_channel(textkanalid)
        message = await channel.fetch_message(messageid)
        await client.change_presence(activity = discord.Game("Made by Hendrik und Finn"))
        try:
            while True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((checkaddr, port))
                sock.settimeout(None)
                with open(path, "r") as read:
                    startedby = read.readline()
                if result == 0:
                    if laststate != "online" :
                        await message.edit(content = f"> \n> Minecraft Server ist **online!**\n> IP: {ipadresse}   {neu}\n> gestartet: {startedby}\n> ⠀") #Startedby
                        print("[ " + str(datetime.datetime.now()) + " ] Server online [--> Updated]")
                    else:
                        print("[ " + str(datetime.datetime.now()) + " ] Server online")
                    laststate = "online" #online ist der state, der nur eine einzige Ausfhrung hat!
                else:
                    socketsheesh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socketsheesh.settimeout(5)
                    myres = socketsheesh.connect_ex((checkaddr, port_testserver))
                    socketsheesh.settimeout(None)
                    if myres == 0:
                        if laststate == "online" or laststate == "offline pcoff" or Durchlauf == 0:
                            await message.edit(content = f"> \n> Minecraft Server ist **offline!**\n> bereit: **!server start** \n> ⠀")
                            print("[ " + str(datetime.datetime.now()) + " ] Server offline [--> Updated]")
                            with open(path, "w") as write:
                                write.write("Manuell")
                        else:
                            print("[ " + str(datetime.datetime.now()) + " ] Server offline")
                        laststate = "offline pcon"
                    else:
                        if laststate == "online" or laststate == "offline pcon" or Durchlauf == 0:
                            await message.edit(content = f"> \n> Minecraft Server ist **offline!**\n> ⠀")
                            print("[ " + str(datetime.datetime.now()) + " ] Server offline [--> Updated]")
                            with open(path, "w") as write:
                                write.write("Manuell")
                        else:
                            print("[ " + str(datetime.datetime.now()) + " ] Server offline")
                        laststate = "offline pcoff"

                time.sleep(15)
                Durchlauf += 1

        finally:
            await message.edit(content = "> \n> Discord-Bot ist **offline!**\n> ⠀")    

client = MyClient()
client.run(token)