import socket
import discord
import time
import datetime
import threading

textkanalid = 851900460867911690
messageid = 922580759108259960
ipadresse = 'mc.finnkrause.com'
port_testserver = 3000

StartedMainServerPath = "./started.txt"
StartedNewServerPath = "./NewServerStarted.txt"

startedby = ""
lastMessage = ""
currentMessage = ""

Durchlauf = 0


class MyClient(discord.Client):
    def checkServer(self, adress, port) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((adress, port))
        sock.settimeout(None)
        return result

    def getStartedBy(self, fileName) -> str:
        returnvalue = ""
        with open(fileName, "r") as read:
            returnvalue = read.readline()
        return returnvalue

    def getDiscordFormattedText(self, TextArray) -> str:
        value = "> ⠀\n"
        for i in TextArray:
            value += "> "+i + "\n"
        value += "> ⠀\n"
        return value

    def isPCon(self) -> bool:
        socketsheesh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketsheesh.settimeout(5)
        myres = socketsheesh.connect_ex(("192.168.178.42", port_testserver))
        socketsheesh.settimeout(None)
        return myres == 0

    def getOnlineMessage(self, adresse, started, Servername) -> str:
        returnvalue = self.getDiscordFormattedText(
            [Servername+" ist **online!**", "IP: " + adresse, "gestartet: "+started])
        return returnvalue

    def getOfflineMessage(self, isPCon, Servername) -> str:
        returnvalue = ""
        if (isPCon):
            returnvalue = self.getDiscordFormattedText(
                [Servername + " ist **offline**!", "bereit: **!server start " + str(Servername).lower() + "**"])
        else:
            returnvalue = self.getDiscordFormattedText(
                [Servername+" ist **offline**!"])
        return returnvalue

    async def on_ready(self):
        global lastMessage
        global Durchlauf
        global currentMessage

        print("Bot is online")
        channel = client.get_channel(textkanalid)
        message = await channel.fetch_message(messageid)
        await client.change_presence(activity=discord.Game("Made by Hendrik und Finn"))

        try:
            while True:
                resMainServer = self.checkServer("192.168.178.42", 25565)
                resNewServer = self.checkServer("192.168.178.42", 25566)

                startedMainServer = self.getStartedBy(StartedMainServerPath)
                startedNewServer = self.getStartedBy(StartedNewServerPath)

                lastMessage = currentMessage
                currentMessage = ""
                isPCon = self.isPCon()

                if resMainServer == 0 or resNewServer == 0:  # * Wenn der Server läuft
                    if (resMainServer == 0):
                        currentMessage += self.getOnlineMessage(
                            "mc.finnkrause.com", startedMainServer, "Mainserver")
                    else:
                        currentMessage += self.getOfflineMessage(
                            isPCon, "Mainserver")
                        with open(StartedMainServerPath, "w") as write:
                            write.write("Manuell")

                    if (resNewServer == 0):
                        currentMessage += self.getOnlineMessage(
                            "hiddenserver.finnkrause.com", startedNewServer, "HiddenServer")
                    else:
                        currentMessage += self.getOfflineMessage(
                            isPCon, "HiddenServer")
                        with open(StartedNewServerPath, "w") as write:
                            write.write("Manuell")

                    print("[ " + str(datetime.datetime.now()) +
                          " ] Server online [--> Updated]")

                    await message.edit(content=currentMessage)

                else:
                    currentMessage += self.getOfflineMessage(
                        isPCon, "Mainserver")
                    currentMessage += self.getOfflineMessage(
                        isPCon, "HiddenServer")

                    with open(StartedMainServerPath, "w") as write:
                        write.write("Manuell")
                    with open(StartedNewServerPath, "w") as write:
                        write.write("Manuell")

                    await message.edit(content=currentMessage)

                time.sleep(15)
                Durchlauf += 1

        finally:
            await message.edit(content="> \n> Discord-Bot ist **offline!**\n> ⠀")


client = MyClient()
token = ""
with open("./token.txt", "r") as r:
    token = r.readline()
client.run(token)
