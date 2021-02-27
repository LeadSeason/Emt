from discord.ext import commands
import discord

# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(template(bot))
