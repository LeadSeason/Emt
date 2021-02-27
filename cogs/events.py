from discord.ext import commands
import discord

# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "is this bot smart" in str(message.content).lower:
            await message.channel.send("Hell yeah I am!")


def setup(bot):
    bot.add_cog(template(bot))
