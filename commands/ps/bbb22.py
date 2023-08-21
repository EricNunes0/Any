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


class cog_bbb22(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "bbb22", aliases = ["22bbb"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def bbb22(self, ctx, member:discord.Member = None):
        try:
            if member == None:
                member = ctx.author
            userAvatar = member.display_avatar.url
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((140,140))
            backgroundImage = requests.get("https://i.postimg.cc/RhMYtxSN/BBB22.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_bebas.ttf", 40)
            fonte2 = ImageFont.truetype("font_bebas.ttf", 32)
            age = random.randint(13,51)
            jobs = ["Desempregado(a)","Ator","Cantor(a)","Empresário(a)","Influencer","Youtuber","Tiktoker","Modelo","Estudante","Jogador de Futebol","Surfista","Medico(a)","Veterinario(a)","Engenheiro(a)","Designer","Editor(a)","Humorista","Atleta"]
            job = random.choice(jobs)
            infos = ImageDraw.Draw(img)
            infos.text(xy=(230,75), text=f"{member.name}", fill=(1, 184, 252), font=fonte1)
            infos.text(xy=(230,115), text=f"{age} anos", fill=(244, 226, 32), font=fonte2)
            infos.text(xy=(230,148), text=f"{job}", fill=(1, 184, 252), font=fonte2)
            img.paste(avatar, (62, 80))
            img.save('img_bbb22.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_bbb22.png")
            psEmbed.set_author(name = f"『📹』BBB 22:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_bbb22.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_bbb22.py loaded")
    await bot.add_cog(cog_bbb22(bot))