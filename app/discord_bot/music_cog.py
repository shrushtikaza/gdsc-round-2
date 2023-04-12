import discord 
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog) :
    def __init__(self,bot) :
        self.bot = bot 

        #specify state of both with:

        self.is_playing = False 
        self.is_paused = False 

        self.music_queue = [] #queue of songs 

        #make sure use best quality and there are no playlists on YT
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    #searching the song on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] #doesnt download
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']} #returns url 

    #play next:
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True #sets status as Playing

            #get url of next song
            m_url = self.music_queue[0][0]['source']

            #remove the first song as its currently playing 
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) #after it is done playing it calls itself - recursive function 
        else:
            self.is_playing = False #if no more music next 

    #function that is called when -play is typed in chat:
    async def play_music(self, ctx): 
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #checks if it is in a Voice Channel 
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case it fails to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1]) #moves the bot to the channel where the user is 
            
            #remove the first song as its currently playing 
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases="p", help="plays a selected song from youtube") #defining the function
    
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:

            #needs to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword.")
            else:
                await ctx.send("Song added to queue!")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

        