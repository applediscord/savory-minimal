import cogs
import json
import re
import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.applications import store
from datetime import datetime
from asyncio import sleep

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        try:
                label = interaction.component.label
                ide = interaction.component.id
        except:
            print("error setting id")
            ide = None
        if label == "Verify" or ide == "verify":
            if interaction.user.id == 512063606750183429:
                await interaction.respond(content="Sorry, you do not have permission to verify!", ephemeral=True)
                return
            role = interaction.message.guild.get_role(788914323485491232)
            mrole = interaction.message.guild.get_role(788890991028469792)
            member = await interaction.message.guild.fetch_member(interaction.user.id)
            await member.add_roles(role)
            await member.remove_roles(mrole)
            await interaction.respond(type=6)
        elif label == "Accept App":
            ide = ide.replace('-a', '')
            m = await interaction.message.guild.fetch_member(interaction.user.id)
            for role in m.roles:
                if role.id in [792875711676940321, 792875711676940321, 788911513129058304]: break
                if m.id == 406629388059410434: break
            else:
                await interaction.respond(content="You do not have permission to use this!")
                return
            await interaction.respond(type=6)
            ctx = interaction.message.guild.get_channel(831579949415530527)
            f = await ctx.send("Fetching data from api...")
            e = store('apps.json', 'guildApps', True, app=True)
            if ide not in e:
                await f.edit(content="Could not find that application!")
                return
            r = ctx.guild.get_role(789590790669205536)
            b = ctx.guild.get_role(831614870256353330)
            try:
                m = await ctx.guild.fetch_member(int(ide))
                await m.add_roles(r)
                await m.remove_roles(b)
            except:
                await ctx.send("Member lookup failed, deleting application; ask applicant to apply again.")
                await interaction.message.delete()
                store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
                return
            await f.edit(content="Sending data to API...")
            store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
            store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=ide)
            e = await ctx.guild.fetch_member(ide)
            try:
                await e.send(f"Your application for `Red Gladiators` has been accepted by `{interaction.user}`! Head over to the server to check it out!")
            except:
                await f.edit(content='Application accepted but user has private messages turned off')
                await interaction.message.edit(components=[])
                return
            await f.edit(content="Application accepted")
            await interaction.message.edit(components=[])
        elif label == "Deny App":
            ide = ide.replace('-d', '')
            m = await interaction.message.guild.fetch_member(interaction.user.id)
            for role in m.roles:
                if role.id in [792875711676940321, 792875711676940321, 788911513129058304]: break
                if m.id == 406629388059410434: break
            else:
                await interaction.respond(content="You do not have permission to use this!")
                return
            ctx = interaction.message.guild.get_channel(831579949415530527)
            await interaction.respond(type=6)
            f = await ctx.send("Fetching data from api...")
            e = store('apps.json', 'guildApps', True, app=True)
            if ide not in e:
                await f.edit(content='Could not find that application!')
                return
            b = ctx.guild.get_role(831614870256353330)
            try:
                m = await ctx.guild.fetch_member(int(ide))
                await m.remove_roles(b)
            except:
                await f.edit("Member lookup failed, deleting application; ask applicant to apply again.")
                await interaction.message.delete()
                store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
                return
            await f.edit(content='Sending data to API...')
            store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
            store('apps.json', 'deniedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=ide)
            e = await ctx.guild.fetch_member(ide)
            try:
                await e.send(f"Your application to `Red Gladiators` has been denied by `{interaction.user}`. You cannot apply again. Talk to a staff member if you have any issues.")
            except:
                await f.edit(content="Application denied successfully but user has private messages turned off")
                await interaction.message.edit(components=[])
                return
            await f.edit(content="Application denied")
            await interaction.message.edit(components=[])
        elif label == "Remove" or ide == "remove":
            await interaction.message.delete()
        try:
            userid = ide.split('-')[0]
        except:
            userid = ide
        if str(interaction.user.id) != userid: return
        if label == 'Exit' or ide == "exit":
            await interaction.message.edit(components=[])
        elif label == 'Delete' or ide == "delete" or interaction.user.id == 406629388059410434:
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        if message.author.bot and message.author.id not in [716045085472718859, 159985870458322944, 710143953533403226]: return
        if message.author.id != 713461668667195553:
            if message.author.id == 406629388059410434:
                if message.content.startswith('embed'):
                    args = message.content[6:].split(' ')
                    await message.delete()
                    if args[0] == 'v':
                        e = discord.Embed(title="Verification", color=discord.Color.blurple(), timestamp=datetime.utcnow())
                        if not '-tn' in args: e.set_thumbnail(url=ctx.guild.icon_url)
                        e.add_field(name="Verify", value="To verify, click the button below. **You will be kicked without warning if you have not verified within _3_ days!**", inline=False)
                        e.add_field(name="Read the rules", value="Make sure to read our <#788887107544285244>!", inline=False)
                        e.add_field(name="Get roles", value="Go to <#817763660340133928> and react to the message with your role", inline=False)
                        if not '-j' in args: e.add_field(name="Subscribe to Jacob Contests", value="Pick up your roles from <#868650553285181462> to be notified about new jacob events in <#893293159512154183>.", inline=False)
                        e.add_field(name="Join the guild!",value="To join the Guild, you first must verify, then check out the <#822915132153135144> channel.", inline=False)
                        e.add_field(name='Need support?', value="If you ever need support, you can create a ticket in <#866426260573650966>.", inline=False)
                        e.set_footer(text="Thank you for joining! Last updated")
                        await ctx.send(embed=e, components=[Button(label='Verify', style=1)])
                    elif args[0] == 'a':
                        e = discord.Embed(title="Guild Applications", color=discord.Color.blurple(), timestamp=datetime.utcnow())
                        e.add_field(name="How to apply", value="Type `/apply` in _any_ chat, then type your minecraft IGN (incasesensitive).", inline=False)
                        e.add_field(name="API", value="If you do not have your APIs (skills, collections, enderchest, **and** inventory) on, your application will be instantly rejected.", inline=False)
                        e.add_field(name="Response", value="Your application will be handled by staff members. They have the choice to accept/reject you based on your skill average, networth, slayers, and more. If you get rejected, you cannot apply again. If you feel this is a mistake, you can always DM a staff member.", inline=False)
                        e.set_footer(text="Last updated")
                        await ctx.send(embed=e)
        if message.channel.id == 788889735157907487:
            if message.author.id == 392502213341216769 or message.author.id == 159985870458322944:
                splitted = message.content.split(' ')
                if int(splitted[7][:-1])%10 != 0:
                    return
                userid = re.sub("[^0-9]", "", splitted[1])
                user = await message.guild.fetch_member(int(userid))
                roleid = {"40!": 865832933028528158, "30!": 865832837948244009, "20!": 864125893660508161, "10!": 841066567151910932}
                role = message.guild.get_role(roleid[splitted[7]])
                await user.add_roles(role)
        elif message.channel.id == 788886124159828012:
            if message.author.id in [716045085472718859, 710143953533403226]:
                await message.reply('Please refrain from using bot commands in general.')
                await sleep(8)
                await message.delete()
        try:
            bl = store('blacklist.json', message.author.id, True)
            for command in bl['blacklistedCommands']:
                if command == ctx.command:
                    return
        except: pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            e = discord.Embed(title="You do not have permission to do this!", color=discord.Color.red())
            await ctx.send(embed=e, delete_after=3)
        elif isinstance(error, commands.CommandNotFound):
            e = discord.Embed(title="Command not found!", color=discord.Color.red())
            await ctx.send(embed=e, delete_after=3)
        else:
            e = discord.Embed(title="An exception occurred", description=f"{error}")
            await cogs.util.bugReport(self.bot, f'`Command Error` {ctx.message.content}', f"{error}")
            await ctx.send(embed=e, delete_after=10)

def setup(bot):
    bot.add_cog(Listeners(bot))
