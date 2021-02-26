import logging as log
import subprocess
import json


def get_conf(data):
    with open("./conf/github.conf.json") as discord_conf:
        return json.load(discord_conf)[data]


def run_command(data):
    p = subprocess.Popen(data.split())
    p.wait()


log.basicConfig(format='%(levelname)s:%(message)s')
try:
    from bot import bot
except ModuleNotFoundError:
    log.error("Bot isn't installed")
    log.info("installing...")
    repo = "https://" + get_conf("username") + ":"
    repo = repo + get_conf("token") + "@" + get_conf("repo")
    run_command("git init")
    run_command("git remote add origin " + repo)
    run_command("git pull origin master")

from bot import bot
p = subprocess.Popen(["git", "pull"])
p.wait()
bot()
