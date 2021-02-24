from discord.ext import commands
import discord
import git

# cog git


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    async def _git(self, ctx):

        try:
            repo = git.Repo(self.rorepo.working_tree_dir)
            repo.remotes.origin.pull()
        except Exception as e:
            await ctx.send(e)
        else:
            await ctx.send("Success")


def setup(bot):
    bot.add_cog(git(bot))
