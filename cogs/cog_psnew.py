import discord
from discord.ext import commands
import requests
import datetime
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
import textwrap
from io import BytesIO
import json
intents = discord.Intents.default()
intents.members = True

now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

#def get_prefix(bot, message):
#    with open('prefixes.json', 'r') as f:
#        prefixes = json.load(f)
#    return prefixes[str(message.guild.id)]
command_prefix = "a!"
bot = commands.Bot(command_prefix = "a!", intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class cog_ps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="photoshop", aliases = ["ps","🖼️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def photoshop(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『🖼️』Photoshop [22]",description =  "**`avataredit - bbb22 - candidato - captcha - christmasgift - clyde - 🛠️crewmate - facecomment - facepost - fato - hipocrisia - instacomment - laranjo - mine - notstonks - pp - srincrivel - stonks - tweet - ytcomment - xcomment - zapmessage`**",color = 0xff7b00)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(cog_ps(bot))