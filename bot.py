import discord
from discord.ext import commands, tasks
import random
from os import listdir
import os.path
import asyncio
from keys import bot as BOT_TOKEN
from mutagen.mp3 import MP3
import datetime

client = commands.Bot(command_prefix='-', case_insensitive=True)

global l
l = listdir('/home/miloje/drugTito/exyuPjesme')
l.sort()
global l1
l1 = []
global azra_l
azra_l = []

global azraPjesme
azraPjesme = []
for i in l:
	if i.startswith('Azra'):
		azraPjesme.append(i)
azraPjesme.sort()

@client.event
async def on_ready():
	playLoop.start()
#	countDown.start()
	print('Тито спреман да буде педер')

@client.command(aliases=['придружи', 'pridruzi', 'pridurži'])
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client == None:
    	await channel.connect()
    else:
    	await ctx.voice_client.move_to(channel)

@tasks.loop()
async def playLoop():
	if client.get_guild(725991701469986876).voice_client == None:
		await client.get_channel(794155646882545704).connect() #направи канал и нађи му id
	pjesma = random.choice(l)
	if not pjesma in l1:
		l1.append(pjesma)
		l1.sort()
		await client.change_presence(activity=discord.Game(pjesma[:-4]))
		client.get_guild(725991701469986876).voice_client.play(discord.FFmpegPCMAudio('/home/miloje/drugTito/exyuPjesme/' + pjesma))
		await asyncio.sleep(MP3('/home/miloje/drugTito/exyuPjesme/' + pjesma).info.length + 3)
	if l1 == l:
		l1.clear()


@client.command(aliases=['пјесме', 'pjesma', 'песма', 'pesma'])
async def pjesme(ctx):
	channel = ctx.author.voice.channel
	if ctx.voice_client == None:
		await channel.connect()
	else:
		await ctx.voice_client.move_to(channel)
	playLoop.start()


@client.command(aliases=['napusti', 'izadji', 'izađi', 'напусти', 'изађи'])
async def leave(ctx):
	await ctx.voice_client.disconnect()
	playLoop.stop()

@client.command(aliases=['прескочи', 'preskoci', 'preskoči'])
async def skip(ctx):
	playLoop.stop()
	playLoop.start()

@client.command(aliases=['азра'])
async def azra(ctx):
	if ctx.author.voice.channel != None:
		channel = ctx.author.voice.channel
		if ctx.voice_client == None:
			await channel.connect()
		else:
			client.get_guild(725991701469986876).voice_client.stop()
			playLoop.cancel()
			await ctx.voice_client.move_to(channel)
		if not playAzra.is_running():
			playAzra.start()

@tasks.loop()
async def playAzra():
	pjesma = random.choice(azraPjesme)
	if not pjesma in azra_l:
		azra_l.append(pjesma)
		azra_l.sort()
		await client.change_presence(activity=discord.Game((pjesma)[:-4]))
		client.get_guild(725991701469986876).voice_client.play(discord.FFmpegPCMAudio('/home/miloje/drugTito/exyuPjesme/' + pjesma))
		await asyncio.sleep(MP3('/home/miloje/drugTito/exyuPjesme/' + pjesma).info.length + 3)
	if azra_l == azraPjesme:
		azra_l.clear()

@client.command(aliases=['заустави'])
async def zaustavi(ctx, *arg):
	if (arg[0].lower().strip() == 'azra' or arg[0].lower().strip() == 'азра') and playAzra.is_running():
		client.get_guild(725991701469986876).voice_client.stop()
		playAzra.cancel()
	if not playLoop.is_running():
		playLoop.start()
		
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

client.run(BOT_TOKEN)