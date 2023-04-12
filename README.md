CODING A DISCORD BOT WITH PYTHON 

Functionality :
- Responding to user messages in Discord using openAI GPT-3 AI. 
- Music functionality from Youtube. 

Steps : 

Function 1 : 

1. Create Discord Application and a bot within it. 
2. Add bot to a guild (server).
3. Connect written code to Discord. 
4. Create .env file with unique token of the bot and the api key. 
5. Two main set of codes are used - one for discord bot functions and another for AI response. [discord_api.py and openai.py within app folder]
6. run.py - use to run the code. 

Function 2 : 

1. Set command prefix as '-' to ensure that music functionality occurs only with '-' followed by a command.
2. Call music functionality, help to main discord bot functions code. [discord_api.py] 
3. Functions like play, pause, skip are defined in music functionality code. [music_cog.py]

Libraries used: 
- discord : discord library with built-in functions.
- openai : openai library. 
- dotenv : helps working with .env files. 
- ffmpeg : handle multimedia files.
- PyNaCl : improves usability, security and speed.
- youtube_dl : to search youtube for songs. 
