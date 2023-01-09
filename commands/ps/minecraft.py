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


class cog_minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "minecraft", aliases = ["mine"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def mine(self, ctx, *, message = None):
        try:
            if message == None:
                await ctx.reply(f"『❌』 {ctx.author.mention}, insira um texto.")
                return
            userAvatar = ctx.author.display_avatar.url
            url = requests.get(userAvatar)
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
            escrever.text(xy = (118,75), text = f"{message}", fill = (230, 230, 230), font = fonte)
            img.paste(avatar, (25, 25), avatar)
            img.save("img_conquistamine.png")
            mineEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            mineEmbed.set_image(url = "attachment://img_conquistamine.png")
            mineEmbed.set_author(name = f"『🧊』Minecraft:", icon_url = self.bot.user.display_avatar.url)
            mineEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = mineEmbed, file=discord.File('img_conquistamine.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_minecraft.py loaded")
    await bot.add_cog(cog_minecraft(bot))