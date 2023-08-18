import discord
from discord.ext import commands
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json
import textwrap
import random

c = open("../config.json")
config = json.load(c)

l = open("../link.json")
link = json.load(l)

intents = discord.Intents.default()
intents.members = True

prefix = config["prefix"]
bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")


class cog_fatos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "fatos", aliases = ["fato", "facts", "fact"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def fatos(self, ctx, *, mensagem=None):
        try:
            if mensagem == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, insira um texto!")
                return
            backgroundImage = requests.get("https://i.postimg.cc/L8smZ2w8/Fatos.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 20)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=20)
            texto.text(xy=(10,10), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
            img.save('img_fatos.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_fatos.png")
            psEmbed.set_author(name = f"『🤓』Fatos:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_fatos.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_fatos.py loaded")
    await bot.add_cog(cog_fatos(bot))