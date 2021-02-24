from discord.ext import commands
import discord
import os

# cog Template


class cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.group(hidden=True)
    async def cogs(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Cogs", description="Cog tools")
            embed.add_field(name="Load", value="Loads a cog", inline=False)
            embed.add_field(name="Unload", value="Unloads a cog", inline=False)
            embed.add_field(name="Reload", value="Reloads a cog", inline=False)
            embed.add_field(name="List", value="List cogs", inline=False)
            await ctx.send(embed=embed)

    @cogs.command(aliases=["l"])
    async def load(self, ctx, arg):
        cogs_arg = "cogs." + arg
        try:
            self.bot.load_extension(cogs_arg)
            embed = discord.Embed(title=f"Cog: {arg} Loaded.", color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

    @cogs.command(aliases=["u"])
    async def unload(self, ctx, arg):
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

    @cogs.command(aliases=["r"])
    async def reload(self, ctx, arg):
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

    @cogs.command(aliases=["ls", "dir", "list"])
    async def _list(self, ctx):

        h = os.scandir("./cogs")
        list_ = []
        for x in h:
            if x.is_file():
                list_.append(x.name.replace(".py", ""))

        list_.remove(".disabled")

        _loaded_cogs = ""
        _cogs = ""
        _loaded = list(self.bot.cogs.keys())

        for x in list_:
            _cogs = _cogs + x + "\n"

            if x in _loaded:
                _loaded_cogs = _loaded_cogs + "True \n"
            else:
                _loaded_cogs = _loaded_cogs + "False \n"

        embed = discord.Embed(title="Cogs List")
        embed.add_field(name="Cogs", value=_cogs, inline=True)
        embed.add_field(name="Loaded", value=_loaded_cogs, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(cogs(bot))
