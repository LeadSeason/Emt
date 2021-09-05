from discord.ext import commands
import discord

# cog mod


class mod(commands.Cog):
    """
        moderason commands
        commands to be made
        ;ban        Done -- bans user from server
        ;unban      Done -- unban unbans a user from server
        ;kick       Done -- throws user outofthe server
        ;selfkick   -- throws calling user outofthe server
        ;clear      Done -- ;clear ammount
        ;mute       Done -- mutes a user from talking
        ;unmute     done -- unmute unmutes userfrom server
        ;userinfo   -- userinfo gets info from user
        ;serverinfo -- serverinfo data of server
        ;roleinfo   -- role info shows permissions and stuff like that
        ;nick       done -- change nick for user
        ;slowmode   -- slowmode turns on slow mode
        ;warn       -- warn warning to keep track of misbehaviour
        ;warns      -- warns list warning for user
        ;tmpmute    -- mutes user from talking unmutes after time
        ;tmpban     -- temporary ban
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
            try:
                await member.send(f"U have been banned fwom `{ctx.guild.name}` fow wason `{reason}`")
            except discord.errors.Forbidden:
                print("chouldent send dm to {member}")
            embed = discord.Embed(title=f"{member.mention} has been banned ", description=f"Ban reason: `{reason}`")
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=["uban"])
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

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.User = None, reason=None):
        if member is None:
            await ctx.send("pwease specify da usew to be kicked")
        elif member == ctx.message.author:
            await ctx.send("ya cannot kick yah self")
        else:
            if reason is None:
                reason = "oi cunt get off the bloody servrer"

            await ctx.guild.kick(member, reason=reason)
            try:
                await member.send(f"U have been kicked fwom `{ctx.guild.name}` fow wason `{reason}`")
            except discord.errors.Forbidden:
                print("couldn't send dm to {member}")
            embed = discord.Embed(title=f"{member.mention} has been kicked ", description=f"Ban reason: `{reason}`")
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, ammount=25):
        try:
            ammount = int(ammount)
        except ValueError:
            await ctx.send("U wetawtawd stwing ow whatevew u sent isnt a numbew")
        else:
            await ctx.channel.purge(limit=ammount)
            embed = discord.Embed(title=f"Cleared {ammount} messages", description=f"{ctx.author} has cleard {ammount} messages")
            await ctx.send(embed=embed)

    @commands.command(aliases=["stfu"])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, reason=None):

        muterole = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muterole:
            muterole = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muterole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(muterole, reason=reason)
        embed = discord.Embed(title="STFU", description=f"{member.mention} was muted ")
        if reason is not None:
            embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["umute"])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):

        muterole = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muterole:
            muterole = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muterole, speak=False, send_messages=False)

        await member.remove_roles(muterole)
        embed = discord.Embed(title=f"Unmuted {member}", description=f"{member.mention} was muted ")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, nick=None):
        if nick is not None:
            name_old = member.display_name
            await member.edit(nick=nick)
            embed = discord.Embed(title=f"Nickname was changed for {name_old}", description=f"Nickname changed from `{name_old}` to {member.mention}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("specify the nick name")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        pass


def setup(bot):
    bot.add_cog(mod(bot))
