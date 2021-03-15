from discord.ext import commands
import discord
import json

# cog help


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="Returns all commands available")
    async def help(self, ctx, arg):
        if ctx.invoked_subcommand is None:
            await ctx.send(arg)
            """
            _list = self.bot.commands
            with open("./data/help.json", encoding='utf-8') as s:
                _help = json.load(s)
            """

    @help.command()
    @commands.is_owner()
    async def add(self, ctx):
        await ctx.send("command not done yet")
        pass

    @help.command()
    @commands.is_owner()
    async def subadd(self, ctx):
        await ctx.send("command not done yet")
        pass


def setup(bot):
    bot.add_cog(help(bot))
