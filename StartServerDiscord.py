import discord
import requests
import socket
import time
import datetime

url = 'http://192.168.178.42:3000/on'
test = 'http://192.168.178.42:3000/test'
path = "/home/pi/started.txt"
r = ''

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in!")
    async def on_message(self, message):
        if (message.author == client.user):
            return
        elif (message.content.startswith("!server start")):
            await message.channel.send("> Prüfung...")
            print("[" + str(datetime.datetime.now()) + f"] Prüfung --> {message.author}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('192.168.178.42', 25565))
            sock.settimeout(None)
            if result == 0:
                await message.channel.send("> Server läuft schon!")
                print("[" + str(datetime.datetime.now()) + f"] Server läuft schon! --> {message.author}")
                time.sleep(20)
                await message.channel.purge(limit = 3)
                print("[" + str(datetime.datetime.now()) + f"] Nachrichten gelöscht! --> {message.author}")

            else:
                try:
                    r = requests.post(test, data = {}, timeout= 5)
                    if r.status_code == 200:
                        await message.channel.send("> Server startet!")
                        print("[" + str(datetime.datetime.now()) + f"] Server gestartet von --> {message.author}")
                        with open(path, "w") as write:
                            write.write(str(message.author))
                        r = requests.post(url, data = {}, timeout=5)
                        time.sleep(20)
                        await message.channel.purge(limit = 3)
                        print("[" + str(datetime.datetime.now()) + f"] Nachrichten gelöscht! --> {message.author}")
                except Exception as e:
                    await message.channel.send("> Finns's PC ist aus oder es gab einen anderen Fehler!")
                    print(f"[" + str(datetime.datetime.now()) + f"] Anfrage von --> {message.author} FEHLER({str(e)})")
                    time.sleep(20)
                    await message.channel.purge(limit = 3)
                    print("[" + str(datetime.datetime.now()) + f"] Nachrichten gelöscht! --> {message.author}")
            print("")
                    
client = MyClient()
client.run("Nzg2MzA5ODg5NjIxNDkxNzUy.X9EiJg.PUuNWUYBf2W8iPWn0SqMfNYI3k0")