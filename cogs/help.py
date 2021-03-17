from discord.ext import commands
import discord
import json

# cog help


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Help for commands")
    async def help(self, ctx, arg=None, subcommand=None):
        commands_list = []
        for x in self.bot.commands:
            commands_list.append(str(x))

        if arg is None:
            arg = "help"
        arg = arg.lower()

        if arg in commands_list:
            if subcommand is None:
                try:
                    with open("./data/help.json", encoding='utf-8') as s:
                        d = json.load(s)[arg]
                except FileNotFoundError:
                    await ctx.send("no help.json found")
                except KeyError:
                    print(f"help for command {arg} doesnt exist")
                    await ctx.send("Help for this command doesn't exist")
                except TypeError:
                    print("./data/help.json is fucked")
                    await ctx.send("help.json is fucked")
                else:
                    embed = discord.Embed(title=arg.capitalize())
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
                        if not keys == "":
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
                try:
                    with open("./data/help.json", encoding='utf-8') as s:
                        d = json.load(s)[arg]["subcommands"][subcommand]
                except FileNotFoundError:
                    await ctx.send("no help.json found")
                except KeyError:
                    print(f"help for command {arg} doesnt exist")
                    await ctx.send("Help for this subcommand doesn't exist")
                else:
                    embed = discord.Embed(title=arg + " " + subcommand)
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
        else:
            await ctx.send("Command doesn't exist")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def helprm(self, ctx, command=None, subcommand=None):
        commands_list = []
        for x in self.bot.commands:
            commands_list.append(str(x))
        if command is None:
            embed = discord.Embed(title="Helprm")
            embed.add_field(
                name="description",
                value="Removes help for a command or subcommand",
                inline=False
            )
            embed.add_field(
                name="usage",
                value=";Helprm <command> <subcommand>",
                inline=False
            )
            await ctx.send(embed=embed)
        elif subcommand is None and command in commands_list:
            with open("./data/help.json", "r", encoding="utf8") as f:
                data = json.load(f)
            try:
                data.pop(command)
            except KeyError:
                await ctx.send(f"{command} is not a command or there is no help for this command")
            else:
                with open("./data/help.json", 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        elif command in commands_list:
            with open("./data/help.json", "r", encoding="utf8") as f:
                data = json.load(f)
            try:
                data[command]["subcommands"].pop(subcommand)
            except KeyError:
                await ctx.send(f"{subcommand} is not a command or there is no help for this command")
            else:
                with open("./data/help.json", 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def helpadd(self, ctx, command=None, subcommand=None, description=None, usage=None):
        commands_list = []
        for x in self.bot.commands:
            commands_list.append(str(x))
        if command not in commands_list:
            await ctx.send(f"{command} in not a command")
            return
        if command is None:
            embed = discord.Embed(title="Helpadd")
            embed.add_field(
                name="description",
                value="adds help for a command or subcommand",
                inline=False
            )
            embed.add_field(
                name="usage",
                value=";Help add <command> <subcommand> <'description'> <'usage'>",
                inline=False
            )
            await ctx.send(embed=embed)
        elif usage is None:
            await ctx.send("missing usage arg\ndid you froget to add subcommand=none")
        else:
            if subcommand is None or subcommand.lower() == "none":
                with open("./data/help.json", "r", encoding="utf8") as f:
                    data = json.load(f)
                subcommands = data[command]["subcommands"]
                _help = {
                    command: {
                        "description": description,
                        "usage": usage,
                        "subcommands": subcommands
                    }
                }

                data.update(_help)
                data[command].update(subcommands)
                with open("./data/help.json", 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                _help = {
                    subcommand: {
                        "description": description,
                        "usage": usage
                    }
                }
                with open("./data/help.json", "r", encoding="utf8") as f:
                    data = json.load(f)
                data[command]["subcommands"].update(_help)
                with open("./data/help.json", 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

    @commands.command(name="commands")
    async def idkjotain(self, ctx):
        commands_list = []
        for x in self.bot.commands:
            if not x.hidden:
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
