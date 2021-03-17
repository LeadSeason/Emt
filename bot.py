import json
import importlib
import os
from discord.ext import commands
import subprocess


def get_token():
    with open("./conf/discord.conf.json") as discord_conf:
        return json.load(discord_conf)["token"]


def bot_cog_load(bot):

    try:
        h = os.scandir("./cogs")
    except FileNotFoundError:
        print("No ./cogs/ folder can't load cogs")
        return

    _list = []
    for x in h:
        if x.is_file():
            _list.append(x.name)

    try:
        _list.remove(".disabled")
    except Exception:
        pass

    try:
        with open("./cogs/.disabled") as a:
            disabled = a.read().splitlines()

        for x in disabled:
            if x.startswith("#"):
                disabled.remove(x)
    except FileNotFoundError:
        disabled = []
        print("No disabled list")

    for x in _list:
        try:
            _cog_name = "cogs." + x.replace(".py", "")
            if x in disabled:
                raise NameError
            importlib.import_module(_cog_name)
            bot.load_extension(_cog_name)
        except commands.ExtensionError as e:
            print(
                f"""Failure: Cogs: "{_cog_name}" failed to load"""
            )
            print(e)
        except NameError:
            print(
                f"""Disabled: Cogs: "{_cog_name}" wasn't loaded"""
            )
        except Exception as e:
            print(
                f"""Failure: Cogs: "{_cog_name}" failed to load"""
            )
            print(e)
        else:
            print(f"""Enabled : Cogs: "{_cog_name}" loaded""")


print("updating...")
p = subprocess.Popen(["git", "pull"])
p.wait()

bot = commands.Bot(
    command_prefix=";",
    case_insensitive=True,
    self_bot=False,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot_cog_load(bot)
bot.run(str(get_token()))
