from dotenv import load_dotenv 
import discord 
from discord.ext import commands 
import os 
from app.chatgpt_ai.openai import chatgpt_response 

from help import help_function #help message at beginning
from music import music_function #music functionality

bot = commands.Bot(command_prefix="-") #ensures the bot is called with prefix of '-' 
bot.remove_command("help")

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

intents = discord.Intents.default() 
intents.message_content = True 

client = MyClient(intents=intents)
