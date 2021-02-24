from discord.ext import commands
import discord
import subprocess
import re
# cog git

# jotain

class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="update")
    async def _git(self, ctx):

        try:
            async with ctx.typing():
                p = subprocess.Popen(
                    ["git", "pull"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                p.wait()
                out, err = p.communicate()
                embed = discord.Embed(title="Output", description=str(out))
                jotain = re.findall(r"cogs/.+?.py", str(out))
                print(jotain)
                embed.add_field(
                    name="test stuff",
                    value=str(jotain),
                    inline=False
                )
                if jotain == []:
                    pass
                    # sanoa että on jo up to date
                else:
                    for x in jotain:
                        try:
                            self.bot.reload_extension(
                                x.replace(".py", "").replace("/", ".")
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f'Cog "{x}" Failed to load',
                                value=str(e),
                                inline=False
                            )
                        else:
                            embed.add_field(
                                name=f'Cog "{x}" reloaded',
                                value=("jotain"),
                                inline=False
                            )

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(git(bot))
