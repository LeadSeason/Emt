import logging as log
import subprocess
import json


def get_conf(data):
    with open("./conf/github.conf.json") as discord_conf:
        return json.load(discord_conf)[data]


log.basicConfig(format='%(levelname)s:%(message)s')
try:
    from bot import bot
except ModuleNotFoundError:
    log.error("Bot isn't installed")
    log.info("installing...")
    repo = "https://" + get_conf("username") + ":" + get_conf("token") + "@" + get_conf("repo")
    p = subprocess.Popen(["git", "clone", repo, "."])
    p.wait()

from bot import bot
p = subprocess.Popen(["git", "pull"])
p.wait()
bot()
