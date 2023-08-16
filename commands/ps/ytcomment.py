import discord
from discord.ext import commands
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json

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


class cog_ytcomment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ytcomment", aliases = ["youtube", "youtubecomment", "yt", "ytc"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def ytcomment(self, ctx, *, mensagem=None):
        try:
            userAvatar = ctx.author.display_avatar.url
            url = requests.get(userAvatar)
            if mensagem == None:
                await ctx.reply(f"『❌』{ctx.author.mention}, insira um texto!")
                return
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((40,40))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new('L', bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)

            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
            saida.putalpha(mascara)
            saida.save('img_avatar.png')

            backgroundImage = requests.get("https://i.postimg.cc/d1KNbqL4/YT-Comment.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 12)
            fonte2 = ImageFont.truetype("font_arial.ttf", 13)
            nick = ImageDraw.Draw(img)
            nick.text(xy=(70,16), text=f"{ctx.author.name}", fill=(255, 255, 255), font=fonte1)
            texto = ImageDraw.Draw(img)
            texto.text(xy=(70,37), text=f"{mensagem}", fill=(255, 255, 255), font=fonte2)
            img.paste(avatar, (15, 14), avatar)
            img.save('img_ytcomment.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_ytcomment.png")
            psEmbed.set_author(name = f"『🎥』YT Comment:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_ytcomment.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_ytcomment.py loaded")
    await bot.add_cog(cog_ytcomment(bot))