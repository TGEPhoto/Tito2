import discord
from discord.ext import commands, tasks
import random
from os import listdir
import asyncio
from mutagen.mp3 import MP3

class music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.l = listdir('./exyuPjesme')
        self.l1 = []
        self.azra_l = []
        self.azraPjesme = []
        for i in self.l:
            if i.startswith('Azra'):
                self.azraPjesme.append(i)
        self.azraPjesme.sort() 

    @commands.Cog.listener()
    async def on_ready(self):
        self.playLoop.start()

    @tasks.loop()
    async def playLoop(self):
        if self.client.get_guild(776167646424727574).voice_client == None:
            await self.client.get_channel(776167646424727579).connect()
            pjesma = random.choice(self.l)
        if not pjesma in self.l1: 
            self.l1.append(pjesma)
            self.l1.sort()
            await self.client.change_presence(activity=discord.Game(pjesma[:-4]))
            self.client.get_guild(776167646424727574).voice_client.play(discord.FFmpegPCMAudio('./exyuPjesme/' + pjesma))
            await asyncio.sleep(MP3('./exyuPjesme/' + pjesma).info.length + 3)
        if self.l1 == self.l:
            self.l1.clear()
    
    @commands.command(aliases=['пјесме', 'pjesma', 'песма', 'pesma'])
    async def pjesme(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.voice_client == None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        self.playLoop.start()


    @commands.command(aliases=['napusti', 'izadji', 'izađi', 'напусти', 'изађи'])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        self.playLoop.stop()

    @commands.command(aliases=['прескочи', 'preskoci', 'preskoči'])
    async def skip(self):
        self.playLoop.stop()
        self.playLoop.start()

    @commands.command(aliases=['азра'])
    async def azra(self, ctx):
        if ctx.author.voice.channel != None:
            channel = ctx.author.voice.channel
            if ctx.voice_client == None:
                await channel.connect()
            else:
                self.client.get_guild(776167646424727574).voice_client.stop()
                self.playLoop.cancel()
                await ctx.voice_client.move_to(channel)
            if not self.playAzra.is_running():
                self.playAzra.start()

    @tasks.loop()
    async def playAzra(self):
        pjesma = random.choice(self.azraPjesme)
        if not pjesma in self.azra_l:
            self.azra_l.append(pjesma)
            self.azra_l.sort()
            await self.client.change_presence(activity=discord.Game((pjesma)[:-4]))
            self.client.get_guild(776167646424727574).voice_client.play(discord.FFmpegPCMAudio('./exyuPjesme/' + pjesma))
            await asyncio.sleep(MP3('./exyuPjesme/' + pjesma).info.length + 3)
        if self.azra_l == self.azraPjesme:
            self.azra_l.clear()

    @commands.command(aliases=['заустави'])
    async def zaustavi(self, ctx, *arg):
        if (arg[0].lower().strip() == 'azra' or arg[0].lower().strip() == 'азра') and self.playAzra.is_running():
            self.client.get_guild(776167646424727574).voice_client.stop()
            self.playAzra.cancel()
        if not self.playLoop.is_running():
            self.playLoop.start()



def setup(client):
    client.add_cog(music(client))