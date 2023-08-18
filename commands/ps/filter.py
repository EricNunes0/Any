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


class cog_filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="filter", aliases = ["avataredit","editavatar","filteravatar","avatarfilter"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def filter(self, ctx, member:discord.Member = None, *, filter = None):
        try:
            embed = discord.Embed(title = f"Avatar Edit",
            description = f"**『🖼️✨』** Aplique diferentes filtros em seu avatar!\n**『⚙️』Uso:** `a!avataredit <usuário> <filtro>`\n**『💬』Exemplo:** `{prefix}avataredit invert `{ctx.author.mention}",color = 0xff7b00)
            embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
            embed.add_field(name = "『➖』Invert/Negative", value = "`Inverte as cores`", inline = True)
            embed.add_field(name = "『⬛』Gray/Grayscale", value = "`Preto e branco`", inline = True)
            embed.add_field(name = "『😶‍🌫️』Blur/Desfocar", value = "`Desfoca o avatar`", inline = True)
            embed.add_field(name = "『✏️』Contour/Contornar", value = "`Desenho`", inline = True)
            embed.add_field(name = "『⬜』Emboss", value = "`Cinza`", inline = True)
            embed.add_field(name = "『🖊️』Find edges/fe", value = "`Contorno escuro`", inline = True)
            embed.add_field(name = "『☁️』Smooth/sm", value = "`Suavizar`", inline = True)
            if member == None or filter == None:
                await ctx.reply(embed=embed)
                return
            userAvatar = member.display_avatar.url
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content)).convert('RGB')
            if filter.lower() == "invert" or filter.lower() == "negative":
                print(avatar)
                avatar_edit = ImageOps.invert(avatar)
                print(2)
            elif filter.lower() == "gray" or filter.lower() == "grayscale":
                avatar_edit = avatar.convert("L")
            elif filter.lower() == "blur" or filter.lower() == "desfocar":
                avatar_edit = avatar.filter(ImageFilter.BLUR)
            elif filter.lower() == "contour" or filter.lower() == "contornar":
                avatar_edit = avatar.filter(ImageFilter.CONTOUR)
            elif filter.lower() == "emboss":
                avatar_edit = avatar.filter(ImageFilter.EMBOSS)
            elif filter.lower() == "find edges" or filter.lower() == "fe":
                avatar_edit = avatar.filter(ImageFilter.FIND_EDGES)
            elif filter.lower() == "smooth" or filter.lower() == "sm":
                avatar_edit = avatar.filter(ImageFilter.SMOOTH_MORE)
            else:
                await ctx.send(f"**❌| {ctx.author.mention}**, este filtro não existe.")
            avatar_edit.save('img_filter.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_filter.png")
            psEmbed.set_author(name = f"『🖌』Filter:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_filter.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_filter.py loaded")
    await bot.add_cog(cog_filter(bot))