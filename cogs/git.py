from discord.ext import commands
import discord
import subprocess
import re
# cog git


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    async def _git(self, ctx):

        # try:
        async with ctx.typing():
            p = subprocess.Popen(
                ["git", "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p.wait()
            out, err = p.communicate()
        print(out)
        embed = discord.Embed(title="Output", description=str(out))
        jotain = re.findall(r"cogs/.+?.py", str(out))
        embed.add_field(
            name="test stuff",
            value=str(jotain),
            inline=False
        )
        await ctx.send(embed=embed)
        # except Exception as e:
        #    await ctx.send(e)


def setup(bot):
    bot.add_cog(git(bot))
