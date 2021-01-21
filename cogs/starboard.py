import discord
from discord.ext import commands, tasks

class starboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction):
        print('resi')
        if reaction.count == 1 and reaction.emoji.name == 'thumbsup': #кад направиш емоџи, додај ид
            embed = discord.Embed(title=reaction.message.contents)
            embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_id)
            await self.client.get_channel(776178558317625354).send(embed=embed)



def setup(client):
    client.add_cog(starboard(client))