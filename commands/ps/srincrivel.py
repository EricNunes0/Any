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


class cog_srincrivel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "srincrivel", aliases = ["sr_incrivel", "srincrível", "senhorincrivel", "senhorincrível"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def srincrivel(self, ctx, i:int = None, *, mensagem=None):
        try:
            senhores = [
                {
                    "id": 1,
                    "name": "Normal",
                    "emoji": "🙂",
                    "image": "https://i.postimg.cc/prCcz91G/Sr-Incrivel-1.png"
                },
                {
                    "id": 2,
                    "name": "Preto e branco",
                    "emoji": "🙁",
                    "image": "https://i.postimg.cc/XYmHf6Qb/Sr-Incrivel-2.png"
                },
                {
                    "id": 3,
                    "name": "Poker Face",
                    "emoji": "😐",
                    "image": "https://i.postimg.cc/66fmDS5r/Sr-Incrivel-3.png"
                },
                {
                    "id": 4,
                    "name": "Feliz",
                    "emoji": "😀",
                    "image": "https://i.postimg.cc/QtkfZ9s8/Sr-Incrivel-4.png"
                },
                {
                    "id": 5,
                    "name": "Muito feliz",
                    "emoji": "😃",
                    "image": "https://i.postimg.cc/sXRTLPkH/Sr-Incrivel-5.png"
                },
                {
                    "id": 6,
                    "name": "Óculos",
                    "emoji": "😎",
                    "image": "https://i.postimg.cc/rFhYpr4z/Sr-Incrivel-6.png"
                },
                {
                    "id": 7,
                    "name": "Óculos azul",
                    "emoji": "😎",
                    "image": "https://i.postimg.cc/526KQ25g/Sr-Incrivel-7.png"
                },
                {
                    "id": 8,
                    "name": "Colorido",
                    "emoji": "🕶️",
                    "image": "https://i.postimg.cc/ncVPZkC6/Sr-Incrivel-8.png"
                },
                {
                    "id": 9,
                    "name": "Malvado",
                    "emoji": "😈",
                    "image": "https://i.postimg.cc/mkL8LL2Q/Sr-Incrivel-9.png"
                },
                {
                    "id": 10,
                    "name": "Olhos vermelhos",
                    "emoji": "😈",
                    "image": "https://i.postimg.cc/c1hFDnXT/Sr-Incrivel-10.png"
                },
                {
                    "id": 11,
                    "name": "GLORIOUS",
                    "emoji": "😮",
                    "image": "https://i.postimg.cc/QCfSV2Hv/Sr-Incrivel-11.png"
                },
                {
                    "id": 12,
                    "name": "Assustado",
                    "emoji": "😶",
                    "image": "https://i.postimg.cc/FHdGsnmn/Sr-Incrivel-12.png"
                },
                {
                    "id": 13,
                    "name": "Creepy Poker Face",
                    "emoji": "😥",
                    "image": "https://i.postimg.cc/kXhfCdrb/Sr-Incrivel-13.png"
                },
                {
                    "id": 14,
                    "name": "Perturbado",
                    "emoji": "😶",
                    "image": "https://i.postimg.cc/c4JXPLzW/Sr-Incrivel-14.png"
                },
                {
                    "id": 15,
                    "name": "Dark",
                    "emoji": "😶",
                    "image": "https://i.postimg.cc/MpC5cbpZ/Sr-Incrivel-15.png"
                }
            ]
            embed = discord.Embed(
                title = "Criador de memes do Sr. Incrível",
                description = f"『✨』Faça seus próprios memes do Sr. Incrível com o seu próprio texto!\n**『⚙️』Uso:** `a!srincrivel <num> Texto aqui`\n**『💬』Exemplo:** `a!srincrivel 1 Sr. Incrível feliz`",
                color = discord.Color.from_rgb(255, 100, 20)
            )
            embed.add_field(name = "『🙂』Normal", value = "Número: `1`", inline = True)
            for senhor in senhores:
                embed.add_field(name = f"『{senhor['emoji']}』{senhor['name']}", value = f"Número: `{senhor['id']}`", inline = True)
            embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
            embed.set_footer(text=f"Pedido por {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            global srIncrivelURL
            srIncrivelURL = None
            if i == None or mensagem == None:
                await ctx.reply(embed=embed)
                return
            else:
                for senhor in senhores:
                    if senhor["id"] == i:
                        srIncrivelURL = senhor["image"]
                if srIncrivelURL == None:
                    await ctx.reply(embed=embed)
                    print("Sr. Incrível falhou ;-;")
                    return
            backgroundImage = requests.get(srIncrivelURL)
            img = Image.open(BytesIO(backgroundImage.content))
            fonte1 = ImageFont.truetype("font_arial.ttf", 20)
            texto = ImageDraw.Draw(img)
            textao = textwrap.fill(text=mensagem, width=25)
            texto.text(xy=(10,10), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
            img.save('img_sr_incrivel.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_sr_incrivel.png")
            psEmbed.set_author(name = f"『ℹ』Sr. Incrível:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_sr_incrivel.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_srincrivel.py loaded")
    await bot.add_cog(cog_srincrivel(bot))