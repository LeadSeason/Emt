from discord.ext import commands
import discord
import random
import asyncio
import re
import subprocess
import uwuify
# cog template


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(aliases=["randomytvid"])
    async def ryt(self, ctx):

        p = subprocess.Popen(
            ["python3", "./utils/ytapi.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        p.wait()
        out, err = p.communicate()
        await ctx.send(str(out).replace("b", "", 1).replace("'", ""))

    @commands.command()
    async def uwuify(self, ctx, *, arg):
        await ctx.send(uwuify.uwu())


def setup(bot):
    bot.add_cog(play(bot))
