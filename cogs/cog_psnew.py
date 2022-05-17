import discord
from discord.ext import commands
import requests
import datetime
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
import textwrap
from io import BytesIO
import json
intents = discord.Intents.default()
intents.members = True

now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

#def get_prefix(bot, message):
#    with open('prefixes.json', 'r') as f:
#        prefixes = json.load(f)
#    return prefixes[str(message.guild.id)]
command_prefix = "a!"
bot = commands.Bot(command_prefix = "a!", intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class cog_ps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="photoshop", aliases = ["ps","🖼️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def photoshop(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『🖼️』Photoshop [22]",description =  "**`avataredit - bbb22 - candidato - captcha - christmasgift - clyde - 🛠️crewmate - facecomment - facepost - fato - hipocrisia - instacomment - laranjo - mine - notstonks - pp - srincrivel - stonks - tweet - ytcomment - xcomment - zapmessage`**",color = 0xff7b00)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
        await ctx.reply(embed=embed)

    @commands.command(name="mine")
    @cooldown(1,5, type = commands.BucketType.user)
    async def mine(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            return await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((80,80))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')
        img = Image.open("img_conquista.png")
        fonte = ImageFont.truetype("font_Minecraft.ttf", 35)
        escrever = ImageDraw.Draw(img)
        escrever.text(xy=(118,75), text=f"{mensagem}", fill=(230, 230, 230), font=fonte)
        img.paste(avatar, (25, 25), avatar)
        img.save('img_conquistamine.png')
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>|**", file=discord.File('img_conquistamine.png'))

    
def setup(bot):
    bot.add_cog(cog_ps(bot))