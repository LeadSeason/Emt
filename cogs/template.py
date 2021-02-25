from discord.ext import commands
import discord

# cog template


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self, ctx):
        import re
        out = "b'Updating 52ead27..1db08e8\nFast-forward\n cogs/template.py | 2 +-\n 1 file changed, 1 insertion"

        jotain = re.findall(r"cogs/.+?.py", str(out))
        jotain2 = re.findall(r"\|.+?\n", str(out))
        print(str(out))
        print(jotain)
        print(jotain2)
        await ctx.send("done")


def setup(bot):
    bot.add_cog(template(bot))
