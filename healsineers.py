import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print("Benecke und Schrammel!")

    async def on_message(self, message):
        if message.author == client.user:
            return
        elif (":BENECKEEEEE:" in message.content):
            await message.channel.send(" <:SCHRAMMEL:844214310837420074>")
            print(message.content + "      "+  message.author)
        elif (":SCHRAMMEL:" in message.content):
            await message.channel.send("<:BENECKEEEEE:844214027072962570>")
            print(message.content + "      "+  str(message.author))
        else:
            print(message.content + "      "+  str(message.author))
            pass
    
client = MyClient()
client.run("token")