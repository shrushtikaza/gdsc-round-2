from dotenv import load_dotenv 
import discord 
from discord.ext import commands 
import os 
from app.chatgpt_ai.openai import chatgpt_response 

from app.discord_bot.helpdesk import help_function #help message at beginning
from app.discord_bot.music import music_function #music functionality

intents = discord.Intents.default() 
intents.message_content = True 

bot = commands.Bot(command_prefix="-",intents=intents) #ensures the bot is called with prefix of '-' 
bot.remove_command("help") #removes inbuilt help function 

#register the class with the bot
bot.add_cog(help_function(bot))
bot.add_cog(music_function(bot))

load_dotenv() #loads variables from env file 

discord_token = os.getenv('DISCORD_TOKEN') #storing discord token

class MyClient(discord.Client) :
    async def on_ready(self) :
        print("Successfully logged in as: ", self.user) #its the bot that logged in

    async def on_message(self, message) :
        print(message.content) #prints content of msg to console 
        if message.author == self.user : #checking if the msg was sent by bot to avoid bot from replying to itself
            return 

        if message.content.startswith ('!ai') or message.content.startswith('!bot'):
            bot_response = chatgpt_response(message.content) #calls a function of AI
            await message.channel.send(f"Answer: {bot_response}")

client = MyClient(intents=intents)
