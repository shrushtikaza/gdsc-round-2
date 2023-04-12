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

    #plays music 

    @commands.command(name="play", aliases=["p"], help="plays a selected song from youtube") #defining the function
    
    async def play(self, ctx, *args):
        query = " ".join(args) 
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:

            #needs to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")

        elif self.is_paused: #if paused 
            self.vc.resume()
        else:
            song = self.search_yt(query) #need to search music on yt
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword.")
            else:
                await ctx.send("Song added to queue!")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    #pauses song

    @commands.command(name="pause", help="pauses the current song")
    
    async def pause(self, ctx, *args):
        
        if self.is_playing :
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        
        elif self.is_paused :
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    #resumes playing song

    @commands.command(name = "resume", aliases=["r"], help="resumes")
    
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    #skips song 

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx) #tries to play next in the queue if it exists

    #displays top 5 songs in queue

    @commands.command(name="queue", aliases=["q"], help="displays the first 5 songs in queue")
    
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("no music in queue")

    #clearing queue 

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("music queue cleared")
