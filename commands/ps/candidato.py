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


class cog_candidato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "candidato", aliases = ["candidata", "candidatar", "candidate"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def candidato(self, ctx, member: discord.Member = None):
        try:
            if not member:
                member = ctx.message.author
            userAvatar = member.display_avatar.url
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((450,450))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new('L', bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)

            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
            saida.putalpha(mascara)
            saida.save('img_avatar.png')

            backgroundImage = requests.get("https://cdn.discordapp.com/attachments/1141841573039054920/1141841979139965019/img_candidato1.png")
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 70)
            fonte2 = ImageFont.truetype("font_arial.ttf", 45)
            nick = ImageDraw.Draw(img)
            nick.text(xy=(585,180), text=f"{member.name}", fill=(255, 255, 255), font=fonte1)
            randomCand = ["Presidente","Prefeito","Governador","Vereador","Deputado Federal","Deputado Estadual"]
            randomCandidato = random.choice(randomCand)
            randomPart = ["Partido da Índole Nacional do Tráfico de Ovos - PINTO","Partido do Queijo Parmesão - PQP","Partido do Amantes de Uvas - PAU","Partido Estadual dos Navegadores da Internet Semanal - PENIS","Partido dos Opositores a Memes Cringes - POMC","Partido dos Postadores de Vídeos Cringes - PPVC","Partido dos Apreciadores dos Carros de Ovos - PACO"]
            randomPartido = random.choice(randomPart)
            rand = ImageDraw.Draw(img)
            rand.text(xy=(585,250), text=f"{randomCandidato}", fill=(255, 255, 255), font=fonte1)
            rand.text(xy=(585,330), text=f"{randomPartido}", fill=(255, 255, 255), font=fonte2)
            img.paste(avatar, (60, 90), avatar)
            img.save('img_candidato.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_candidato.png")
            psEmbed.set_author(name = f"『👤』Candidato:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_candidato.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_candidato.py loaded")
    await bot.add_cog(cog_candidato(bot))