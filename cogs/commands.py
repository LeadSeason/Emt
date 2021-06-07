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
import string
import aiohttp
import aiofiles
import traceback

# cog commands


class command(commands.Cog):
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
            traceback.print_last
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

            if foodlist is {'': []}:
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
        async with aiofiles.open("./conf/discord.conf.json") as f:
            API_KEY = json.loads(await f.read())["ytapi"]

        rand = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
        url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults=1&part=snippet&type=video&q={rand}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                if r.status == 200:
                    data = await r.json()
                else:
                    print(f"Error: Website responce:{r.status}")

        vidurl = "https://youtu.be/" + "".join(x["id"]["videoId"] for x in data["items"])
        await ctx.send(vidurl)

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
        elif command not in commands_list:
            await ctx.send(f"{command} in not a command")
            return
        elif usage is None:
            await ctx.send("missing usage arg\ndid you froget to add subcommand=none")
        else:
            if subcommand is None or subcommand.lower() == "none":
                with open("./data/help.json", "r", encoding="utf8") as f:
                    data = json.load(f)

                try:
                    subcommands = data[command]["subcommands"]
                except KeyError:
                    _help = {
                        command: {
                            "description": description,
                            "usage": usage,
                        }
                    }
                    data.update(_help)
                    with open("./data/help.json", 'w', encoding='utf8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                else:
                    _help = {
                        command: {
                            "description": description,
                            "usage": usage,
                            "subcommands": subcommands
                        }
                    }

                    data.update(_help)
                    if subcommand is not None:
                        data[command].update(subcommands)
                    with open("./data/help.json", 'w', encoding='utf8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
            else:
                with open("./data/help.json", "r", encoding="utf8") as f:
                    data = json.load(f)
                try:
                    _ = data[command]["subcommands"]
                except KeyError:
                    _help = {
                        "subcommands": {
                            subcommand: {
                                "description": description,
                                "usage": usage
                            }
                        }
                    }
                    data[command].update(_help)
                    with open("./data/help.json", 'w', encoding='utf8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)

                else:
                    _help = {
                        subcommand: {
                            "description": description,
                            "usage": usage
                        }
                    }
                    data[command]["subcommands"].update(_help)
                    with open("./data/help.json", 'w', encoding='utf8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def helpls(self, ctx):
        commands_list = []
        for x in self.bot.commands:
            commands_list.append(str(x))
        commands_list.sort()

        with open("./data/help.json", "r", encoding="utf8") as f:
            data = json.load(f)

        k = list(data.keys())

        l1 = ""
        l2 = ""

        for x in commands_list:
            if x in k:
                l1 += x + "\n"
                l2 += "True\n"
            else:
                l1 += x + "\n"
                l2 += "False\n"

        embed = discord.Embed(title="helpls")
        embed.add_field(name="keys", value=l1, inline=True)
        embed.add_field(name="commands", value=l2, inline=True)
        await ctx.send(embed=embed)

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

    @commands.command()
    async def rps(self, ctx, arg):
        if arg.lower() in ["rock", "paper", "scissors"]:
            if arg.lower() == "rock":
                embed = discord.Embed(title="I Won", description="You chose Rock, I choose Paper.")
                await ctx.send(embed=embed)
            if arg.lower() == "paper":
                embed = discord.Embed(title="I Won", description="You chose Paper, I choose Scissors.")
                await ctx.send(embed=embed)
            if arg.lower() == "scissors":
                embed = discord.Embed(title="I Won", description="You chose Scissors, I choose Rock.")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Usage", description="You need to choose rock, paper or scissors.")
            await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx):
        if random.randint(1, 2) == 1:
            embed = discord.Embed(title="You rolled tails")
            embed.set_image(url="https://media.discordapp.net/attachments/613368769313636429/822034638661746698/coin.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You rolled heads")
            embed.set_image(url="https://media.discordapp.net/attachments/613368769313636429/822034634383818752/coin_2.png")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def playing(self, ctx, *, arg=None):
        await self.bot.change_presence(activity=discord.Game(arg))

    @commands.command()
    @commands.is_owner()
    async def exec(self, ctx, *, arg):
        try:
            exec(arg)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def dadjoke(self, ctx):
        jokes = [
            "What do you call a factory that makes okay products?" "A satisfactory.",
            "What did the janitor say when he jumped out of the closet?" "Supplies!",
            "Have you heard about the chocolate record player? It sounds pretty sweet.",
            "What did the ocean say to the beach?" "Nothing, it just waved.",
            "Why do seagulls fly over the ocean?" "Because if they flew over the bay, we'd call them bagels.",
            "I only know 25 letters of the alphabet. I don't know y.",
            "What did one wall say to the other?" "I'll meet you at the corner.",
            "What did the zero say to the eight?" "That belt looks good on you.",
            "A skeleton walks into a bar and says, 'Hey, bartender. I'll have one beer and a mop.'",
            "Where do fruits go on vacation?" "Pear-is!",
            "I asked my dog what's two minus two. He said nothing.",
            "What did Baby Corn say to Mama Corn?" "Where's Pop Corn?",
            "What's the best thing about Switzerland?" "I don't know, but the flag is a big plus.",
            "What does a sprinter eat before a race?" "Nothing, they fast!",
            "Where do you learn to make a banana split?" "Sundae school.",
            "Dad, did you get a haircut?" "No, I got them all cut!",
            "What do you call a poor Santa Claus?" "St. Nickel-less.",
            "I got carded at a liquor store, and my Blockbuster card accidentally fell out. The cashier said never mind.",
            "Where do boats go when they're sick?" "To the boat doc.",
            "I don't trust those trees. They seem kind of shady.",
            "My wife is really mad at the fact that I have no sense of direction. So I packed up my stuff and right!",
            "How do you get a squirrel to like you? Act like a nut.",
            "Why don't eggs tell jokes? They'd crack each other up.",
            "I don't trust stairs. They're always up to something.",
            "What do you call someone with no body and no nose? Nobody knows.",
            "Did you hear the rumor about butter? Well, I'm not going to spread it!",
            "Why couldn't the bicycle stand up by itself? It was two tired.",
            "Why did Billy get fired from the banana factory? He kept throwing away the bent ones.",
            "Dad, can you put my shoes on?" "No, I don't think they'll fit me.",
            "Why can't a nose be 12 inches long? Because then it would be a foot.",
            "What does a lemon say when it answers the phone?" "Yellow!",
            "This graveyard looks overcrowded. People must be dying to get in.",
            "What kind of car does an egg drive?" "A yolkswagen.",
            "Dad, can you put the cat out?" "I didn't know it was on fire.",
            "How do you make 7 even?" "Take away the s.",
            "How does a taco say grace?" "Lettuce pray.",
            "What time did the man go to the dentist? Tooth hurt-y.",
            "Why didn't the skeleton climb the mountain?" "It didn't have the guts.",
            "How many tickles does it take to make an octopus laugh? Ten tickles.",
            "I have a joke about chemistry, but I don't think it will get a reaction.",
            "What concert costs just 45 cents? 50 Cent featuring Nickelback!",
            "What does a bee use to brush its hair?" "A honeycomb!",
            "How do you make a tissue dance? You put a little boogie in it.",
            "Why did the math book look so sad? Because of all of its problems!",
            "What do you call cheese that isn't yours? Nacho cheese.",
            "My dad told me a joke about boxing. I guess I missed the punch line.",
            "What kind of shoes do ninjas wear? Sneakers!",
            "How does a penguin build its house? Igloos it together.",
            "You think swimming with sharks is expensive? Swimming with sharks cost me an arm and a leg.",
            "I ordered a chicken and an egg from Amazon. I'll let you know...",
            "Do you wanna box for your leftovers?" "No, but I'll wrestle you for them.",
            "That car looks nice but the muffler seems exhausted.",
            "Shout out to my fingers. I can count on all of them.",
            "If a child refuses to nap, are they guilty of resisting a rest?",
            "What country's capital is growing the fastest?" "Ireland. Every day it's Dublin.",
            "I once had a dream I was floating in an ocean of orange soda. It was more of a fanta sea.",
            "Did you know corduroy pillows are in style? They're making headlines.",
            "Did you hear about the kidnapping at school? It's okay, he woke up.",
            "A cheeseburger walks into a bar. The bartender says, 'Sorry, we don't serve food here.'",
            "I once got fired from a canned juice company. Apparently I couldn't concentrate.",
            "I used to play piano by ear. Now I use my hands.",
            "Have you ever tried to catch a fog? I tried yesterday but I mist.",
            "I'm on a seafood diet. I see food and I eat it.",
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "I made a pencil with two erasers. It was pointless.",
            "How do you make a Kleenex dance? Put a little boogie in it!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Did you hear about the guy who invented the knock-knock joke? He won the 'no-bell' prize.",
            "I've got a great joke about construction, but I'm still working on it.",
            "I used to hate facial hair...but then it grew on me.",
            "I decided to sell my vacuum cleaner—it was just gathering dust!",
            "I had a neck brace fitted years ago and I've never looked back since.",
            "You know, people say they pick their nose, but I feel like I was just born with mine.",
            "What's brown and sticky? A stick.",
            "Why can't you hear a psychiatrist using the bathroom? Because the 'P' is silent.",
            "What do you call an elephant that doesn't matter? An irrelephant.",
            "What do you get from a pampered cow? Spoiled milk.",
            "I like telling Dad jokes. Sometimes he laughs!",
            "What's the best smelling insect?" "A deodor-ant.",
            "I used to be a personal trainer. Then I gave my too weak notice.",
            "Did I tell you the time I fell in love during a backflip? I was heels over head!",
            "If a child refuses to sleep during nap time, are they guilty of resisting a rest?",
            "I ordered a chicken and an egg online. I’ll let you know.",
            "It takes guts to be an organ donor.",
            "If you see a crime at an Apple Store, does that make you an iWitness?",
            "I'm so good at sleeping, I can do it with my eyes closed!",
            "I was going to tell a time-traveling joke, but you guys didn't like it.",
            "Why is Peter Pan always flying?" "He neverlands.",
            "How can you tell if a tree is a dogwood tree?" "By its bark.",
            "I used to hate facial hair, but then it grew on me.",
            "It's inappropriate to make a 'dad joke' if you're not a dad. It's a faux pa.",
            "What do you call a hot dog on wheels?" "Fast food!",
            "Did you hear about the circus fire? It was in tents.",
            "Can February March? No, but April May!",
            "How do lawyers say goodbye? We'll be suing ya!",
            "Wanna hear a joke about paper? Never mind—it's tearable.",
            "What's the best way to watch a fly fishing tournament? Live stream.",
            "Spring is here! I got so excited I wet my plants.",
            "I could tell a joke about pizza, but it's a little cheesy.",
            "Don't trust atoms. They make up everything!",
            "When does a joke become a dad joke? When it becomes apparent.",
            "I wouldn't buy anything with velcro. It's a total rip-off.",
            "What’s an astronaut’s favorite part of a computer? The space bar.",
            "I don't play soccer because I enjoy the sport. I'm just doing it for kicks!",
            "Why are elevator jokes so classic and good? They work on many levels.",
            "Why do bees have sticky hair? Because they use a honeycomb.",
            "What do you call a fake noodle? An impasta.",
            "Which state has the most streets? Rhode Island.",
            "What did the coffee report to the police? A mugging.",
            "What did the fish say when he hit the wall? Dam.",
            "Is this pool safe for diving? It deep ends."
        ]
        await ctx.send(random.choice(jokes))


def setup(bot):
    bot.add_cog(command(bot))
