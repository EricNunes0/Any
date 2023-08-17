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


class cog_tweet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "tweet", aliases = ["twittar", "tw"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def tweet(self, ctx, *, mensagem=None):
        try:
            userAvatar = ctx.author.display_avatar.url
            url = requests.get(userAvatar)
            if mensagem == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, insira um texto!")
                return
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((70,70))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new('L', bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)

            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
            saida.putalpha(mascara)
            saida.save('img_avatar.png')

            backgroundImage = requests.get("https://i.postimg.cc/G2N0SMFw/Tweet.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 20)
            fonte2 = ImageFont.truetype("font_arial.ttf", 30)
            nick = ImageDraw.Draw(img)
            nick.text(xy=(150,60), text=f"{ctx.author.name}", fill=(0, 0, 0), font=fonte1)
            nick.text(xy=(150,80), text=f"@{ctx.author.name}", fill=(100, 100, 100), font=fonte1)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=40)
            texto.text(xy=(70,130), text=f"{textao}", fill=(0, 0, 0), font=fonte2)
            retweets = random.randint(30000,80000)
            likes = random.randint(40000,100000)
            rand = ImageDraw.Draw(img)
            rand.text(xy=(70,323), text=f"{retweets}", fill=(0, 0, 0), font=fonte1)
            rand.text(xy=(255,323), text=f"{likes}", fill=(0, 0, 0), font=fonte1)
            img.paste(avatar, (60, 45), avatar)
            img.save('img_tweet.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_tweet.png")
            psEmbed.set_author(name = f"『🐦』Tweet:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_tweet.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_tweet.py loaded")
    await bot.add_cog(cog_tweet(bot))