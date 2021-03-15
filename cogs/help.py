from discord.ext import commands
import discord

# cog help


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Returns all commands available")
    async def help(self, ctx):
        helptext = "```"
        for command in self.bot.commands:
            helptext += f"{command}\n"
        helptext += "```"
        await ctx.send(helptext)


def setup(bot):
    bot.add_cog(help(bot))
