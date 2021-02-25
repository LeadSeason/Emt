from discord.ext import commands
import discord

# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self, ctx):
        await ctx.send("aaaaaaaaaaaaaaaa")


def setup(bot):
    bot.add_cog(template(bot))
