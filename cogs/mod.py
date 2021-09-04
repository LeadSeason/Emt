from discord.errors import NotFound
from discord.ext import commands
import discord

# cog mod


class mod(commands.Cog):
    """
        moderason commands
        commands to be made
        ;ban        -- bans user from server
        ;unban      -- unban unbans a user from server
        ;kick       -- throws user outofthe server
        ;selfkick   -- throws calling user outofthe server
        ;clear      -- ;clear ammount
        ;mute       -- mutes a user from talking
        ;unmute     -- unmute unmutes userfrom server
        ;userinfo   -- userinfo gets info from user
        ;serverinfo -- serverinfo data of server
        ;roleinfo   -- role info shows permissions and stuff like that
        ;nick       -- change nick for user
        ;slowmode   -- slowmode turns on slow mode
        ;warn       -- warn warning to keep track of misbehaviour
        ;warns      -- warns list warning for user
        ;tmpmute    -- mutes user from talking unmutes after time
        ;tmpban    -- temporary ban
        ;lockdown   -- lockdown disables every one from talking in the server'
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User = None, reason=None):
        if member is None:
            await ctx.send("pwease specify da usew to be banned")
        elif member == ctx.message.author:
            await ctx.send("ya cannot ban yah self")
        else:
            if reason is None:
                reason = "oi cunt get off the bloody servrer"

            await ctx.guild.ban(member, reason=reason)
            await member.send(f"U have been banned fwom `{ctx.guild.name}` fow wason `{reason}`")

            embed = discord.Embed(title="User has been banned ", description=f"Ban reason: `{reason}`")
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("pwease specify da usew to be unbanned")
        elif member == ctx.message.author:
            await ctx.send("ya cannot unban yah self")
        else:
            try:
                await ctx.guild.unban(member)
                await ctx.send("Member unbanned")
            except discord.errors.NotFound:
                await ctx.send("Cant ban member when member isnt banned")


def setup(bot):
    bot.add_cog(mod(bot))
