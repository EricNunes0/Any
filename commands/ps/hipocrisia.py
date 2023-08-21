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


class cog_hipocrisia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "hipocrisia", aliases = ["hipocrita","felipeneto"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def hipocrisia(self, ctx, *, mensagem=None):
        try:
            if mensagem == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, insira um texto!")
                return
            backgroundImage = requests.get("https://cdn.discordapp.com/attachments/1141841573039054920/1142976370377502811/img_hipocrisia.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 70)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=28)
            texto.text(xy=(870,70), text=f"{textao}", fill=(255, 255, 255), font=fonte1)
            img.save('img_hipocrisia.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_hipocrisia.png")
            psEmbed.set_author(name = f"『🐶』Hipocrisia:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_hipocrisia.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_hipocrisia.py loaded")
    await bot.add_cog(cog_hipocrisia(bot))