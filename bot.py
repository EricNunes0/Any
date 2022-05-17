import discord
from discord import *
import dotenv
import datetime
from pprint import pprint
from discord_slash import SlashCommand
import random
from random import randint
from discord.ext import commands, tasks
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord_components import *
import re
import textwrap
import json
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = discord.Client()
bot = commands.Bot(command_prefix = "a!", case_insensitive = True,  intents = intents)
command_prefix = "a!"
bot.remove_command("help")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#os.chdir("./images")

@bot.event
async def on_ready():
    activity = discord.Game(name=f"a!help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Estou pronto! Eu sou o {bot.user}")
    DiscordComponents(client)



dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)