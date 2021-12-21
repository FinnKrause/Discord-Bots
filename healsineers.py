import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print("Benecke und Schrammel!")

    async def on_message(self, message):
        if message.author == client.user:
            return
        elif (":BENECKEEEEE:" in message.content):
            await message.channel.send(" <:SCHRAMMEL:844214310837420074>")
            print(str(message.author) + ": " + message.content)
        elif (":SCHRAMMEL:" in message.content):
            await message.channel.send("<:BENECKEEEEE:844214027072962570>")
            print(str(message.author) + ": " + message.content)
        else:
            print(str(message.author) + ": " + message.content)


client = MyClient()
token = ""
with open("./token.txt", "r") as r:
    token = r.readline()
client.run(token)
