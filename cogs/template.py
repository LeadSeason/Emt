from discord.ext import commands
import discord

# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Nytkö?")


def setup(bot):
    bot.add_cog(template(bot))
