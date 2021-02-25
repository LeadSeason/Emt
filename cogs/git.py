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
        # try:
        async with ctx.typing():
            p = subprocess.Popen(
                ["git", "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p.wait()
            out, err = p.communicate()

            jotain = re.findall(r"cogs/.+?.py", str(out))
            if "Already up to date." in out:
                embed = discord.Embed(
                    title="Already up to date.",
                    color=0x00ff00
                    )
            updated = ""
            if jotain == []:
                embed = discord.Embed(
                    title="No cogs where updeted",
                    description="""
                    but something else was updeted
                    bot should be restarted
                    """
                )
                pass
            else:
                for x in jotain:
                    h = x.replace(".py", "").replace("/", ".")
                    try:
                        self.bot.reload_extension(h)
                    except commands.ExtensionFailed as e:
                        embed.add_field(
                            name=f'Cog "{h}" Failed to load',
                            value=str(e),
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name="okei jotain muuta kusi",
                            value=str(e),
                            inline=False
                        )
                    else:
                        updated += "Updeted " + h + "\n"

                embed = discord.Embed(
                    title="Updated:",
                    description=updated
                )

        await ctx.send(embed=embed)
        """    
        except Exception as e:
            await ctx.send(e)
        """

def setup(bot):
    bot.add_cog(git(bot))
