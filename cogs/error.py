from discord.ext import commands
import discord
import traceback

# cog error


class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You aren't a bot dev")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("you dont have permissions for that command")
        else:
            traceback.print_exc
            print(error)


def setup(bot):
    bot.add_cog(error(bot))
