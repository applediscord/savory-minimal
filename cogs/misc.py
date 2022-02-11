import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @scmd.cog_slash(name='senither')
    async def senither(self, ctx):
        await ctx.send("https://hypixel-leaderboard.senither.com/", hidden=True)

def setup(bot):
    bot.add_cog(Misc(bot))