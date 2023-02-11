import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
from io import BytesIO

c = open("../config.json")
config = json.load(c)

l = open("../link.json")
link = json.load(l)

intents = discord.Intents.default()
intents.members = True

prefix = config["prefix"]
bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec = 0, per_min = 0, per_hour = 0, type = commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

BIRTHDAY_IMAGES = [
    "https://i.imgur.com/6AZV2bX.png",
    "https://i.imgur.com/dSOCKVB.png",
    "https://i.imgur.com/GkxMNbY.png",
    "https://i.imgur.com/cyjxIMu.png",
    "https://i.imgur.com/oijQ1Uh.png",
    "https://i.imgur.com/0sTR7Th.png",
    "https://i.imgur.com/j2Y5ga0.png",
    "https://i.imgur.com/Rhqq0p7.png",
]

bot.ses = aiohttp.ClientSession()
class cog_birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "birthday", aliases = ["happybirthday", "aniversario", "aniversário", "parabens", "parabéns"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def birthday(self, ctx, user: discord.User = None, channel: discord.TextChannel = None, index: int = None):
        try:
            if channel == None:
                channel = ctx.channel
            if user == None:
                user = ctx.author
            if index == None:
                index = 0
            elif index >= len(BIRTHDAY_IMAGES) or index < 0:
                index = 0
            user0Avatar = user.display_avatar.url
            url0 = requests.get(user0Avatar)
            avatar0 = Image.open(BytesIO(url0.content)).convert('RGB')
            avatar0 = avatar0.resize((350, 350))
            bigavatar0 = (avatar0.size[0] * 3, avatar0.size[1] * 3)
            mascara0 = Image.new('L', bigavatar0, 0)
            recortar0 = ImageDraw.Draw(mascara0)
            recortar0.ellipse((0, 0) + bigavatar0, fill=255)
            mascara0 = mascara0.resize(avatar0.size, Image.ANTIALIAS)
            avatar0.putalpha(mascara0)
            saida0 = ImageOps.fit(avatar0, mascara0.size, centering=(0.5, 0.5))
            saida0.putalpha(mascara0)
            response = requests.get(BIRTHDAY_IMAGES[index])
            img = Image.open(BytesIO(response.content)).convert('RGB')
            img.paste(avatar0, (1065, 75), avatar0)
            img.save("img_happybirthday.png")
            await channel.send(content = user.mention, file = discord.File("img_happybirthday.png"))
            return
        except Exception as e:
            print(e)

    @birthday.error
    async def birthday_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)

async def setup(bot):
    print(f"{prefix}birthday")
    await bot.add_cog(cog_birthday(bot))