import os
from discord.ext import commands
from loguru import logger
import json

with open("data/config.json", "r") as f:
    config = json.load(f)
    
token = config["botToken"]
client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command('help')


def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            client.load_extension(f"cogs.{name}")
            logger.info(f"Loaded cogs.{name}")


load_cogs()
client.run(token)
