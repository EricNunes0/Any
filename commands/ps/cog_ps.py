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
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『🖼️』Photoshop [22]",description =  "**`avataredit - bbb22 - candidato - captcha - christmasgift - clyde - 🛠️crewmate - facecomment - facepost - fato - hipocrisia - instacomment - laranjo - mine - notstonks - pp - srincrivel - stonks - tweet - ytcomment - xcomment - zapmessage`**",color = 0xff7b00)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
        await ctx.reply(embed=embed)

    @commands.command(name="tweet")
    @cooldown(1,5, type = commands.BucketType.user)
    async def tweet(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((70,70))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)

        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')

        img = Image.open("img_tweet(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 20)
        fonte2 = ImageFont.truetype("font_arial.ttf", 30)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(150,60), text=f"{ctx.author.name}", fill=(0, 0, 0), font=fonte1)
        nick.text(xy=(150,80), text=f"@{ctx.author.name}", fill=(100, 100, 100), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=40)
        texto.text(xy=(70,130), text=f"{textao}", fill=(0, 0, 0), font=fonte2)
        retweets = random.randint(30000,80000)
        likes = random.randint(40000,100000)
        rand = ImageDraw.Draw(img)
        rand.text(xy=(70,323), text=f"{retweets}", fill=(0, 0, 0), font=fonte1)
        rand.text(xy=(255,323), text=f"{likes}", fill=(0, 0, 0), font=fonte1)
        img.paste(avatar, (60, 45), avatar)
        img.save('img_tweet.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_tweet.png'))

    @commands.command(name="candidato")
    @cooldown(1,5, type = commands.BucketType.user)
    async def candidato(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
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

        img = Image.open("img_candidato(1).png")
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
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**",file=discord.File('img_candidato.png'))

    @commands.command(name="clyde")
    @cooldown(1,5, type = commands.BucketType.user)
    async def clyde(self, ctx, *, mensagem=None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y às %H:%M")
        if mensagem == None:
            return await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        img = Image.open("img_clyde(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 18)
        fonte2 = ImageFont.truetype("font_arial.ttf", 21)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(225,35), text=f"{now}", fill=(140, 140, 140), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=55)
        texto.text(xy=(110,60), text=f"{textao}", fill=(220, 220, 220), font=fonte2)
        img.save('img_clyde.png')
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**",file=discord.File('img_clyde.png'))

    @commands.command(name="christmasgift", aliases = ["giftchristmas","natalpresente","presentenatal","natalgift","giftnatal"])
    @cooldown(1,8, type = commands.BucketType.user)
    async def christmasgift(self, ctx, member:discord.Member = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if member == None:
            return await ctx.send(f"❌| Por favor {ctx.author.mention}, mencione um usuário.\n⁉| Para mais informações sobre o comando, digite `{prefix}help christmasgift`")
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        userAvatar1 = member.avatar_url
        url1 = requests.get(userAvatar1)
        
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((120,120))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        
        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')
        
        avatar1 = Image.open(BytesIO(url1.content))
        avatar1 = avatar1.resize((95,95))
        bigavatar1 = (avatar1.size[0] * 3, avatar1.size[1] * 3)
        mascara1 = Image.new('L', bigavatar1, 0)
        recortar1 = ImageDraw.Draw(mascara1)
        recortar1.ellipse((0, 0) + bigavatar1, fill=255)
        mascara1 = mascara1.resize(avatar1.size, Image.ANTIALIAS)
        avatar1.putalpha(mascara1)
        
        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar(1).png')
        
        img = Image.open("img_natal(1).png")
        img.paste(avatar, (125, 240), avatar)
        img.paste(avatar1, (470, 170), avatar1)
        img.save('img_natal.png')
        
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 8
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**",file=discord.File('img_natal.png'))

    @commands.command(name="laranjo")
    @cooldown(1,5, type = commands.BucketType.user)
    async def laranjo(self, ctx, *, mensagem=None):
        if mensagem == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        img = Image.open("img_laranjo(1).jpg")
        fonte1 = ImageFont.truetype("font_arial.ttf", 30)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=42)
        texto.text(xy=(15,15), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_laranjo.jpg')
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**",file=discord.File('img_laranjo.jpg'))

    @commands.command(name="fato", aliases = ["fatos"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def fato(self, ctx, *, mensagem=None):
        if mensagem == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 6
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        img = Image.open("img_fato(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 20)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=20)
        texto.text(xy=(10,10), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_fato.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}** {ctx.author.mention}", file=discord.File('img_fato.png'))

    @commands.command(name="srincrivel", aliases = ["sr_incrivel"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def srincrivel(self, ctx, i:int = None, *, mensagem=None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if i == None or mensagem == None:
            embed = discord.Embed(
                title = "Criador de memes do Sr. Incrível",
                description = f"**✨|** Faça seus próprios memes do Sr. Incrível com o seu próprio texto!\n**⚙️| Uso:** `{prefix}srincrivel <num> Texto aqui`\n**💬| Exemplo:** `{prefix}srincrivel 1 Sr. Incrível feliz`",
                color = 0xff7b00
            )
            embed.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            embed.add_field(name = "🙂| Normal", value = "Número: `1`", inline = True)
            embed.add_field(name = "🙁| Preto e branco", value = "Número: `2`", inline = True)
            embed.add_field(name = "😐| Poker face", value = "Número: `3`", inline = True)
            embed.add_field(name = "😀| Feliz", value = "Número: `4`", inline = True)
            embed.add_field(name = "😃| Muito feliz", value = "Número: `5`", inline = True)
            embed.add_field(name = "😎| Óculos", value = "Número: `6`", inline = True)
            embed.add_field(name = "😎| Óculos azul", value = "Número: `7`", inline = True)
            embed.add_field(name = "🕶️| Colorido", value = "Número: `8`", inline = True)
            embed.add_field(name = "😈| Malvado", value = "Número: `9`", inline = True)
            embed.add_field(name = "😈| Olhos vermelhos", value = "Número: `10`", inline = True)
            embed.add_field(name = "😮| GLORIUS", value = "Número: `11`", inline = True)
            embed.add_field(name = "😶| Assustado", value = "Número: `12`", inline = True)
            embed.add_field(name = "😥| Creepy Poker Face", value = "Número: `13`", inline = True)
            embed.add_field(name = "😶| Pertubado", value = "Número: `14`", inline = True)
            embed.add_field(name = "😶| Dark", value = "Número: `15`", inline = True)
            embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
            return await ctx.reply(embed=embed)
        elif i == 1:
            img = Image.open("img_sr_incrivel(1).png")
        elif i == 2:
            img = Image.open("img_sr_incrivel(2).png")
        elif i == 3:
            img = Image.open("img_sr_incrivel(3).png")
        elif i == 4:
            img = Image.open("img_sr_incrivel(4).png")
        elif i == 5:
            img = Image.open("img_sr_incrivel(5).png")
        elif i == 6:
            img = Image.open("img_sr_incrivel(6).png")
        elif i == 7:
            img = Image.open("img_sr_incrivel(7).png")
        elif i == 8:
            img = Image.open("img_sr_incrivel(8).png")
        elif i == 9:
            img = Image.open("img_sr_incrivel(9).png")
        elif i == 10:
            img = Image.open("img_sr_incrivel(10).png")
        elif i == 11:
            img = Image.open("img_sr_incrivel(11).png")
        elif i == 12:
            img = Image.open("img_sr_incrivel(12).png")
        elif i == 13:
            img = Image.open("img_sr_incrivel(13).png")
        elif i == 14:
            img = Image.open("img_sr_incrivel(14).png")
        elif i == 15:
            img = Image.open("img_sr_incrivel(15).png")
        else:
            print("Sr. Incrível falhou ;-;")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 6
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        fonte1 = ImageFont.truetype("font_arial.ttf", 20)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=25)
        texto.text(xy=(10,10), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_sr_incrivel.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_sr_incrivel.png'))

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
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 6
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        fonte1 = ImageFont.truetype("font_coolvetica_rg.ttf", 30)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=30)
        texto.text(xy=(20,20), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_facepost.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_facepost.png'))

    @commands.command(name="facecomment", aliases = ["facecom"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def facecomment(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((50,50))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)

        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')

        img = Image.open("img_facecomment(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 18)
        fonte2 = ImageFont.truetype("font_arial.ttf", 22)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(75,20), text=f"{ctx.author.name}", fill=(255, 255, 255), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=40)
        texto.text(xy=(75,45), text=f"{textao}", fill=(255, 255, 255), font=fonte2)
        comenta = random.randint(20,150)
        likes = random.randint(100,500)
        rand = ImageDraw.Draw(img)
        rand.text(xy=(97,283), text=f"{comenta}", fill=(200, 200, 200), font=fonte1)
        rand.text(xy=(526,241), text=f"{likes}", fill=(255, 255, 255), font=fonte1)
        img.paste(avatar, (7, 9), avatar)
        img.save('img_facecomment.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_facecomment.png'))

    @commands.command(name="instacomment", aliases = ["instacom"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def instacomment(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((35,35))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)

        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save('img_avatar.png')

        img = Image.open("img_instacomment(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 12)
        fonte2 = ImageFont.truetype("font_arial.ttf", 18)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(55,15), text=f"{ctx.author.name}", fill=(0, 0, 0), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=40)
        texto.text(xy=(55,30), text=f"{textao}", fill=(0, 0, 0), font=fonte2)
        comenta = random.randint(20,99)
        likes = random.randint(300,999)
        rand = ImageDraw.Draw(img)
        rand.text(xy=(191,253), text=f"{comenta}", fill=(120, 120, 120), font=fonte1)
        rand.text(xy=(93,219), text=f"{likes}", fill=(120, 120, 120), font=fonte1)
        img.paste(avatar, (14, 3), avatar)
        img.save('img_instacomment.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_instacomment.png'))

    @commands.command(name="xcomment", aliases = ["xcom"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def xcomment(self, ctx, *, mensagem=None):
        userAvatar = ctx.author.avatar_url
        url = requests.get(userAvatar)
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((48,48))

        img = Image.open("img_xcomment(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 12)
        fonte2 = ImageFont.truetype("font_arial.ttf", 18)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(65,11), text=f"{ctx.author.name}", fill=(0, 0, 0), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=40)
        texto.text(xy=(65,30), text=f"{textao}", fill=(0, 0, 0), font=fonte2)
        comenta = random.randint(20,99)
        likes = random.randint(10,99)
        dislikes = random.randint(10,99)
        rand = ImageDraw.Draw(img)
        rand.text(xy=(115,201), text=f"{comenta}", fill=(20, 20, 20), font=fonte1)
        rand.text(xy=(90,176), text=f"{likes}", fill=(120, 120, 120), font=fonte1)
        rand.text(xy=(140,176), text=f"{dislikes}", fill=(120, 120, 120), font=fonte1)
        img.paste(avatar, (10, 11))
        img.save('img_xcomment.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_xcomment.png'))

    @commands.command(name="pp", aliases = ["primeiraspalavras"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def pp(self, ctx, *, mensagem=None):
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)

        img = Image.open("img_pp(1).jpeg")
        fonte1 = ImageFont.truetype("font_arial.ttf", 38)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=18)
        texto.text(xy=(60,340), text=f"{textao}", fill=(0, 0, 0), font=fonte1)
        img.save('img_pp.jpeg')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_pp.jpeg'))

    @commands.command(name="captcha", aliases = ["recaptcha"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def captcha(self, ctx, member:discord.Member = None, *, mensagem=None):
        if member == None:
            member = ctx.author
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, informe um usuário e o texto.")
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((80,80))

        img = Image.open("img_captcha(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 12)
        fonte2 = ImageFont.truetype("font_arial.ttf", 18)
        nick = ImageDraw.Draw(img)
        nick.text(xy=(20,11), text=f"{ctx.author.name}", fill=(255, 255, 255), font=fonte1)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=40)
        texto.text(xy=(20,30), text=f"{textao}", fill=(255, 255, 255), font=fonte2)
        img.paste(avatar, (4, 82)) #X1
        img.paste(avatar, (86, 82)) #X2
        img.paste(avatar, (167, 82)) #X3
        img.paste(avatar, (4, 163)) #Y1
        img.paste(avatar, (86, 163)) #Y2
        img.paste(avatar, (167, 163)) #Y3
        img.paste(avatar, (4, 245)) #Z1
        img.paste(avatar, (86, 245)) #Z2
        img.paste(avatar, (167, 245)) #Z3
        img.save('img_captcha.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_captcha.png'))

    @commands.command(name="crewmate", aliases = ["crewmates","tripulante","tripulantes"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def crewmate(self, ctx):
        members = []
        for member in ctx.guild.members:
            members.append(member)
        member1 = random.choice(members)
        member2 = random.choice(members)
        member3 = random.choice(members)
        member4 = random.choice(members)
        member5 = random.choice(members)
        member6 = random.choice(members)
        member7 = random.choice(members)
        member8 = random.choice(members)
        member9 = random.choice(members)
        url1 = requests.get(member1.avatar_url)
        url2 = requests.get(member2.avatar_url)
        url3 = requests.get(member3.avatar_url)
        url4 = requests.get(member4.avatar_url)
        url5 = requests.get(member5.avatar_url)
        url6 = requests.get(member6.avatar_url)
        url7 = requests.get(member7.avatar_url)
        url8 = requests.get(member8.avatar_url)
        url9 = requests.get(member9.avatar_url)    
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar1 = Image.open(BytesIO(url1.content))
        avatar1 = avatar1.resize((70,70))
        avatar2 = Image.open(BytesIO(url2.content))
        avatar2 = avatar2.resize((80,80))
        avatar3 = Image.open(BytesIO(url3.content))
        avatar3 = avatar3.resize((90,90))
        avatar4 = Image.open(BytesIO(url4.content))
        avatar4 = avatar4.resize((105,105))
        avatar5 = Image.open(BytesIO(url5.content))
        avatar5 = avatar5.resize((145,145))
        avatar6 = Image.open(BytesIO(url6.content))
        avatar6 = avatar6.resize((105,105))
        avatar7 = Image.open(BytesIO(url7.content))
        avatar7 = avatar7.resize((90,90))
        avatar8 = Image.open(BytesIO(url8.content))
        avatar8 = avatar8.resize((80,80))
        avatar9 = Image.open(BytesIO(url9.content))
        avatar9 = avatar9.resize((70,70))    

        img = Image.open("img_crewmates(1).png")
        img.paste(avatar1, (274, 585)) #Rosa
        img.paste(avatar2, (370, 615)) #Branco
        img.paste(avatar3, (505, 625)) #Azul Escuro
        img.paste(avatar4, (665, 645)) #Marrom
        img.paste(avatar5, (840, 655)) #Preto
        img.paste(avatar6, (1020, 645)) #Vermelho
        img.paste(avatar7, (1200, 625)) #Verde
        img.paste(avatar8, (1340, 618)) #Amarelo
        img.paste(avatar9, (1440, 585)) #Roxo
        img.save('img_crewmates.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_crewmates.png'))

    @commands.command(name="avataredit", aliases = ["editavatar","filteravatar","avatarfilter"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def avataredit(self, ctx, member:discord.Member = None, *, filter = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"Avatar Edit",
        description = f"**🖼️✨|** Aplique diferentes filtros em seu avatar!\n**⚙️| Uso:** `{prefix}avataredit <usuário> <filtro>`\n**💬| Exemplo:** `{prefix}avataredit invert `{ctx.author.mention}",color = 0xff7b00)
        embed.set_thumbnail(url="https://i.imgur.com/A9X6IKH.gif")
        embed.add_field(name = "➖| Invert/Negative", value = "`Inverte as cores`", inline = True)
        embed.add_field(name = "⬛| Gray/Grayscale", value = "`Preto e branco`", inline = True)
        embed.add_field(name = "😶‍🌫️| Blur/Desfocar", value = "`Desfoca o avatar`", inline = True)
        embed.add_field(name = "✏️| Contour/Contornar", value = "`Desenho`", inline = True)
        embed.add_field(name = "⬜| Emboss", value = "`Cinza`", inline = True)
        embed.add_field(name = "🖊️| Find edges/fe", value = "`Contorno escuro`", inline = True)
        embed.add_field(name = "☁️| Smooth/sm", value = "`Suavizar`", inline = True)
        embed.add_field(name = "🌈| Rainbow", value = "`Arco-íris`", inline = True)
        if member == None or filter == None:
            return await ctx.send(embed=embed)
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 5
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        avatar = Image.open(BytesIO(url.content))
        if filter.lower() == "invert" or filter.lower() == "negative":
            avatar_edit = ImageOps.invert(avatar)
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
        elif filter.lower() == "rainbow":
            img = Image.open("img_rainbow.png").resize(avatar.size)
            mask = Image.open('img_rainbow.png').convert('L').resize(avatar.size)
            avatar_edit = Image.composite(img, avatar, mask)
        else:
            await ctx.send(f"**❌| {ctx.author.mention}**, este filtro não existe.")
        avatar_edit.save('img_avatar.png')
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_avatar.png'))

    @commands.command(name="hipocrisia", aliases = ["hipocrita"])
    @cooldown(1,7, type = commands.BucketType.user)
    async def hipocrisia(self, ctx, *, mensagem=None):
        if mensagem == None:
            await ctx.send(f"❌| {ctx.author.mention}, insira um texto.")
            return
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)

        img = Image.open("img_hipocrisia(1).png")
        fonte1 = ImageFont.truetype("font_arial.ttf", 70)
        texto = ImageDraw.Draw(img)
        textao = textwrap.fill(text=mensagem, width=28)
        texto.text(xy=(870,70), text=f"{textao}", fill=(255, 255, 255), font=fonte1)
        img.save('img_hipocrisia.png')
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_hipocrisia.png'))

    @commands.command(name="bbb22")
    @cooldown(1,8, type = commands.BucketType.user)
    async def bbb22(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((140,140))
        img = Image.open("img_bbb22(1).png")
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
        
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 8
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        await ctx.send(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**",file=discord.File('img_bbb22.png'))

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
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = 7
        users[str(ctx.author.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users,f)
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
        await ctx.reply(content = f"**{ctx.author.mention} <:anicoin:919293624850727022>| +{earnings}**", file=discord.File('img_zapmessage.png'))

async def setup(bot):
    print("cog_ps.py loaded")
    await bot.add_cog(cog_ps(bot))