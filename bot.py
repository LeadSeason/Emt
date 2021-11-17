import importlib
import os
from discord.ext import commands
import subprocess
from dotenv import load_dotenv


class CogDisabled(Exception):
    pass


def getconf(arg):
    return os.environ.get(arg)


def bot_cog_load(bot):

    _list = []
    try:
        with os.scandir("./cogs") as h:
            for x in h:
                if not x.name.startswith(".") and x.is_file():
                    _list.append(x.name)
    except FileNotFoundError:
        print("No ./cogs/ folder can't load cogs")
        return

    try:
        _list.remove(".disabled")
    except ValueError:
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
                raise CogDisabled
            importlib.import_module(_cog_name)
            bot.load_extension(_cog_name)
        except commands.ExtensionError as e:
            print(
                f"""Failure: Cogs: "{_cog_name}" failed to load"""
            )
            print(e)
        except CogDisabled:
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


load_dotenv()

if getconf("UPDATE_ON_START") is True:
    print("updating...")
    p = subprocess.Popen(["git", "pull"])
    p.wait()

bot = commands.Bot(
    command_prefix=getconf("PREFIX"),
    case_insensitive=True,
    self_bot=False,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot_cog_load(bot)
bot.run(str(getconf("TOKEN")))
