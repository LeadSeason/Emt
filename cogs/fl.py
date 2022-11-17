from discord.ext import commands
import discord
import json
from bs4 import BeautifulSoup as Soup
import datetime
import time
import os
import aiohttp
import traceback


class fl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def genjson(self):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://www.kpedu.fi/palvelut/ravintolat-ja-ruokalistat/menuetti-ja-pikkumenuetti-opiskelijaravintolat") as r:
                if r.status == 200:
                    data = await r.text()
                else:
                    return r.status

        c = Soup(data, "html.parser")
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
            x = x.lower()
            if "maanantai" in x:
                list_food = []
                date = "ma"
                list_food.append(x)
            elif "tiistai" in x or "laskiaistiistai" in x:
                data.update({date: list_food})
                list_food = []
                date = "ti"
                list_food.append(x)
            elif "keskiviikko" in x:
                data.update({date: list_food})
                list_food = []
                date = "ke"
                list_food.append(x)
            elif "torstai" in x:
                data.update({date: list_food})
                list_food = []
                date = "to"
                list_food.append(x)
            elif "perjanta" in x:
                data.update({date: list_food})
                list_food = []
                date = "pe"
                list_food.append(x)
            else:
                list_food.append(x)
        data.update({date: list_food})

        try:
            os.stat("./cache/")
        except FileNotFoundError:
            os.mkdir("./cache/")

        with open("./cache/foods.json", 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
            # json.dump(data, f, indent=4, ensure_ascii=False)
        return "success"

    @commands.command(aliases=["fl", "sapuska"])
    async def foodlist(self, ctx, *args):
        try:
            skip = False
            try:
                file_stat = os.stat("./cache/foods.json").st_mtime

            except FileNotFoundError:
                h = await self.genjson()
                if h == "error":
                    await ctx.channel.send(
                        "there was a error while making the json file")
                    skip = True

            else:
                if time.time() - file_stat > 3600:
                    h = await self.genjson()
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
            tomorrow_args = ["tomorrow", "huomenna"]
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
                            if "ma" in dates:
                                pass
                            else:
                                dates.append("ma")
                        elif datetime.datetime.today().weekday() == 1:
                            if "ti" in dates:
                                pass
                            else:
                                dates.append("ti")
                        elif datetime.datetime.today().weekday() == 2:
                            if "ke" in dates:
                                pass
                            else:
                                dates.append("ke")
                        elif datetime.datetime.today().weekday() == 3:
                            if "to" in dates:
                                pass
                            else:
                                dates.append("to")
                        elif datetime.datetime.today().weekday() == 4:
                            if "pe" in dates:
                                pass
                            else:
                                dates.append("pe")
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
                with open("./cache/foods.json", encoding='utf-8') as s:
                    foodlist = json.load(s)

                if "" in foodlist:
                    await ctx.send("There is no food today 😭")
                else:
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
        except Exception:
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(fl(bot))
