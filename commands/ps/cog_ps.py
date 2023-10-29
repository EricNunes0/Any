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

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users=json.load(f)

    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change 

    with open("mainbank.json","w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

class cog_ps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="photoshop", aliases = ["ps","🖼️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def photoshop(self, ctx):
        prefix = "a!"
        embed = discord.Embed(title = f"『🖼️』Photoshop [22]",description =  "**`avataredit - bbb22 - candidato - captcha - christmasgift - clyde - 🛠️crewmate - facecomment - facepost - fato - hipocrisia - instacomment - laranjo - mine - notstonks - pp - srincrivel - stonks - tweet - ytcomment - xcomment - zapmessage`**",color = 0xff7b00)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {prefix}help <comando>", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
        await ctx.reply(embed=embed)

    @commands.command(name="facepost", aliases = ["postface"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def facepost(self, ctx, i:int = None, *, mensagem=None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]    
        embed = discord.Embed(
            title = "Gerador de Postagens do Facebook",
            description = f"**✨|** Cria postagens de Facebook!\n**⚙️| Uso:** `{prefix}facepost <num> Texto aqui`\n**💬| Exemplo:** `{prefix}facepost 1 Olá, pessoal!`",
            color = 0xff7b00
        )
        embed.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
        embed.add_field(name = "📙| Sala laranja", value = "Número: `1`", inline = True)
        embed.add_field(name = "📘| Azul e verde", value = "Número: `2`", inline = True)
        embed.add_field(name = "☁️| Nuvens", value = "Número: `3`", inline = True)
        embed.add_field(name = "🟦| Fundo azul marinho", value = "Número: `4`", inline = True)
        embed.add_field(name = "🔵| Fundo azul", value = "Número: `5`", inline = True)
        embed.add_field(name = "🟢| Fundo verde", value = "Número: `6`", inline = True)
        embed.add_field(name = "🟠| Fundo laranja", value = "Número: `7`", inline = True)
        embed.add_field(name = "⛰️| Montanhas vermelhas", value = "Número: `8`", inline = True)
        embed.add_field(name = "😍| Olhos de coração", value = "Número: `9`", inline = True)
        embed.add_field(name = "💩| Cocô", value = "Número: `10`", inline = True)
        embed.add_field(name = "❤️| Coração", value = "Número: `11`", inline = True)
        embed.add_field(name = "🔥| Fogo", value = "Número: `12`", inline = True)
        embed.add_field(name = "🤣| Risos", value = "Número: `13`", inline = True)
        embed.set_thumbnail(url="https://images.vexels.com/media/users/3/152579/isolated/lists/a52ce2d4014c39b7b7c5974a1a1cbb85-icone-de-ponto-de-interrogacao-do-circulo-laranja.png")
        if i == None or mensagem == None:
            return await ctx.reply(embed=embed)
        elif i == 1:
            img = Image.open("img_facepost(1).png")
        elif i == 2:
            img = Image.open("img_facepost(2).png")
        elif i == 3:
            img = Image.open("img_facepost(3).png")
        elif i == 4:
            img = Image.open("img_facepost(4).png")
        elif i == 5:
            img = Image.open("img_facepost(5).png")
        elif i == 6:
            img = Image.open("img_facepost(6).png")
        elif i == 7:
            img = Image.open("img_facepost(7).png")
        elif i == 8:
            img = Image.open("img_facepost(8).png")
        elif i == 9:
            img = Image.open("img_facepost(9).png")
        elif i == 10:
            img = Image.open("img_facepost(10).png")
        elif i == 11:
            img = Image.open("img_facepost(11).png")
        elif i == 12:
            img = Image.open("img_facepost(12).png")
        elif i == 13:
            img = Image.open("img_facepost(13).png")
        else:
            return await ctx.reply(embed=embed)
        fonte1 = ImageFont.truetype("font_coolvetica_rg.ttf", 30)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=30)
        texto.text(xy=(20,20), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_facepost.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +**", file=discord.File('img_facepost.png'))   

    @commands.command(name="zapmessage", aliases = ["zapmsg"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def zapmessage(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        now = datetime.datetime.now()
        now = now.strftime("%H:%M")
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((105,105))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)

        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')

        zap1 = Image.open("img_zapmessage(1).png")
        zap2 = Image.open("img_zapmessage(2).png")
        zap3 = Image.open("img_zapmessage(3).png")
        zap4 = Image.open("img_zapmessage(4).png")
        zap5 = Image.open("img_zapmessage(5).png")
        zap6 = Image.open("img_zapmessage(6).png")
        zap7 = Image.open("img_zapmessage(7).png")
        zap8 = Image.open("img_zapmessage(8).png")
        zap9 = Image.open("img_zapmessage(9).png")
        zap10 = Image.open("img_zapmessage(10).png")
        zap11 = Image.open("img_zapmessage(11).png")
        zap12 = Image.open("img_zapmessage(12).png")
        zap13 = Image.open("img_zapmessage(13).png")
        zap14 = Image.open("img_zapmessage(14).png")
        zap15 = Image.open("img_zapmessage(15).png")
        zap16 = Image.open("img_zapmessage(16).png")
        zap17 = Image.open("img_zapmessage(17).png")
        zap18 = Image.open("img_zapmessage(18).png")
        zap19 = Image.open("img_zapmessage(19).png")
        zap20 = Image.open("img_zapmessage(20).png")
        zap21 = Image.open("img_zapmessage(21).png")
        zap22 = Image.open("img_zapmessage(22).png")
        zap23 = Image.open("img_zapmessage(23).png")
        zap24 = Image.open("img_zapmessage(24).png")
        zap25 = Image.open("img_zapmessage(25).png")
        zap26 = Image.open("img_zapmessage(26).png")
        zaps = [zap1,zap2,zap3,zap4,zap5,zap6,zap7,zap8,zap9,zap10,zap11,zap12,zap13,zap14,zap15,zap16,zap17,zap18,zap19,zap20,zap21,zap22,zap23,zap24,zap25,zap26]
        zap = random.choice(zaps)
        fonte1 = ImageFont.truetype("font_arial.ttf", 40)
        fonte2 = ImageFont.truetype("font_arial.ttf", 50)
        fonte3 = ImageFont.truetype("font_arial.ttf", 28)
        nick = ImageDraw.Draw(zap)
        nick.text(xy=(175,40), text=f"{ctx.author.name}", fill=(255, 255, 255), font=fonte1)
        texto = ImageDraw.Draw(zap)
        textao = textwrap.fill(text=mensagem, width=29)
        texto.text(xy=(175,165), text=f"{textao}", fill=(255, 255, 255), font=fonte2)
        texto.text(xy=(890,1069), text=f"{now}", fill=(170, 210, 170), font=fonte3)
        zap.paste(avatar, (63, 18), avatar)
        zap.save('img_zapmessage.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +**", file=discord.File('img_zapmessage.png'))

async def setup(bot):
    print("cog_ps.py loaded")
    await bot.add_cog(cog_ps(bot))