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


class cog_captcha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "captcha", aliases = ["recaptcha", "catpcha"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def captcha(self, ctx, member:discord.Member = None, *, mensagem=None):
        try:
            if member == None:
                await ctx.send(f"『❌』{ctx.author.mention}, informe um usuário e o texto.")
            if mensagem == None:
                await ctx.send(f"『❌』{ctx.author.mention}, informe um usuário e o texto.")
            userAvatar = member.display_avatar.url
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((80,80))

            backgroundImage = requests.get("https://i.postimg.cc/G2HrPR1V/Captcha.jpg")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 12)
            fonte2 = ImageFont.truetype("font_arial.ttf", 18)
            nick = ImageDraw.Draw(img)
            nick.text(xy=(20,11), text=f"{ctx.author.name}", fill=(255, 255, 255), font=fonte1)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=40)
            texto.text(xy=(20,30), text=f"{textao}", fill=(255, 255, 255), font=fonte2)
            img.paste(avatar, (4, 82)) #X1
            img.paste(avatar, (86, 82)) #X2
            img.paste(avatar, (167, 82)) #X3
            img.paste(avatar, (4, 163)) #Y1
            img.paste(avatar, (86, 163)) #Y2
            img.paste(avatar, (167, 163)) #Y3
            img.paste(avatar, (4, 245)) #Z1
            img.paste(avatar, (86, 245)) #Z2
            img.paste(avatar, (167, 245)) #Z3
            img.save('img_captcha.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_captcha.png")
            psEmbed.set_author(name = f"『☑』Captcha:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_captcha.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_captcha.py loaded")
    await bot.add_cog(cog_captcha(bot))