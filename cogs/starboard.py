import discord
from discord.ext import commands

class starboard(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.listMsg = []
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.count == 1 and str(reaction.emoji) == '👍' and not reaction.message.id in self.listMsg: #кад направиш емоџи, додај ид
            embed = discord.Embed(title=reaction.message.content)
            embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
            await self.client.get_channel(776178558317625354).send(embed=embed)
            self.listMsg.append(reaction.message.id)



def setup(client):
    client.add_cog(starboard(client))