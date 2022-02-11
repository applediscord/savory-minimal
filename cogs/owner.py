import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from asyncio import sleep

# Eval command imports
import sys
import requests
import io
import cogs
from aioconsole import aexec

store = cogs.util.store
checks = cogs.checks

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        out, err = io.StringIO(), io.StringIO()
        silence = False
        if code.startswith('-s'):
            silence = True
            code = code[3:]
            await ctx.message.delete()
        code = code[:-3]
        code = code[5:]
        args = {
            "discord": discord,
            "Button": Button,
            "Select": Select,
            "SelectOption": SelectOption,
            "ctx": ctx,
            "self": self,
            "cogs": cogs,
            "sleep": sleep,
            "requests": requests,
            "client": self.bot,
            "datetime": datetime
        }
        sys.stdout = out
        sys.stderr = err
        await aexec(code, args) # main exec process
        results = out.getvalue()
        errors = err.getvalue()
        if not silence:
            await ctx.send(f"```py\n{results}```{('```Errors: ' + errors + '```') if errors != '' else ''}")

    @commands.command()
    @commands.is_owner()
    async def d(self, ctx, meID):
        await ctx.message.delete()
        e = await ctx.channel.fetch_message(int(meID))
        await e.delete()

    @commands.command()
    @commands.is_owner()
    async def kickuser(self, ctx, member: discord.Member, reason):
        await ctx.message.delete()
        await member.kick(reason=reason)

    @commands.command()
    @commands.check(checks.owner_staff)
    async def purge(self, ctx, message):
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(message))

def setup(bot):
    bot.add_cog(Owner(bot))
