from discord.ext import commands
import discord
import os
import subprocess
import re

# cog Template


class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.is_owner()
    async def dev(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Dev Tools",
                description="Dev tools wip"
            )
            embed.add_field(
                name="clear",
                value="prints 500 newlines",
                inline=False
            )
            embed.add_field(
                name="Restart",
                value="Restarts bot",
                inline=False
            )
            embed.add_field(
                name="Load",
                value="Loads a cog",
                inline=False
            )
            embed.add_field(
                name="Unload",
                value="Unloads a cog",
                inline=False
            )
            embed.add_field(
                name="Reload",
                value="Reloads a cog",
                inline=False
            )
            embed.add_field(
                name="ListCogs",
                value="List cogs",
                inline=False
            )
            embed.add_field(
                name="update",
                value="updates to master",
                inline=False
            )
            await ctx.send(embed=embed)
        else:
            pass

    @dev.command()
    async def restart(self, ctx):
        await ctx.send("Shutting down")
        await self.bot.logout()

    @dev.command(name="update")
    async def _git(self, ctx, *arg):
        if "debug" in [x.lower() for x in arg]:
            debug = True
        else:
            debug = False

        async with ctx.typing():
            p = subprocess.Popen(
                ["git", "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p.wait()
            out, err = p.communicate()

            jotain = re.findall(r"cogs/.+?.py", str(out))
            jotain2 = re.findall(r"\|.+?\\n", str(out))

            if "Already up to date" in str(out):
                embed = discord.Embed(title="Already up to date")

            elif jotain == []:
                embed = discord.Embed(
                    title="No cogs where updated",
                    description="""
                    Something in the main script must have updated
                    Bot should be restarted to update the main script
                    """
                )
                pass

            else:
                embed = discord.Embed(
                    title="Updated:",
                )
                for x, k in zip(jotain, jotain2):
                    h = str(x.replace(".py", "").replace("/", "."))
                    _l = str(k.replace("| ", "").replace("\\n", ""))

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
                            value=_l,
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f'Cog "{h}" has errors in it',
                            value=str(e),
                            inline=False
                        )
                    else:
                        embed.add_field(
                            name=f'Cog "{h}" updated',
                            value=_l,
                            inline=False
                        )

        if debug:
            embed.add_field(
                name="Debug:",
                value=str(out),
                inline=False
            )
        await ctx.send(embed=embed)

    @dev.command(aliases=["l"])
    async def load(self, ctx, *, arg):
        cogs_arg = "cogs." + arg
        try:
            self.bot.load_extension(cogs_arg)
            embed = discord.Embed(title=f"Cog: {arg} Loaded.", color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @dev.command(aliases=["u"])
    async def unload(self, ctx, *, arg):
        cogs_arg = "cogs." + arg
        try:
            self.bot.unload_extension(cogs_arg)
            embed = discord.Embed(
                title=f"Cog: {arg} Unloaded.",
                color=0x00ff00
                )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @dev.command(aliases=["r"])
    async def reload(self, ctx, *, arg):
        cogs_arg = "cogs." + arg
        try:
            self.bot.reload_extension(cogs_arg)
            embed = discord.Embed(
                title=f"Cog: {arg} Reloaded.",
                color=0x00ff00
                )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @dev.command(aliases=["listcogs", "lscogs", "lsc"])
    async def _list(self, ctx):

        h = os.scandir("./cogs")
        list_ = []
        for x in h:
            if x.is_file():
                list_.append(x.name.replace(".py", ""))

        list_.remove(".disabled")

        _loaded_cogs = ""
        _cogs = ""
        _loaded = []

        for x in list_:
            try:
                self.bot.load_extension(f"cogs.{x}")
            except commands.ExtensionAlreadyLoaded:
                _loaded.append(x)
            else:
                self.bot.unload_extension(f"cogs.{x}")

        for x in list_:
            _cogs = _cogs + x + "\n"

            if x in _loaded:
                _loaded_cogs = _loaded_cogs + "True \n"
            else:
                _loaded_cogs = _loaded_cogs + "False \n"

        embed = discord.Embed(title="Cogs List")
        embed.add_field(name="Cogs", value=_cogs, inline=True)
        embed.add_field(name="Loaded", value=_loaded_cogs, inline=True)
        embed.add_field(name="debug", value=str(_loaded), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(dev(bot))
