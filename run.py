import subprocess


p = subprocess.Popen(["git", "pull"])
p.wait()
from bot import bot
bot()
