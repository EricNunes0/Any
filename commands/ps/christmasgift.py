import discord
from discord.ext import commands
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json
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


class cog_christmasgift(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "christmasgift", aliases = ["giftchristmas","natalpresente","presentenatal","natalgift","giftnatal","cg"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def christmasgift(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        try:
            if member1 == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, mencione um usuário!")
                return
            if member2 == None:
                member2 = member1
                member1 = ctx.author
            userAvatar1 = member1.display_avatar.url
            url1 = requests.get(userAvatar1)
            userAvatar2 = member2.display_avatar.url
            url2 = requests.get(userAvatar2)
            
            avatar1 = Image.open(BytesIO(url1.content))
            avatar1 = avatar1.resize((120,120))
            bigavatar1 = (avatar1.size[0] * 3, avatar1.size[1] * 3)
            mascara1 = Image.new('L', bigavatar1, 0)
            recortar1 = ImageDraw.Draw(mascara1)
            recortar1.ellipse((0, 0) + bigavatar1, fill=255)
            mascara1 = mascara1.resize(avatar1.size, Image.ANTIALIAS)
            avatar1.putalpha(mascara1)
            
            saida = ImageOps.fit(avatar1, mascara1.size, centering=(0.5, 1.5))
            saida.putalpha(mascara1)
            saida.save('img_avatar.png')
            
            avatar2 = Image.open(BytesIO(url2.content))
            avatar2 = avatar2.resize((95,95))
            bigavatar2 = (avatar2.size[0] * 3, avatar2.size[1] * 3)
            mascara2 = Image.new('L', bigavatar2, 0)
            recortar2 = ImageDraw.Draw(mascara2)
            recortar2.ellipse((0, 0) + bigavatar2, fill=255)
            mascara2 = mascara1.resize(avatar2.size, Image.ANTIALIAS)
            avatar2.putalpha(mascara2)
            
            saida = ImageOps.fit(avatar2, mascara2.size, centering=(0.5, 1.5))
            saida.putalpha(mascara2)
            saida.save('img_avatar(1).png')
            
            backgroundImage = requests.get("https://i.postimg.cc/sx20bG9k/Christmas-Gift.png")
            img = Image.open(BytesIO(backgroundImage.content))
            img.paste(avatar1, (125, 240), avatar1)
            img.paste(avatar2, (470, 170), avatar2)
            img.save('img_christmasgift.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_christmasgift.png")
            psEmbed.set_author(name = f"『🎄』Christmas Gift:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_christmasgift.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_christmasgift.py loaded")
    await bot.add_cog(cog_christmasgift(bot))