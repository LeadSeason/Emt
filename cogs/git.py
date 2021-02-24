from discord.ext import commands
import discord
import git

# cog git


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):

        try:
            g = git.cmd.git("./.git/")
            g.pull()
        except Exception as e:
            await ctx.send(e)
        else:
            await ctx.send("Success")


def setup(bot):
    bot.add_cog(git(bot))
