from discord.ext import commands
import discord
import json
import aiohttp
import asyncio
import datetime
# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getdata_search(self, arg2):
        with open("./conf/wot_conf.json") as discord_conf:
            wot_apikey = json.load(discord_conf)["api_key"]
        baseurl = "https://api.worldoftanks.eu/wot"

        async with aiohttp.ClientSession() as session:
            async with session.get(url=baseurl + "/account/list/" + wot_apikey + f"&search={arg2}") as req:
                user = await req.json()
            if int(user["meta"]["count"]) == 0:
                return "notfound"
            return int(user["data"][0]["account_id"])

    async def getdata_list(self, arg1):
        with open("./conf/wot_conf.json") as discord_conf:
            wot_apikey = json.load(discord_conf)["api_key"]
        baseurl = "https://api.worldoftanks.eu/wot"

        async with aiohttp.ClientSession() as session:
            async with session.get(url=baseurl + "/account/info/" + wot_apikey + f"&account_id={arg1}") as req:
                user = await req.json()
            if user["status"] == "ok":
                return user
            elif user["status"] == "error":
                return "notfound"

    async def timeconvert(self, arg):
        return datetime.datetime.utcfromtimestamp(int(arg)).strftime(' %d-%m-%Y %H:%M:%S\n')

    @commands.command()
    async def playerstats(self, ctx, username: str = None):
        user_id = await self.getdata_search(username)
        if user_id == "notfound":
            print("error player not found")
            await ctx.send("error")
        else:
            user_id = str(user_id)
            data = await self.getdata_list(user_id)
            user_data = data["data"][user_id]
            des = "Account made:" + await self.timeconvert(user_data["created_at"])
            des += "Rank: " + str(user_data["global_rating"])
            des += "\nlast battle:" + await self.timeconvert(user_data["last_battle_time"])
            embed = discord.Embed(title="player stats for player " + user_data["nickname"], color=0x4d4d4d, description=des)
            user_stats = user_data["statistics"]["all"]
            stats_des = "max_xp: " + str(user_stats["max_xp"])
            stats_des += "\nbattles: " + str(user_stats["battles"])
            stats_des += "\nwins: " + str(user_stats["wins"])
            stats_des += "\nlosses: " + str(user_stats["losses"])
            winluus = int((user_stats["wins"] / (int(user_stats["wins"]) + int(user_stats["losses"]))) * 100)
            stats_des += "\nwin ratio: " + str(round(int(winluus), 5)) + "%"
            stats_des += "\nmax_frag: " + str(user_stats["max_frags"])
            stats_des += "\nTree cut: " + str(user_data["statistics"]["trees_cut"])
            embed.add_field(name="Stats", value=stats_des, inline=False)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(template(bot))
