import discord
from discord.ext import commands, tasks
import random
from os import listdir
import os.path
import asyncio
from keys import bot as BOT_TOKEN
from mutagen.mp3 import MP3
import datetime

intents = discord.Intents.default()
intents.reactions = True
client = commands.Bot(command_prefix='-', case_insensitive=True, intents=intents)

@client.event
async def on_ready():
	print('Тито спреман да буде педер и даље')


#for filename in os.listdir('./cogs'):
 #   if filename.endswith('.py'):
 #       client.load_extension(f'cogs.{filename[:-3]}')

client.load_extension('cogs.starboard')

client.run(BOT_TOKEN)