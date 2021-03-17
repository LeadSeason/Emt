from discord.ext import commands
import discord
import random
import asyncio
import re
import subprocess
import uwuify
import platform
import json
import requests
from bs4 import BeautifulSoup as Soup
import datetime
import time
import os

# cog play


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generate_jsonfile()

    def generate_jsonfile(self):
        try:
            url = "https://www.kpedu.fi/palvelut/ravintolat-ja-ruokalistat/menuetti-ja-pikkumenuetti-opiskelijaravintolat"
            data = requests.get(url)

            c = Soup(data.content, "html.parser")
            c = c.find_all("div", class_="content-expanded-list")
            c = Soup(str(c), "html.parser")
            foods = c.find_all("p")

            h = ""
            for x in foods[1:]:
                h = h + x.get_text() + "\n"

            food_list = list(h.split("\n"))
            while True:
                try:
                    food_list.remove("\xa0")
                except ValueError:
                    break
            food_list.remove("")

            list_food = []
            date = ""
            data = {}
            for x in food_list:
                if x.startswith("MAANANTAI"):

                    list_food = []
                    date = "ma"
                    list_food.append(x)
                elif x.startswith("TIISTAI"):
                    data.update({date: list_food})
                    list_food = []
                    date = "ti"
                    list_food.append(x)
                elif x.startswith("LASKIAISTIISTAI"):
                    data.update({date: list_food})
                    list_food = []
                    date = "ti"
                    list_food.append(x)
                elif x.startswith("KESKIVIIKKO"):
                    data.update({date: list_food})
                    list_food = []
                    date = "ke"
                    list_food.append(x)
                elif x.startswith("TORSTAI"):
                    data.update({date: list_food})
                    list_food = []
                    date = "to"
                    list_food.append(x)
                elif x.startswith("PERJANTA"):
                    data.update({date: list_food})
                    list_food = []
                    date = "pe"
                    list_food.append(x)
                else:
                    list_food.append(x)
            data.update({date: list_food})

            with open("./data/foods.json", 'w', encoding='utf8') as f:
                json.dump(data, f, ensure_ascii=False)
                # json.dump(data, f, indent=4, ensure_ascii=False)
            return "success"
        except Exception as e:
            print(e)
            return "error"

    @commands.command(aliases=["fl", "sapuska"])
    async def foodlist(self, ctx, *args):
        skip = False
        try:
            file_stat = os.stat("./data/foods.json").st_mtime

        except FileNotFoundError:
            h = self.generate_jsonfile()
            if h == "error":
                await ctx.channel.send(
                    "there was a error while making the json file")
                skip = True

        else:
            if time.time() - file_stat > 3600:
                h = self.generate_jsonfile()
                if h == "error":
                    await ctx.channel.send(
                        "there was a error while making the json file")
                    skip = True

        sapuska = ""

        if args == ():
            sapuska = "Viikon sapuskat"
            args = ["ma", "ti", "ke", "to", "pe"]

        date = ""
        dates = []
        ma_args = ["manantai", "ma", "mon", "monday"]
        ti_args = ["tiistai", "ti", "tue", "tues", "tuesday"]
        ke_args = ["keskiviikko", "ke", "wed", "weds", "wednesday"]
        to_args = ["torstai", "to", "thu", "thur", "thurs", "thursday"]
        pe_args = ["perjantai", "pe", "fri", "friday"]
        today_args = ["today", "tänään"]
        help_args = ["help", "apua", "h", "?"]

        for input_arg in args:
            date = input_arg.lower()

            if date in ma_args:
                if "ma" in dates:
                    pass
                else:
                    dates.append("ma")

            elif date in ti_args:
                if "ti" in dates:
                    pass
                else:
                    dates.append("ti")

            elif date in ke_args:
                if "ke" in dates:
                    pass
                else:
                    dates.append("ke")

            elif date in to_args:
                if "to" in dates:
                    pass
                else:
                    dates.append("to")

            elif date in pe_args:
                if "pe" in dates:
                    pass
                else:
                    dates.append("pe")

            elif date in help_args:
                if "help" in dates:
                    pass
                else:
                    dates.append("help")
            elif date in today_args:
                if "today" in dates:
                    pass
                else:
                    if datetime.datetime.today().weekday() == 0:
                        dates.append("ma")
                    elif datetime.datetime.today().weekday() == 1:
                        dates.append("ti")
                    elif datetime.datetime.today().weekday() == 2:
                        dates.append("ke")
                    elif datetime.datetime.today().weekday() == 3:
                        dates.append("to")
                    elif datetime.datetime.today().weekday() == 4:
                        dates.append("pe")
                    else:
                        pass
            else:
                pass

        args = dates

        if args == []:
            embed = discord.Embed(
                title="",
                description="""
                invalid argument where given
                see ;foodlist help for help
                """,
                color=0xFF5733
            )
            await ctx.send(embed=embed)
            skip = True

        if "help" in args:
            des = """
            ",foodlist help" to show this
            ",foodlist" to show all days
            ",foodlist specific day" to show a specific day
            valid days are ma ti ke to pe
            """
            embed = discord.Embed(
                title="food list",
                description=des,
                color=0x4d4d4d
            )
            await ctx.send(embed=embed)
            skip = True

        if not skip:
            with open("./data/foods.json", encoding='utf-8') as s:
                foodlist = json.load(s)

            if str(foodlist) is {'': []}:
                await ctx.send("There is food today 😞")

            if not sapuska == "Viikon sapuskat":
                sapuska = "Sapuskat"
                if len(args) == 1:
                    sapuska = "Tänä päivän Sapuskaa"

            embed = discord.Embed(title=sapuska, color=0x4d4d4d)

            args2 = ["ma", "ti", "ke", "to", "pe"]
            for x in args2:
                if x in args:
                    k = foodlist[x]
                    foods = "\n"
                    foods = foods.join(k[1:])
                    embed.add_field(name=k[0], value=foods, inline=False)

            await ctx.send(embed=embed)

    @commands.command(name="typing")
    async def _typing(self, ctx, arg="5"):
        try:
            arg = int(arg)
            if arg > 120:
                raise TypeError
        except ValueError:
            await ctx.send("Argument needs to be a number.")
        except TypeError:
            await ctx.send("Argument too high.")
        else:
            async with ctx.typing():
                await asyncio.sleep(arg)
            await ctx.send("Hello")

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, arg):
        a = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don’t count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes – definitely.",
            "You may rely on it.",
        ]

        wish = ctx.message.author.name + " asked the 8ball:"
        respose = random.choice(a)

        embed = discord.Embed(title="8Ball")
        embed.add_field(name=wish, value=arg, inline=False)
        embed.add_field(name="8ball responds:", value=respose, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, *, arg=None):
        if arg is None:
            randint = random.randint(1, 100)
            await ctx.send(f"You rolled {randint}!")
        else:
            ints = list(map(int, re.findall(r"\d+", arg)))
            if not len(ints) == 2:
                embed = discord.Embed(
                    title="Too many or little args",
                    description="example: ;roll 1-100"
                )
                await ctx.send(embed=embed)
            else:
                try:
                    randint = random.randint(ints[0], ints[1])
                except ValueError:
                    randint = random.randint(ints[1], ints[0])
                    await ctx.send(f"You rolled {randint}!")
                else:
                    await ctx.send(f"You rolled {randint}!")

    @commands.command(aliases=["ryt"])
    async def randomytvid(self, ctx):
        if platform.system() == "Windows":
            p = subprocess.Popen(
                ["py", "./utils/ytapi.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif platform.system() == "Linux":
            p = subprocess.Popen(
                ["python3", "./utils/ytapi.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            raise RuntimeError("Unknow platform")

        p.wait()
        out, err = p.communicate()
        await ctx.send(str(out).replace("b'", "", 1).replace("\\n'", ""))

    @commands.command()
    async def uwuify(self, ctx, *, arg):
        flags = uwuify.SMILEY | uwuify.YU
        await ctx.send(uwuify.uwu(arg, flags=flags))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {str(round(self.bot.latency * 1000))}ms")

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
    bot.add_cog(play(bot))
