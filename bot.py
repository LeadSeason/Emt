import json
import importlib
import os
import logging
import discord
import datetime
from discord.ext import commands


class bot():
    def __init__(self):
        self.logging_setup()
        self.bot = commands.Bot(
            command_prefix=";",
            case_insensitive=True,
            self_bot=False,
            help_command=None
            )
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
                logging.error(f"""Failure: Cogs: "{_cog_name}" failed to load""")
                logging.error(e)
            except NameError:
                logging.info(f"""Disabled: Cogs: "{_cog_name}" wasn't loaded""")
            except Exception as e:
                logging.error(f"""Failure: Cogs: "{_cog_name}" failed to load""")
                logging.error(e)
            else:
                logging.info(f"""Enabled : Cogs: "{_cog_name}" loaded""")

    def logging_setup(self):
        dt = datetime.datetime.today()
        filenamestart = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
        for x in range(9999):
            filename = filenamestart + "-" + str(x) + ".log"
            if not os.path.exists("./logs/" + filename):
                break

        self.logger = logging.getLogger('discord')
        self.handler = logging.FileHandler(
            filename="./logs/" + filename,
            encoding='utf-8',
            mode='w'
            )
        self.handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
            ))
        self.logger.addHandler(self.handler)
