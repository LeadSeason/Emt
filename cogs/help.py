from discord.ext import commands
import discord
import json

# cog help


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="Returns all commands available")
    async def help(self, ctx, arg=None):
        if ctx.invoked_subcommand is None:
            if arg is None:
                arg = "help"
            arg = arg.lower()
            for command in self.bot.commands:
                if arg == command:
                    try:
                        with open("./data/help.json", encoding='utf-8') as s:
                            d = json.load(s)[arg]
                    except FileNotFoundError:
                        await ctx.send("no help.json found")
                    except KeyError:
                        print(f"help for command {arg} doesnt exist")
                        await ctx.send("Help for this command doesn't exist")
                    else:
                        embed = discord.Embed(title="Help")
                        embed.add_field(
                            name="description",
                            value=d["description"],
                            inline=False
                        )
                        embed.add_field(
                            name="usage",
                            value=d["usage"],
                            inline=False
                        )
                        await ctx.send(embed=embed)

                    break
            else:
                await ctx.send("Command doesn't exist")

    @help.command()
    @commands.is_owner()
    async def add(self, ctx):
        await ctx.send("command not done yet")
        pass

    @help.command()
    @commands.is_owner()
    async def subadd(self, ctx):
        await ctx.send("command not done yet")
        pass


def setup(bot):
    bot.add_cog(help(bot))