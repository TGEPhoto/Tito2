import discord
from discord.ext import commands

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        """
        Briše poruke. u suštini bukvalno reši no međutim može da se gasira
        """
        await ctx.channel.purge(limit=amount)

    