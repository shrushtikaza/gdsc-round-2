from app.discord_bot.discord_api import client, discord_token

if __name__ == '__main__' : #checks whether code is being run as a main program or being imported as a module
    client.run(discord_token)  