from discord.ext import commands
import discord

# cog events


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")


def setup(bot):
    bot.add_cog(events(bot))
