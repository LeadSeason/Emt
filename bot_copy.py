import json
import importlib
import os
from discord.ext import commands


class bot():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=";")
        self.bot_cog_load()
        self.bot.run(str(self.get_token()))

    def get_token(self):
        with open("./conf/discord.conf.json") as discord_conf:
            return json.load(discord_conf)["token"]

    def bot_cog_load(self):
        with open("./cogs/.disabled") as a:
            disabled = a.read().splitlines()

        h = os.scandir("./cogs")
        _list = []
        for x in h:
            if x.is_file():
                _list.append(x.name)

        try:
            _list.remove(".disabled")
        except Exception:
            pass

        for cube in disabled:
            if cube.startswith("#"):
                disabled.remove(cube)

        for x in _list:
            try:
                _cog_name = "cogs."+x.replace(".py", "")
                if x in disabled:
                    raise NameError
                importlib.import_module(_cog_name)
                self.bot.load_extension(_cog_name)
            except commands.ExtensionError as e:
                print(f"""Failure: Cogs: "{_cog_name}" failed to load""")
                print(e)
            except NameError:
                print(f"""Disabled: Cogs: "{_cog_name}" wasn't loaded""")
            except Exception as e:
                print(f"""Failure: Cogs: "{_cog_name}" failed to load""")
                print(e)
            else:
                print(f"""Enabled : Cogs: "{_cog_name}" loaded""")
