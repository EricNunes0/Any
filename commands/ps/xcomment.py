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


class cog_xcomment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "xcomment", aliases = ["xc", "xcom", "commentx", "xvideo", "xvideos"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def xcomment(self, ctx, *, mensagem=None):
        try:
            userAvatar = ctx.author.display_avatar.url
            url = requests.get(userAvatar)
            if mensagem == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, insira um texto!")
                return
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((48,48))

            backgroundImage = requests.get("https://i.postimg.cc/tT89M0Tc/X-Comment.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 12)
            fonte2 = ImageFont.truetype("font_arial.ttf", 18)
            nick = ImageDraw.Draw(img)
            nick.text(xy=(65,11), text=f"{ctx.author.name}", fill=(0, 0, 0), font=fonte1)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=40)
            texto.text(xy=(65,30), text=f"{textao}", fill=(0, 0, 0), font=fonte2)
            comenta = random.randint(20,99)
            likes = random.randint(10,99)
            dislikes = random.randint(10,99)
            rand = ImageDraw.Draw(img)
            rand.text(xy=(115,201), text=f"{comenta}", fill=(20, 20, 20), font=fonte1)
            rand.text(xy=(90,176), text=f"{likes}", fill=(120, 120, 120), font=fonte1)
            rand.text(xy=(140,176), text=f"{dislikes}", fill=(120, 120, 120), font=fonte1)
            img.paste(avatar, (10, 11))
            img.save('img_xcomment.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_xcomment.png")
            psEmbed.set_author(name = f"『✖』X Comment:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_xcomment.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_xcomment.py loaded")
    await bot.add_cog(cog_xcomment(bot))