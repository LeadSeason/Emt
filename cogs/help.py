from discord.ext import commands
import discord
import json

# cog help


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Help for commands")
    async def help(self, ctx, arg=None):
        if ctx.invoked_subcommand is None:
            commands_list = []
            for x in self.bot.commands:
                commands_list.append(str(x))

            if arg is None:
                arg = "help"
            arg = arg.lower()

            if arg in commands_list:
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
                    try:
                        keys = ""
                        for x in list(d["subcommands"].keys()):
                            keys = keys + x + " "
                        embed.add_field(
                            name="Subcommands",
                            value=keys,
                            inline=False
                        )
                    except KeyError as e:
                        print(f"error:{e}")
                        pass
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Command doesn't exist")

    @commands.command()
    @commands.is_owner()
    async def helpadd(self, ctx):
        await ctx.send("command not done yet")
        pass

    @commands.command()
    @commands.is_owner()
    async def helpsubadd(self, ctx):
        await ctx.send("command not done yet")
        pass

    @commands.command(name="commands")
    async def idkjotain(self, ctx):
        commands_list = []
        hidden = ["dev", "helpsubadd", "helpadd"]
        for x in self.bot.commands:
            if x not in hidden:
                commands_list.append(str(x))

        outstr = ""
        for x in commands_list:
            outstr = outstr + x + "\n"
        embed = discord.Embed(
            title="Commands",
            description=outstr
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
