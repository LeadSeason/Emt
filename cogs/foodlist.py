from discord.ext import commands
import discord
import time
import os
import json
import requests
import datetime
from bs4 import BeautifulSoup as Soup

# cog Foodlist


class foodlist(commands.Cog):
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
            h = self.generate_jsonfile(ctx.author)
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
            print(str(foodlist))

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


def setup(bot):
    bot.add_cog(foodlist(bot))
