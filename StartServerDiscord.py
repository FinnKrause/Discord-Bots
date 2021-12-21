import discord
import requests
import socket
import time
import datetime

test = 'http://192.168.178.42:3000/test'
path = "./started.txt"
r = ''


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in!")

    def isOnline(self, adresse, port, message):
        print("[" + str(datetime.datetime.now()) +
              f"] Prüfung --> {message.author}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((adresse, port))
        sock.settimeout(None)
        return result

    async def startServer(self, adresse, message, dataPath):
        r = requests.post(adresse, data={}, timeout=5)
        if r.status_code == 200:
            await message.channel.send("> Server startet!")
            print("[" + str(datetime.datetime.now()) +
                  f"] Server gestartet von --> {message.author}")
            with open(dataPath, "w") as write:
                write.write(str(message.author))
            r = requests.post(adresse.replace(
                "test", "on"), data={}, timeout=5)
            time.sleep(20)
            await message.channel.purge(limit=3)
            print("[" + str(datetime.datetime.now()) +
                  f"] Nachrichten gelöscht! --> {message.author}")
            return r

    async def handleStartError(self, message, e):
        await message.channel.send("> Finns's PC ist aus oder es gab einen anderen Fehler!")
        print(f"[" + str(datetime.datetime.now()) +
              f"] Anfrage von --> {message.author} FEHLER({str(e)})")
        time.sleep(20)
        await message.channel.purge(limit=3)
        print("[" + str(datetime.datetime.now()) +
              f"] Nachrichten gelöscht! --> {message.author}")

    async def handleAlreadyOn(self, message):
        await message.channel.send("> Server läuft schon!")
        print("[" + str(datetime.datetime.now()) +
              f"] Server läuft schon! --> {message.author}")
        time.sleep(20)
        await message.channel.purge(limit=3)
        print("[" + str(datetime.datetime.now()) +
              f"] Nachrichten gelöscht! --> {message.author}")

    async def on_message(self, message):
        if (message.author == client.user):
            return
        elif (message.content.startswith("!server start mainserver")):
            await message.channel.send("> Prüfung...")

            result = self.isOnline('192.168.178.42', 25565, message)

            if result == 0:
                await self.handleAlreadyOn(message)

            else:
                try:
                    await self.startServer(
                        "http://192.168.178.42:3000/test", message, "./started.txt")
                except Exception as e:
                    await self.handleStartError(message, e)
            print("")

        elif (message.content.startswith("!server start hiddenserver")):
            await message.channel.send("> Prüfung...")

            result = self.isOnline('192.168.178.42', 25566, message)

            if result == 0:
                await self.handleAlreadyOn(message)

            else:
                try:
                    await self.startServer(
                        "http://192.168.178.42:2999/test", message, "./NewServerStarted.txt")

                except Exception as e:
                    await self.handleStartError(message, e)
            print("")


client = MyClient()
token = ""
with open("./token.txt", "r") as r:
    token = r.readline()

client.run(token)
