import datetime
from pprint import pprint
from discord_slash import SlashCommand
import random
from random import randint
from dotenv import load_dotenv
import discord
from discord import activity, client, member, Embed, ActionRow, Button, ButtonStyle
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

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)