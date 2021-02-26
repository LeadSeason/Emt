import logging as log
import subprocess
import json


def get_conf(data):
    with open("./conf/github.conf.json") as github:
        return json.load(github)[data]


def run_command(data):
    log.info("running command" + data.split())
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
    run_command("git clone " + repo)
    run_command("cp -r Emt/*")

from bot import bot
p = subprocess.Popen(["git", "pull"])
p.wait()
bot()
