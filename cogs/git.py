from discord.ext import commands
import discord
import subprocess

# cog git

#idk jotain tää on testi


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    async def _git(self, ctx):

        try:
            print("########")
            p = subprocess.Popen(
                ["git", "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p.wait()
            out, err = p.communicate()
            await ctx.send(out)
        except Exception as e:
            await ctx.send(e)
        else:
            await ctx.send("Success")


def setup(bot):
    bot.add_cog(git(bot))
