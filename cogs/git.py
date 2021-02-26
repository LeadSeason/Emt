from discord.ext import commands
import discord
import subprocess
import re
# cog git


class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="git")
    @commands.is_owner()
    async def _git(self, ctx):
        ctx.typing()
        p = subprocess.Popen(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        p.wait()
        out, err = p.communicate()

        jotain = re.findall(r"cogs/.+?.py", str(out))
        jotain2 = re.findall(r"\|.+?\\n", str(out))
        print(str(out))
        print(jotain)
        print(jotain2)
        if jotain == []:
            embed = discord.Embed(title="Already up to date")
            pass
        else:
            idk = 0
            for x, k in zip(jotain, jotain2):
                embed = discord.Embed(
                    title="Updated:",
                )
                h = x.replace(".py", "").replace("/", ".")
                _l = k.replace("| ", "").replace("\\n", "")
                print(h)
                print(_l)
                try:
                    self.bot.reload_extension(h)
                except commands.ExtensionFailed as e:
                    embed.add_field(
                        name=f'Cog "{h}" Failed to load',
                        value=str(e),
                        inline=False
                    )
                except commands.ExtensionAlreadyLoaded:
                    embed.add_field(
                        name=f'Cog "{h}" Was updated but not loaded',
                        value=str(_l),
                        inline=False
                    )
                except Exception as e:
                    embed.add_field(
                        name="okei jotain muuta kusi",
                        value=str(e),
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f'Cog "{h}" updated',
                        value=_l,
                        inline=False
                    )
                idk += 1

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(git(bot))


"""
b'Updating cc84127..f5c0eae\n
Fast-forward\n
cogs/dev.py | 22 ++++++++++++----------\n
1 file changed, 12 insertions(+), 10 deletions(-)\n'
"""
# re.findall(r"|.+?\n", str(out))
