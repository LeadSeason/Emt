from discord.ext import commands
import discord
import sys

# cog Template


class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.is_owner()
    async def dev(self, ctx):
        await ctx.send("Dev tools wip")

    @dev.command(aliases=["clear", "cls"])
    async def console_clear(self, ctx):
        print("\n"*500)

    @dev.command(aliases=["kill", "stop"])
    async def shutdown(self, ctx):
        sys.exit()


def setup(bot):
    bot.add_cog(dev(bot))
