from discord.ext import commands
import discord
import subprocess

# cog git


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    async def _git(self, ctx):

        try:
            print("########")
            p = subprocess.Popen(["git", "pull"])
            print(p.communicate())
            p.wait()
            
        except Exception as e:
            await ctx.send(e)
        else:
            await ctx.send("Success")


def setup(bot):
    bot.add_cog(git(bot))
#test