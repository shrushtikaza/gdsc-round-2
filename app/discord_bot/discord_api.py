from dotenv import load_dotenv 
import discord 
import os 
from app.chatgpt_ai.openai import chatgpt_response 
import random 

load_dotenv() #loads variables from env file 

discord_token = os.getenv('DISCORD_TOKEN') 

class MyClient(discord.Client) :
    async def on_ready(self) :
        print("Successfully logged in as: ", self.user) #its the bot that logged in

    async def on_message(self, message) :
        print(message.content) #prints content of msg to console 
        if message.author == self.user : #checking if the msg was sent by bot to avoid bot from replying to itself
            return 
        command, user_message = None, None 

        if message.content.startswith ('!ai') or message.content.startswith('!smorkbot'):
            bot_response = chatgpt_response(user_message) #calls a function of AI
            await message.channel.send(f"Answer: {bot_response}")

intents = discord.Intents.default() 
intents.message_content = True 

client = MyClient(intents=intents)