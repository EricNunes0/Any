from genericpath import commonprefix
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import asyncio
import datetime
import random
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

#async def open_account(user):
#    users = await get_bank_data()

#    if str(user.id) in users:
#        return False
#    else:
#        users[str(user.id)] = {}
#        users[str(user.id)]["wallet"] = 0
#        users[str(user.id)]["bank"] = 0

#    with open("mainbank.json","w") as f:
#        json.dump(users, f)
#    return True

#async def get_bank_data():
#    with open("mainbank.json","r") as f:
#        users=json.load(f)

#    return users

#async def update_bank(user, change = 0, mode = "wallet"):
#    users = await get_bank_data()
#    users[str(user.id)][mode] += change 

#    with open("mainbank.json","w") as f:
#        json.dump(users, f)
#    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
#    return bal

class cog_fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fun", aliases = ["diversão","diversao","🤣"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def fun(self, ctx):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『🤣』Diversão [31]",description = f"**`8ball - akumanomi - amogus - angry - attack - baka - bite - bye - cafune - cantada - casar - cheeks - dado - dick - ednaldo - emojify - fake - foto - hack - hug - impostor - jjbattle - kiss - moeda - nitro - punch - raylamm - slap - ship - 🛠️tictactoe - x1`**",color = 0xffbb00)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {command_prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/hEgd2tI.gif")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["8ball","pergunta"])
    @cooldown(1,2, type = commands.BucketType.user)
    async def ball(self, ctx, *, message):
        now = datetime.datetime.now()
        now = now.strftime("%H:%M:%S")
        answers = ["Sim!✔","Não!❌","Provavelmente sim ☑","Provavelmente não ✖","Claro que sim!✅","Claro que não!❎","Acho que sim☑","Acho que não ✖","Minhas fontes dizem que sim ✔","Minhas fontes dizem que não ❌"]
        escolha = random.choice(answers)
        ballEmbed = discord.Embed(color = 0xffbb00)
        ballEmbed.add_field(name = "『❔』Pergunta:", value = f"```{message}```", inline = False)
        ballEmbed.add_field(name = "『🎱』Resposta:", value = f"```{escolha}```", inline = False)
        ballEmbed.set_footer(text=f"• Pedido por {ctx.author} às {now}", icon_url= ctx.author.avatar_url)
        await ctx.send(embed = ballEmbed)

    @ball.error
    async def ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            embed = discord.Embed(title = f"『🎱』{command_prefix}8ball", color = 0xffbb00)
            embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.avatar_url)
            embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Responde qualquer pergunta com 100% de precisão 😎.`", inline = False)
            embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{command_prefix}ball, {command_prefix}pergunta`", inline = False)
            embed.add_field(name = f"『⚙️』Uso:", value = f"`{command_prefix}8ball <pergunta>`", inline = False)
            embed.add_field(name = f"『💬』Exemplos¹ (60 segundos):", value = f"`{command_prefix}8ball Eu vou ganhar na loteria?`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões do usuário:", value = f"`Nenhuma`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões do bot:", value = f"`Ver canais, Enviar mensagens`", inline = False)
            embed.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/2nkTc33.gif")
            await ctx.reply(embed=embed)


    @commands.command(name="akumanomi")
    @cooldown(1,3, type = commands.BucketType.user)
    async def akumanomi(self, ctx):
        num = random.randint(1,20)
        print(1,20)
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #user = ctx.author
        #earnings = 3
        #users[str(user.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        akuma_name = ["Você achou a Gomu Gomu no Mi! 👒",
        "Você achou a Hana Hana no Mi! 🌸",
        "Você achou a Yomi Yomi no Mi! 💀",
        "Você achou a Mera Mera no Mi! 🔥",
        "Você achou a Bara Bara no Mi! 🤡",
        "Você achou a Doru Doru no Mi! 🕯",
        "Você achou a Kage Kage no Mi! 👥",
        "Você achou a Sube Sube no Mi! 🍑",
        "Você achou a Baku Baku no Mi! 😋",
        "Você achou a Ope Ope no Mi! ❤",
        "Você achou a Bomu Bomu no Mi! 💣",
        "Você achou a Ito Ito no Mi! 🦩",
        "Você achou a Kilo Kilo no Mi! ⚖",
        "Você achou a Awa Awa no Mi! 🧼",
        "Você achou a Suna Suna no Mi! 🏜",
        "Você achou a Moku Moku no Mi! 💨",
        "Você achou a Yami Yami no Mi! 🕳",
        "Você achou a Mane Mane no Mi! 🪞",
        "Você achou a Horo Horo no Mi! 👻",
        "Você achou a Gura Gura no Mi! 🌀"]
        
        akuma_desc = ["Esta Akuma no Mi do tipo Paramecia dá ao corpo do usuário as propriedades da borracha, tornando o usuário um Homem-Borracha. Foi comida pelo protagonista de One Piece, Monkey D. Luffy.",
        "Esta Akuma no Mi tipo Paramecia permite que o usuário replique e brote pedaços de seu corpo a partir da superfície de qualquer objeto ou coisa viva. Foi comida por Nico Robin.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário volte à vida depois de morrer. Foi comida por Brook.",
        "Esta Akuma no Mi do tipo Logia permite que o usuário crie, controle e se transforme em fogo à vontade. Ela foi comida por Sabo, e previamente, por Portgas D. Ace.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário seja imune a ataques cortantes e de ser capaz de dividir seu próprio corpo em pedaços e controlar a referida peças da forma que quiser, principalmente levita-los longe do corpo principal do usuário. Foi comida por Buggy, acidentalmente.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário produza cera do seu corpo e molde-a em qualquer forma que quiser. Foi comida por Galdino, mais conhecido por sua alcunha, Mr. 3.",
        "Esta Akuma No Mi do tipo Paramecia permite que o usuário manifeste e controle sombras, como uma forma física tangível. Ela foi comida pelo ex-Shichibukai, Gecko Moria.",
        "Esta Akuma no Mi do tipo Paramecia torna o corpo do usuário escorregadio, que faz com que a maioria dos ataques e todos os objetos escorreguem de seu corpo, protegendo o usuário de danos na maioria das situações. Além disso, se alguém está acima do peso de alguma forma, eles ficarão magros fazendo com que o excesso de gordura *escorregue*. Foi comida por Alvida.",
        "Esta Akuma no Mi do tipo Paramecia dá ao usuário a capacidade de comer qualquer coisa (exceto Kairouseki). Foi comida por Wapol.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário crie um espaço esférico ou *sala*, no qual o usuário tem total controle sobre o posicionamento e orientação dos objetos dentro dele. Foi comida por Trafalgar D. Water Law, que foi alimentado à força por Donquixote Rosinante.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário faça qualquer parte de seu corpo explodir. Foi comido por Gem, mais conhecido por seu pseudônimo de Mr. 5 na Baroque Works.",
        "Esta Akuma no Mi do tipo Paramecia permite que o seu usuário crie e manipule fios extremamente finos ao olho nu. Também permite que o usuário crie fios invisíveis, assim então podendo controlar o corpo da outra pessoa, além de também dar a capacidade de prender seus fios em nuvens, fazendo assim o usuário 'voar'. Foi comida por Donquixote Doflamingo.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário altere seu peso de 1 a 10.000 kg, sem afetar o tamanho geral dos corpos deles. Foi comido por Mikita, mais conhecida por seu codinome Miss Valentine na Baroque Works.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário emita e controle bolhas de sabão e que podem não só limpa a sujeira, mas também pode 'limpar' o poder do adversário. Foi comida por Kalifa.",
        "Esta Akuma no Mi do tipo Logia permite que o usuário crie, controle e se transforme em areia à vontade. Foi comida pelo antigo Shichibukai, Crocodile, também conhecido pelo seu codinome na Baroque Works, de Mr. 0.",
        "Esta Akuma no Mi do tipo Logia permite que o usuário crie, controle e se transforme em fumaça à vontade. Foi comida por Smoker.",
        "Esta Akuma no Mi do tipo Logia permite que o usuário criar e controlar as trevas à vontade. Foi comida por Marshall D. Teach, também conhecido como Barba Negra, que a roubou do Comandante Thatch da 4ª Divisão dos Piratas do Barba Branca depois de matá-lo.",
        "Esta Akuma no Mi do tipo Paramecia permite que o seu usuário copie e se transforme na pessoa que ele tocar com sua mão, ficando exatamente igual a pessoa que foi tocada por ele, não somente com o rosto igual, mas também com o corpo todo.",
        "Esta Akuma no Mi do tipo Paramecia que permite ao usuário produzir e controlar réplicas espectrais como fantasmas que podem vir em diferentes formas. Esses fantasmas são intangíveis o tempo todo eles voam se usa esses fantasmas numa luta produzindo-os e eles passam pela pessoa e as deixam negativas e depressivas fazendo-os ajoelhar-se. Foi comida por Perona.",
        "Esta Akuma no Mi do tipo Paramecia permite que o usuário crie vibrações ou 'tremores'. Foi comida por Edward Newgate, mas após sua morte, seu poder foi roubado por Marshall D. Teach."]
        
        akuma_thumb = ["https://i.pinimg.com/originals/f9/81/a6/f981a656232523154a3b636d15d68a4c.png",
        "https://static.wikia.nocookie.net/onepiece/images/2/21/Hana_Hana_no_Mi_Infobox.png/revision/latest/scale-to-width-down/345?cb=20190619150325&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/3/3b/Yomi_Yomi_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20211002194504&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/2/29/Mera_Mera_no_Mi.png/revision/latest/scale-to-width-down/250?cb=20140409083856&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/9/9c/Bara_Bara_no_Mi_Infobox.png/revision/latest/scale-to-width-down/192?cb=20211005154252&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/3/35/Doru_Doru_no_Mi_Infobox.jpg/revision/latest/scale-to-width-down/177?cb=20200902184120&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/7/7b/Kage_Kage_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20211005154442&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/e/e9/Sube_Sube_no_Mi_Infobox.png/revision/latest/scale-to-width-down/287?cb=20200918015020&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/c/c6/Baku_Baku_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20211005154237&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/0/0e/Ope_Ope_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20211005154646&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/1/1a/Bomu_Bomu_no_Mi_Infobox.png/revision/latest/scale-to-width-down/347?cb=20211005154328&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/6/61/Ito_Ito_no_Mi_Infobox-0.png/revision/latest/scale-to-width-down/250?cb=20160117120846&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/8/89/Kiro_Kiro_no_Mi_Infobox.png/revision/latest?cb=20210204030042",
        "https://static.wikia.nocookie.net/onepiece/images/5/51/Awa_Awa_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20190908000736&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/7/7d/Suna_Suna_no_Mi_Infobox.png/revision/latest/scale-to-width-down/268?cb=20210909232312&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/8/8d/Moku_Moku_no_Mi_Infobox.png/revision/latest/scale-to-width-down/324?cb=20211005154618&path-prefix=pt",
        "https://static.wikia.nocookie.net/onepiece/images/f/f5/Yami_Yami_no_Mi_Infobox.png/revision/latest/scale-to-width-down/350?cb=20181223211520&path-prefix=pt",
        "https://pbs.twimg.com/media/ERVOW0bXkAUpUwp.jpg",
        "http://pm1.narvii.com/6583/986bcdc38b2b8613fd005633af3d1a65e839735d_00.jpg",
        "http://pm1.narvii.com/6699/e357f33d4fbae046311f4303a08356d3442abb90_00.jpg",]

        akumanomi = discord.Embed(
            title = akuma_name[num],
            description = akuma_desc[num],
            color = 0xffbb00
        )
        akumanomi.set_thumbnail(url=akuma_thumb[num])
        akumanomi.set_footer(text = f"Pedido por {ctx.author.name} em {now}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=akumanomi)

    @commands.command(name="amogus", aliases = ["sus","amongus"])
    @cooldown(1,1, type = commands.BucketType.user)
    async def amogus(self, ctx):
        num = random.randint(0,24)
        squares = ["🟥","🟥","🟧","🟨","🟩","🟪","🟫","⬜","⬛","⏹️",":flag_br:",":flag_es:","🇨🇳","🇬🇧", "🇳🇱", "🇦🇲", "🇦🇷", "🇦🇹", "🇦🇽", "🇦🇿", "🇧🇪", "🇨🇦", "🇫🇷", "🇮🇹", "🇯🇵", "🇰🇷"]
        s = squares[num]
        sus = f"➖➖{s}{s}{s}\n➖{s}{s}🟦🟦🟦\n{s}{s}{s}🟦🟦🟦\n{s}{s}{s}🟦🟦🟦\n{s}{s}{s}{s}{s}{s}\n➖{s}{s}{s}{s}{s}\n➖{s}{s}➖{s}{s}\n➖{s}{s}➖{s}{s}"
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #earnings = 1
        #users[str(ctx.author.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        await ctx.send(sus)

    @commands.command(name="angry", aliases = ["raiva"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def angry(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        angry_image = ["https://c.tenor.com/rzDkOlEDun0AAAAC/hayase-nagatoro-nagatoro-angry.gif",
        "https://c.tenor.com/wtSs_VCHYmEAAAAC/noela-angry.gif",
        "https://c.tenor.com/7rIJkf8pB2EAAAAS/a-channel-tooru.gif",
        "https://c.tenor.com/X3x3Y2mp2W8AAAAC/anime-angry.gif",
        "https://c.tenor.com/jgFVzr3YeJwAAAAC/date-a-live-rage.gif",
        "https://c.tenor.com/yCR6JOoxS6wAAAAd/anime-angry.gif",
        "https://c.tenor.com/MifS9QJUGA4AAAAC/anime-angry.gif",
        "https://c.tenor.com/HzZIzXahdw0AAAAC/one-punch-man-saitama.gif",
        "https://c.tenor.com/pI5JTP4Z9w0AAAAd/bungou-stray-dogs-wan-chuuya-nakahara.gif",
        "https://c.tenor.com/2uSb2XPxYNUAAAAC/mad-angry.gif",
        "https://c.tenor.com/VidlGXLXk3gAAAAC/anime-girl.gif",
        "https://c.tenor.com/3tjdeVFZR6oAAAAC/anime-pout.gif",
        "https://c.tenor.com/fovBuonF-dIAAAAC/aikatsu-aikatsu-stars.gif",
        "https://c.tenor.com/ikKAd57zDEwAAAAd/anime-mad.gif",
        "https://c.tenor.com/G_YeALOH-iAAAAAC/mao-amatsuka-mad.gif",
        "https://c.tenor.com/Ma3PyQWx5L4AAAAC/kamisama-kiss.gif",
        "https://c.tenor.com/MLsVzlSceaEAAAAC/anime-angry.gif",
        "https://c.tenor.com/m7GE0heNsPYAAAAC/anime-scary.gif",
        "https://c.tenor.com/9JUYPgGXEtgAAAAC/anime-angly.gif",
        "https://c.tenor.com/zvtbPoUvH1sAAAAC/shy-anime.gif",
        "https://c.tenor.com/b76QnX1XVAcAAAAC/raiva-anime.gif",
        "https://c.tenor.com/XDSBlROZTh8AAAAd/my-hero-academia-mha.gif",
        "https://c.tenor.com/K8jGB-xcdnoAAAAC/cringe-anime.gif",
        "https://c.tenor.com/yNWlcWKPsbkAAAAC/assassination-classroom-asano.gif",
        "https://c.tenor.com/oxqylurVQmkAAAAC/touken-angry.gif",
        "https://c.tenor.com/DJk8RI8ZLvQAAAAC/angry-mad.gif",
        "https://c.tenor.com/RtQzS1HCLvYAAAAC/taiga-toradora.gif",
        "https://c.tenor.com/2YmFNn9rx1EAAAAC/bakugo-angry-cake.gif",
        "https://c.tenor.com/VlG3XYw4d0EAAAAd/hayase-nagatoro-nagatoro-angry.gif",
        "https://c.tenor.com/4a4d9b6kbKEAAAAC/angry-anime-angry.gif",
        "https://c.tenor.com/JCFncEzU3YEAAAAd/mio-mio-akiyama.gif",
        "https://c.tenor.com/7dWlqDyO8wYAAAAC/anime-angry.gif",
        "https://c.tenor.com/D_Untm0RiksAAAAC/dia-love.gif",
        "https://c.tenor.com/LeZ-bqFn0rkAAAAC/angry-toradora.gif"
        ]
        angry = random.choice(angry_image)

        angry_image = discord.Embed(
            description = f"**😡| {ctx.author.mention} ficou com raiva <a:ab_Triggered:932381700464472084>**",
            color = 0xffbb00,
        )
        angry_image.set_image(url=angry)
        angry_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=angry_image)

    @commands.command(name="attack", aliases = ["atacar"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def attack(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        attack_image = ["https://i.gifer.com/IS5z.gif", #Bulbasaur
        "https://pa1.narvii.com/6204/46f937cd1ecbc2a3c75a40736a043e3dc672756d_hq.gif", #Venusaur
        "https://i.gifer.com/embedded/download/L6tF.gif", #Charmander
        "https://64.media.tumblr.com/93554bfb2c410367390c1910116e760f/tumblr_ntdxcjgnus1rd4ymxo2_500.gifv", #Charmeleon
        "http://pa1.narvii.com/5903/7ade1898e9c95e33f9948abc8de367b1290c6c79_00.gif", #Charizard
        "https://c.tenor.com/hkiaCdqDtDoAAAAd/mega-charizard-x-powerful-anime-attack.gif", #Charizard X
        "https://c.tenor.com/Occh8IGPz5wAAAAC/charizard-mega-charizard-y.gif", #Charizard Y
        "https://c.tenor.com/wHOXd5twXI4AAAAC/squirtle-attack.gif", #Squirtle
        "https://i.pinimg.com/originals/5d/9b/0a/5d9b0a15fc82456243690e98557dc01a.gif", #Blastoise
        "http://i.imgur.com/DJZje2D.gif", #Mega Blastoise
        "https://pa1.narvii.com/6470/36a88cc095b341ed5aa0b0df1c88f32d993b4516_hq.gif", #Caterpie
        "https://68.media.tumblr.com/7e0e3ef3289c990be34e6bcfa20cf050/tumblr_mu3v3csaxe1s035gko2_500.gif", #Metapod
        "https://thumbs.gfycat.com/AnotherSentimentalGrayfox-max-1mb.gif", #Butterfree
        "https://4.bp.blogspot.com/-YXDs2ixwwgY/VTu_mzGB8oI/AAAAAAAAV34/aUBxuwL0gm4/s1600/Weedle_Poison_Sting_GIF.gif", #Weedle
        "https://c.tenor.com/FxPEBbuPLn8AAAAC/beedrill-pokemon.gif", #Beedrill
        "https://pa1.narvii.com/6709/cd5657eeaeb5894722e0c81db1e9e16e1f4f4a63_hq.gif", #Mega Beedrill
        ]
        attack = random.choice(attack_image)
        if member == None:
            attack_text = ""
        elif member.id == ctx.author.id:
            attack_text = f"**🥊| {ctx.author.mention} atacou a si mesmo**"
        else:
            attack_text = f"**🥊| {ctx.author.mention} atacou {member.mention}**"

        attack_image = discord.Embed(
            description = attack_text,
            color = 0xffbb00,
        )
        attack_image.set_image(url=attack)
        attack_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=attack_image)

    @commands.command(name="baka")
    @cooldown(1,3, type = commands.BucketType.user)
    async def baka(self, ctx, *, member: discord.Member = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if member == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, mencione um usuário.\n⁉| Para mais informações sobre o comando, digite `{command_prefix}help baka`")
            return
        url_image = ["https://c.tenor.com/OyIYV1OjcjQAAAAM/anime-fiduka.gif",
        "https://c.tenor.com/REgUMZiMpf8AAAAC/anime-baka.gif",
        "https://pa1.narvii.com/7652/da2c3ab7a45c550b755206a3188c02a6a11126e3r1-498-278_hq.gif",
        "https://c.tenor.com/UsggMuRixo0AAAAC/baka-anime.gif",
        "https://c.tenor.com/GffsABES8JIAAAAC/baka-anime.gif",
        "https://c.tenor.com/FLw8YNNPRYIAAAAC/baka-anime.gif",
        "https://c.tenor.com/G4zCaHnNxysAAAAC/anime-boy-baka-baka.gif",
        "https://c.tenor.com/axEcqUnz5MkAAAAC/baka-anime.gif",
        "https://c.tenor.com/ty1WwFxMUc8AAAAC/anime-boy-baka-anime.gif",
        "https://c.tenor.com/smRK3hdF5DMAAAAC/baka-anime.gif",
        "https://c.tenor.com/ILl8K-ur6iEAAAAC/baka-anime.gif",
        "https://c.tenor.com/CHK-jryUa6sAAAAC/kakegurui.gif",
        "https://c.tenor.com/TZju-aIuUmAAAAAC/baka-anime.gif",
        "https://c.tenor.com/b8sy7WBrJA8AAAAd/baka-tsundere.gif",
        ]
        url_imagem = random.choice(url_image)
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #user = ctx.author
        #earnings = 5
        #users[str(user.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        embed_image = discord.Embed(
            description = f"{ctx.author.mention} chamou o {member.mention} de baka!",
            color = 0xffbb00,
        )
        embed_image.set_image(url=url_imagem)
        embed_image.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_image)

    @commands.command(name="bater", aliases = ["punch"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def on_member(self, ctx, *, member: discord.Member = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if member == None:
            await ctx.send(f"❌| Por favor {ctx.author.mention}, mencione um usuário.\n⁉| Para mais informações sobre o comando, digite `{command_prefix}help bater`")
            return
        url_image = ["https://pa1.narvii.com/6457/ef21d3fe6324b364aa23f0d398aec3190dda0b6a_hq.gif",
        "https://pa1.narvii.com/6317/dea3687e9b3869453fc5742ccc085286c56dfae3_hq.gif",
        "https://thumbs.gfycat.com/ShadowyFoolhardyEyas-max-1mb.gif",
        "https://i.pinimg.com/originals/8a/ab/09/8aab09880ff9226b1c73ee4c2ddec883.gif",
        "https://s.aficionados.com.br/imagens/giphy-3-5.gif",
        "https://static.wikia.nocookie.net/narutofanon/images/a/aa/Punho_Megatonico.gif/revision/latest?cb=20180918144926&path-prefix=pt-br",
        "https://pa1.narvii.com/6631/d7a2d51aac954f010d2357552b3f2f55edc1db9d_hq.gif",
        "http://3.bp.blogspot.com/-2NWjo2FOaMU/VLWogQPv7cI/AAAAAAAAAoo/hfeKFJOCOW0/s1600/barakamongif.gif",
        "https://pa1.narvii.com/6516/7de68a2c456f26361a598f31fa8e2cfceeb5927b_hq.gif",
        "https://2img.net/h/1.bp.blogspot.com/-vNF44W4EoVU/T55vi-SH0yI/AAAAAAAAAhI/TUL4cvV_WCw/s1600/tumblr_m34kd8kLCK1r5tmleo2_500.gif",
        "https://sm.ign.com/ign_br/screenshot/default/tsunade-vs-orochimaru_xftf.gif",
        "https://pa1.narvii.com/6710/0d7f0d555493888fc03d410306678953305fece5_hq.gif",
        "https://c.tenor.com/P4HQFHaju04AAAAC/muda-muda-giorno-giovanna.gif"
        ]
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #user = ctx.author
        #earnings = 5
        #users[str(user.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        url_imagem = random.choice(url_image)
        embed_image = discord.Embed(
            description = f"{ctx.author.mention} bateu em {member.mention}!",
            color = 0xffbb00,
        )
        embed_image.set_image(url=url_imagem)
        embed_image.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_image)

    @commands.command(name="beijar", aliases = ["kiss"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def beijar(self, ctx, *, member: discord.Member = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if member == None:
            return await ctx.send(f"❌| Por favor {ctx.author.mention}, mencione um usuário.\n⁉| Para mais informações sobre o comando, digite `{command_prefix}help beijar`")
        url_image = ["https://i.imgur.com/Rtu2JyU.gif",
        "https://i.pinimg.com/originals/02/e7/8c/02e78c4b46d02a713e4d5054252a2c28.gif",
        "https://acegif.com/wp-content/uploads/anime-kissin-2.gif",
        "http://67.media.tumblr.com/756c52d84caf10e177777d6ee8504581/tumblr_ngyt1mvACH1qg78wpo1_500.gif",
        "https://capricho.abril.com.br/wp-content/uploads/2017/04/bv8.gif",
        "https://i.imgur.com/iz1awkG.gif",
        "https://img.wattpad.com/7a65c6bc07fb4c2c3091e27f0e9c9221391d3362/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f67715a614f672d73396d497046413d3d2d3638312e313565333662326466396264383836353835353633313739353330342e676966",
        "https://www.intoxianime.com/wp-content/uploads/2017/02/KuzunoHonkai-Episode5-Omake-3.gif",
        "https://i.imgur.com/ma3wNn3.gif",
        "https://utinuti.files.wordpress.com/2017/04/kuzunohonkai-episode9-omake-7.gif",
        "https://i.imgur.com/GhGvzuv.gif",
        "https://pa1.narvii.com/6407/a86e88ebb9eba428de6981e6bab6b9ac4579d9be_hq.gif",
        "https://aniyuki.com/wp-content/uploads/2021/07/aniyuki-anime-gif-kiss-49.gif",
        "https://ptanime.com/wp-content/uploads/2017/07/Koi-to-uso-GIF3.gif",
        "https://ptanime.com/wp-content/uploads/2017/07/Koi-to-uso-GIF3.gif",
        "https://64.media.tumblr.com/a86ac3d87c03c844898eedf841fc04f5/tumblr_pe123uhFl21ut7rfeo1_500.gifv",
        ]
        url_imagem = random.choice(url_image)
        embed_image = discord.Embed(
            description = f"{ctx.author.mention} beijou {member.mention}. 😘",
            color = 0xffbb00,
        )
        embed_image.set_image(url=url_imagem)
        embed_image.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=member.avatar_url)
        await ctx.send(embed=embed_image)

    @commands.command(name="bite", aliases = ["morder","mordida"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def bite(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        bite_image = ["https://i.gifer.com/5Hj4.gif",
        "https://c.tenor.com/nkNsOraAx4AAAAAC/anime-bite.gif",
        "https://c.tenor.com/4j3hMz-dUz0AAAAC/anime-love.gif",
        "https://c.tenor.com/n0DPyBDtZHgAAAAC/anime-bite.gif",
        "https://c.tenor.com/1LtA9dSoAIQAAAAC/zero-no-tsukaima-bite.gif",
        "https://c.tenor.com/TX6YHUnHJk4AAAAC/mao-amatsuka-gj-bu.gif",
        "https://c.tenor.com/DrLl1pH034gAAAAM/gamerchick42092-anime.gif",
        "https://c.tenor.com/aKzAQ_cFsFEAAAAC/arms-bite.gif",
        "https://c.tenor.com/IKDf1NMrzsIAAAAC/anime-acchi-kocchi.gif",
        "https://c.tenor.com/Xpv7HTk-DIYAAAAC/mad-angry.gif",
        "https://c.tenor.com/xHeSSmvJvQQAAAAC/vampire-kiss.gif",
        "https://c.tenor.com/5FOgNEcoaYMAAAAS/neck-kisses.gif",
        "https://c.tenor.com/hwCVSWyji0QAAAAC/anime-bite.gif",
        "https://c.tenor.com/8UjO54apiUIAAAAS/gjbu-bite.gif",
        "https://c.tenor.com/aXcm33Ky8qsAAAAC/diabolik-anime.gif",
        "https://c.tenor.com/TwP8Vv8acSkAAAAC/the-melancholy-of-haruhi-suzumiya-biting-ear.gif",
        "https://c.tenor.com/0uRmrUvyZFEAAAAC/vamp-vampire-bite.gif",
        "https://c.tenor.com/1egHkU3e_8cAAAAC/girl-bite.gif",
        "https://c.tenor.com/eQYan9dHVIkAAAAC/chuuu.gif",
        "https://c.tenor.com/0yrpvnpqSG0AAAAC/anime-bite.gif",
        "https://c.tenor.com/HO71nB7fQdkAAAAC/anime-zombielandsaga.gif",
        "https://c.tenor.com/3lz4gjb3q-QAAAAC/moka-bite.gif",
        "https://c.tenor.com/RlbZRirdg3UAAAAC/yui-komori-subaru-sakamaki.gif",
        "https://c.tenor.com/V8D96KuAOtsAAAAd/last-period-anime.gif",
        "https://c.tenor.com/6HhJw-4zmQUAAAAC/anime-bite.gif",
        "https://c.tenor.com/iIAvibfzzFYAAAAC/demichan-wa-kataritai-nom-nom.gif",
        "https://c.tenor.com/ld5vyQrrGXUAAAAC/black-butler-sebastian.gif",
        "https://c.tenor.com/H2bi31hpZnYAAAAC/re-zero-rem.gif",
        "https://c.tenor.com/pZdhFntvwGYAAAAC/bite-finger.gif",
        "https://c.tenor.com/Nk-Eq8_ZiNwAAAAC/index-toaru.gif",
        "https://c.tenor.com/3iWdmGbvMFQAAAAC/anime-finger.gif",
        "https://c.tenor.com/4bMy2Yj3lG8AAAAd/nom3-bite-finger.gif",
        ]
        bite = random.choice(bite_image)
        if member == None:
            bite_image = discord.Embed(
                color = 0xffbb00,
            )
            bite_image.set_image(url=bite)
            bite_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=bite_image)
        else:
            bite_image = discord.Embed(
                description = f"🧛| {ctx.author.mention} mordeu {member.mention}",
                color = 0xffbb00,
            )
            bite_image.set_image(url=bite)
            bite_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=bite_image)

    @commands.command(name="bye", aliases = ["tchau"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def bye(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        bye_image = ["https://c.tenor.com/Rf5v6glMta8AAAAC/hey-waves.gif",
        "https://c.tenor.com/EJ1C6RDW3YoAAAAC/kakashi-bye-bye-anime.gif",
        "https://c.tenor.com/ktle_yw1QxEAAAAC/bye-finger-gun.gif",
        "https://c.tenor.com/mxmuYq0f6YcAAAAC/bye-bye-senpai-anime-smile.gif",
        "https://c.tenor.com/4Knme9s_ErkAAAAC/pokemon-pokemon-evolutions.gif",
        "https://c.tenor.com/i2THl25f1xUAAAAC/anime-bye-bye-ranpo-edogawa.gif",
        "https://c.tenor.com/_Exw4V_izbkAAAAC/cute-anime.gif",
        "https://c.tenor.com/thNxDWlG1EcAAAAd/killua-zoldyck-anime.gif",
        "https://c.tenor.com/9wzq3wK8NwcAAAAC/sawako-kuronuma-sawako.gif",
        "https://c.tenor.com/DLbH0i7N7yIAAAAd/bay-anime-bye-anime.gif",
        "https://c.tenor.com/qRFgrVQGgYMAAAAC/misha-uchinomaidgauzasugiru.gif",
        "https://c.tenor.com/q80PMcmrxDwAAAAd/anime-girl.gif",
        "https://c.tenor.com/sPgkxwu-MRsAAAAC/anime-tokyo-revengers.gif",
        "https://c.tenor.com/4B3gwE0AJEAAAAAC/mine-anime.gif",
        "https://c.tenor.com/ESVgd3T5YlcAAAAC/demon-slayer-anime.gif",
        "https://c.tenor.com/Tz8QeOZ-PekAAAAC/anime-animu.gif",
        "https://c.tenor.com/rza_O7Gdk9UAAAAC/anime-bye.gif",
        "https://c.tenor.com/CGZ8m0xZA2cAAAAC/sumi-sakurasawa-bye-bye.gif",
        "https://c.tenor.com/PH78_m9Mh4UAAAAC/anime-bye-bye.gif",
        "https://c.tenor.com/z1Bv922uTCUAAAAC/astolfo-anime.gif",
        "https://c.tenor.com/waDeKL3N3EwAAAAd/anime-anime-love.gif",
        "https://c.tenor.com/e48wByvWU-IAAAAC/anime-hi.gif",
        "https://c.tenor.com/rWN4ZHFLknoAAAAC/bye-hi.gif",
        "https://c.tenor.com/A3aDS-kmv68AAAAC/nai-hi.gif",
        "https://c.tenor.com/mE4zHyX0BHgAAAAC/tohru-bye.gif",
        "https://c.tenor.com/r97dqFJ-2j0AAAAC/bye-bye-angrygirls.gif",
        "https://c.tenor.com/soSgZnaEuSUAAAAC/ate-um-outro-dia-naruto.gif",
        ]
        bye = random.choice(bye_image)
        if member == None:
            bye_msg = f"👋| {ctx.author.mention} deu um tchau."
        else:
            bye_msg = f"👋| {ctx.author.mention} deu um tchau para {member.mention}"
        
        bye_image = discord.Embed(
            description = bye_msg,
            color = 0xffbb00,
        )
        bye_image.set_image(url=bye)
        bye_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=bye_image)

    @commands.command(name="cafune", aliases = ["pat"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def cafune(self, ctx, *, member: discord.Member = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if member == None:
            await ctx.send(f"❌| Por favor {ctx.author.mention}, mencione um usuário.\n⁉| Para mais informações sobre o comando, digite `{command_prefix}help cafune`")
            return
        url_image = ["https://images-ext-2.discordapp.net/external/Cb7mlYet51c8t5iGzi-Jkqzt1cKax6eRo23Tffr92EI/https/cdn.nekos.life/pat/pat_068.gif",
        "https://images-ext-2.discordapp.net/external/p0CFRRlbWeVBxqO-LKd8f1z0MuftV9CVEngViadX7OI/https/cdn.nekos.life/pat/pat_023.gif",
        "https://images-ext-1.discordapp.net/external/GwGUWdwUSowPt5cDxb-6YtH6yi9cEn13YM3YVdyT4nA/https/cdn.nekos.life/pat/pat_002.gif",
        "https://images-ext-2.discordapp.net/external/pdnVFaSxM0kyBLkAlbI145aaEUUi-tInbWVvh_2PnXw/https/cdn.nekos.life/pat/pat_063.gif",
        "https://images-ext-1.discordapp.net/external/5gTEJjgFQmEsfinxmX8eyo8-fiCOW7e-DA_J9KNxh5Q/https/cdn.nekos.life/pat/pat_015.gif",
        "https://images-ext-2.discordapp.net/external/n3ncxR4xV_gSq3BkAba3RazL95C9EMjTBbg3tqEL4M8/https/cdn.nekos.life/pat/pat_074.gif",
        "https://images-ext-1.discordapp.net/external/LtCBxGiwGXqwIleKSzoOm0h8-758kSAeLM8A3r0Td1U/https/cdn.nekos.life/pat/pat_056.gif?width=836&height=473",
        "https://images-ext-1.discordapp.net/external/CSgEBCycJTISxIwGbZa3u6FTGFiul_nRj7VZZQlnRY4/https/cdn.nekos.life/pat/pat_057.gif?width=473&height=473",
        "https://images-ext-1.discordapp.net/external/mxR1yC5_1iwzBRiCxo8yQWlrCLnS8cOF-kkhFwkXGf0/https/cdn.nekos.life/pat/pat_069.gif",
        "https://images-ext-2.discordapp.net/external/HHTNXMLtQIFrHbOm5Fbl8MrIsrCt5UW9LItgnn3w0ME/https/cdn.nekos.life/pat/pat_064.gif",
        "https://images-ext-2.discordapp.net/external/AhO1MV_LCl3ntEGsvpsgPcy8EjOqJoUKimWR3d0zGZk/https/cdn.nekos.life/pat/pat_022.gif",
        "https://images-ext-2.discordapp.net/external/c28lf8X1fDPKrPXGyUgEOqvj65LQ8uSmWk0DLQaDDUA/https/cdn.nekos.life/pat/pat_029.gif",
        "https://images-ext-1.discordapp.net/external/Bnrrn6H2D0NrfaoRK_Er0_nAx9DUT0NJH8G24O2vESo/https/cdn.nekos.life/pat/pat_067.gif?width=572&height=473",
        "https://images-ext-2.discordapp.net/external/vtf1HJ2uA5H2s1ItrDdjj4z-l7hNyr0UT0HxZZ3QJ4w/https/cdn.nekos.life/pat/pat_041.gif"
        ]
        url_imagem = random.choice(url_image)
        embed_image = discord.Embed(
            description = f"{ctx.author.mention} fez um cafuné em {member.mention}! 🤗",
            color = 0xffbb00,
        )
        embed_image.set_image(url=url_imagem)
        embed_image.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_image)

    @commands.command(name="cantada")
    @cooldown(1,3, type = commands.BucketType.user)
    async def cantada(self, ctx):
        cantadas = ["Usei shampoo anti-quedas, mas continuo caindo de amores por você.",
        "Você é um eixo terrestre? Porque meu mundo gira em torno de você!",
        "Vontade de fazer aquilo que começa com s: ser o amor da sua vida.",
        "Em cima da colina passa boi passa boiada, só saio da sua frente quando for minha namorada.",
        "Você não é Death Note, mas me matou quando me escreveu pela primeira vez.",
        "Ontem eu queria te beijar. Hoje estou igual ontem.",
        "Se preto fosse paixão e branco fosse carinho, o que eu sinto por você seria xadrezinho.",
        "Sabe o que combina com você? Eu!",
        "Não te doem as pernas de fugir dos meus sonhos todas as noites, meu amor?",
        "Gata, me chama de tabela periódica e diz que rola uma química entre nós!",
        "Você não é pescoço mas mexeu com a minha cabeça!",
        "As rosas são vermelhas, violetas são azuis, eu não posso rimar, mas posso namorar você?",
        "Queria te desejar noite, porque se fosse boa, estaríamos juntos.",
        "Você sabe qual é o motivo do meu sorriso todos os dias? A primeira palavra dessa frase...",
        "Já imaginei como seria a nossa vida juntos muitas vezes, mas tenho certeza de que nem o mais louco dos sonhos iria se comparar com a realidade de ter você ao meu lado!",
        "Vou te dar um beijo, se você não gostar me devolve.",
        "Especial é você, que me faz sorrir nos piores momentos.",
        "O crime só compensa se for pra roubar uns beijos seu!",
        "Se você acredita em salvação, teria como você me salvar da solidão?",
        "Estou fazendo uma campanha de doação de órgãos... Então, não quer doar o seu coração pra mim?",
        "Se beleza fosse flor, você seria o Jardim Botânico!",
        "Não sou carro, mas sou Para ti. (Sim, existe um modelo de carro Parati)",
        "Queria desejar noite, porque para ser boa teríamos que estar juntos.",
        "Em 2022 eu estava apaixonado(a) por você. E parece que estamos em 2022...",
        "Está calor, né? Mas não é de hoje que eu me derreto por você.",
        "Pesquisas apontam que *agente* junto é erro de gramática, mas a gente separado é erro do destino.",
        "Meu nome é Arnaldo, mas pode me chamar de Naldo, porque perdi o ar quando vi você."
        ]
        cantada = random.choice(cantadas)
        await ctx.send(f"{cantada}\n**<:anicoin:919293624850727022>|**")

    @commands.command(name="cheeks", aliases = ["cheek","bochecha"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def cheeks(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        cheek_image = ["https://c.tenor.com/X7V66nTiHBkAAAAd/cheek-pinch.gif",
        "https://c.tenor.com/iDK70enVnTcAAAAC/anime-cute.gif",
        "https://c.tenor.com/4Cv8fAL-lSsAAAAS/cute-anime.gif",
        "https://c.tenor.com/1H1CJrhwbFcAAAAd/pinch-cheeks-anime.gif",
        "https://c.tenor.com/6JuQubTkqxoAAAAC/gakuenhd-cute-anime-baby.gif",
        "https://c.tenor.com/8iKS9O-KD8IAAAAC/mitsudomoe-pinch.gif",
        "https://c.tenor.com/PJ6hr1z49EsAAAAC/noucome-chocolat.gif",
        "https://c.tenor.com/G0GWkGCYw8EAAAAC/anime-cheek.gif",
        "https://c.tenor.com/iEXZT4FlC0EAAAAC/koisuru-asteroid-asteroid-in-love.gif",
        "https://c.tenor.com/C7Rsuk3cIV8AAAAC/anime-cheeks.gif",
        "https://c.tenor.com/38mAGJcM7osAAAAC/mai-sakurajima-rascal-does-not-dream-of-bunny-girl-senpai.gif",
        "https://c.tenor.com/4j3hMz-dUz0AAAAC/anime-love.gif",
        "https://c.tenor.com/2rwxALHum7wAAAAC/pulls-cheek-youre-so-cute.gif",
        "https://c.tenor.com/EMQB9n_G4-4AAAAC/funny-face-face.gif",
        "https://c.tenor.com/cEZZ8LBsNVcAAAAC/saikava-dragon.gif",
        "https://c.tenor.com/bEcGFSFfFJcAAAAd/rokka-asahi-lock.gif",
        "https://c.tenor.com/ISN_bpY007QAAAAC/cute-pinch-cheek.gif",
        "https://c.tenor.com/bCVdsJcmkbkAAAAC/neko-cat-girl.gif",
        "https://c.tenor.com/XkzzeHVgdYUAAAAC/pinchcheek-shounen-maid.gif",
        "https://c.tenor.com/pJU4JShWnz8AAAAC/konosuba-aqua.gif",
        ]
        cheek = random.choice(cheek_image)
        if member == None:
            return await ctx.send(f"❌| {ctx.author.mention}, mencione um usuário.")
        elif member == bot.user:
            cheek_msg = f"☺️| Ei {ctx.author.mention}, não faça isso comigo."
        else:
            cheek_msg = f"☺️| {ctx.author.mention} mexeu nas bochechas do {member.mention}"
        
        cheek_image = discord.Embed(
            description = cheek_msg,
            color = 0xffbb00,
        )
        cheek_image.set_image(url=cheek)
        cheek_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=cheek_image)

    @commands.command(name="dado")
    @cooldown(1,2, type = commands.BucketType.user)
    async def dado(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        dados = ["**1**! <:dado_1:905214553787338762>","**2**! <:dado_2:905214571256635412>","**3**! <:dado_3:905214660985376838>","**4**! <:dado_4:905214683005476924>","**5**! <:dado_5:905214716731859035>","**6**! <:dado_6:905214733030932481>"]
        dado = random.choice(dados)
        embed = discord.Embed(
            description = f"{ctx.author.mention} rolou 1 dado, e conseguiu {dado}",
            color = 0xffbb00,
        )
        embed.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="dado2")
    @cooldown(1,2, type = commands.BucketType.user)
    async def dado2(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        num = [0,1,2,3,4,5]
        dados_rand = ["<:dado_1:905214553787338762>","<:dado_2:905214571256635412>","<:dado_3:905214660985376838>","<:dado_4:905214683005476924>","<:dado_5:905214716731859035>","<:dado_6:905214733030932481>"]
        num1 = random.choice(num)
        num2 = random.choice(num)
        dado1 = dados_rand[num1]
        dado2 = dados_rand[num2]
        num_soma = (num1 + 1) + (num2 + 1)
        embed = discord.Embed(
            description = f"{ctx.author.mention} rolou 2 dados, e conseguiu **{num_soma}**! {dado1}{dado2}",
            color = 0xffbb00,
        )
        embed.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="dick")
    @cooldown(1,2, type = commands.BucketType.user)
    async def dick(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        tamanho = random.randint(1,26)
        embed = discord.Embed(
            title = f"{ctx.author.name}, você tem {tamanho} centímetros",
            description = "O que importa é saber como usar...",
            color = 0xffbb00,
        )

        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-11/512px/1f423.png")
        embed.set_footer(text="Pedido por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="hack", pass_context = True)
    @cooldown(1,1, type = commands.BucketType.user)
    async def hack(self, ctx, member: discord.Member = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        if member == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, mencione um usuário.\n**⁉|** Para mais informações sobre o comando, digite `{command_prefix}help hack`")
            return
        msgs = ["Boku no pico é mt bom","O Anibot é muito brabo","Quer namorar cmg?","Quanto é o pack do pé?"]
        words = ["cavalo","pinto","gf","hentai","gay","delícia","webnamorar","gado","sarrada","linda","boi","amor","webnamoro","Claudia","Julia","Ana","Bea","Luana","Laura","Samanta","Larissa","Leticia","Giovanna","Manuela","mentira","ah é","jojo","jojofag","otaku","fedido","meme"]
        dms = ["toma fazer gf cmg?","obg pela skin no lol, te amo","Meu pack do pé é 10 reais, n posso fazer mais barato","Não adianta insistir, não vou ver boku no pico","me doa robux ae","Nossa lobo mau 😳"]
        search = ["Peido tem peso? Pq se não eu me caguei","Mulher hentai gifs","Como aumentar o meu tamanho?","Pq o Anibot é o melhor bot de todos?"]
        emails = ["gmail","hotmail","outlook","yahoo","live"]
        lastMsg = random.choice(msgs)
        mostWords = random.choice(words)
        lastDM = random.choice(dms)
        lastSearch = random.choice(search)
        email = random.choice(emails)
        msg = await ctx.send(f"『<a:ab_carregando:911073196038582272>』 Iniciando o hack...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Procurando email e senha da conta.")
        await asyncio.sleep(1)
        await msg.edit(content=f"『<a:ab_carregando:911073196038582272>』 Email e senha obtidos:\nEmail: `{member.name}@{email}.com`\nSenha: `********`")
        await asyncio.sleep(1.5)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Analisando as mensagens...")
        await asyncio.sleep(1)
        await msg.edit(content=f"『<a:ab_carregando:911073196038582272>』 Última mensagem enviada: `{lastMsg}`")
        await asyncio.sleep(1)
        await msg.edit(content=f"『<a:ab_carregando:911073196038582272>』 Palavra mais usada: `{mostWords}`")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Verificando lista de amigos (se ainda tiver algum)...")
        await asyncio.sleep(1)
        await msg.edit(content=f"『<a:ab_carregando:911073196038582272>』 Última DM recebida: `{lastDM}`")
        await asyncio.sleep(1.5)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Encontrando IP...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 IP encontrado: `192.120.1.6.16`")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Injetando trojan...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Emojis roubados <:DekuPaint:821159400626454539>")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Instalando Baidu antivírus... 🛡")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Baidu instalado com sucesso! ⏬")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Analisando histórico do navegador...")
        await asyncio.sleep(1)
        await msg.edit(content=f"『<a:ab_carregando:911073196038582272>』 Última pesquisa: `{lastSearch}`")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Roubando fotos da galeria...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Compartilhando fotos...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Roubando cartão de crédito...")
        await asyncio.sleep(1)
        await msg.edit(content="『<a:ab_carregando:911073196038582272>』 Dados vendidos para o governo!")
        await asyncio.sleep(1)
        await msg.edit(content=f"『✅』 {member.name} foi hackeado com sucesso!")

    @commands.command(name="hug", aliases = ["abraçar","abraço"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        attack_image = ["http://33.media.tumblr.com/680b69563aceba3df48b4483d007bce3/tumblr_mxre7hEX4h1sc1kfto1_500.gif",
        "https://i.gifer.com/origin/b8/b814b05e2e14df35cd80a3cfb7aeece4.gif",
        "https://i.gifer.com/8VnY.gif",
        "https://i.gifer.com/27tM.gif",
        "https://i.gifer.com/Zi8A.gif",
        "https://i.gifer.com/3a9O.gif",
        "https://i.gifer.com/5ngg.gif",
        "https://i.gifer.com/B7bp.gif",
        "https://i.gifer.com/YW.gif",
        "https://i.gifer.com/ZRLJ.gif",
        "https://i.gifer.com/OPY.gif",
        "https://i.gifer.com/83y9.gif",
        "https://i.gifer.com/8X6d.gif",
        "https://i.gifer.com/79oD.gif",
        "https://i.gifer.com/Bvr.gif",
        "https://i.gifer.com/Txh9.gif",
        "https://i.gifer.com/F1s1.gif",
        "https://i.gifer.com/Wjrj.gif",
        "https://i.gifer.com/Y4Pm.gif",
        "https://i.gifer.com/9jXo.gif",
        "https://i.gifer.com/3XEo.gif",
        "https://i.gifer.com/5ZHH.gif",
        "https://i.gifer.com/Yp9v.gif",
        "https://i.gifer.com/79o1.gif",
        "https://i.gifer.com/AX2b.gif",
        "https://i.gifer.com/ZMzD.gif",
        ]
        attack = random.choice(attack_image)
        if member == None:
            attack_image = discord.Embed(
                color = 0xffbb00,
            )
            attack_image.set_image(url=attack)
            attack_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=attack_image)
        else:
            attack_image = discord.Embed(
                description = f"🫂| {ctx.author.mention} abraçou {member.mention}",
                color = 0xffbb00,
            )
            attack_image.set_image(url=attack)
            attack_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=attack_image)

    @commands.command(name="impostor")
    @cooldown(1,2, type = commands.BucketType.user)
    async def impostor(self, ctx):
        members = []
        for member in ctx.guild.members:
            members.append(member)
        members = random.choice(members)
        amogus = ["<a:RedSus:927767875127746622>","<a:OrangeSus:927767953397669918>","<a:GreenSus:927768004383625236>","<a:BlueSus:927768065268142152>","<a:WhiteSus:927768123627696148>","<a:BlackSus:927768188765233163>"]
        sus = random.choice(amogus)
        impostor = await ctx.send(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 。　　　　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 Impostor restante 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　{sus}　 。　　　　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 Impostor restante 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 {sus}。　　　　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 Impostor restante 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 。{sus}　　　　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 impostor restante... 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 。　{sus}　　　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 impostor restante... 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 。　　　{sus}　　  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 impostor restante... 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)
        asyncio.sleep(0.8)
        await impostor.edit(f"""
        . 　　　。　　　　•　 　ﾟ　　。 　　.
        .　　　 　　.　　　　　。　　 。　.
        .　　 。　　　　　{sus}  。 . 　　 • 　　　　•
        ﾟ　　 {members} é o impostor!.　 。　.
        '　　　 1 impostor restante... 　 　　。
        ﾟ　　　.　　　. ,　　　　.　 .
        """)  

    @commands.command(name="moeda", aliases=["coin"])
    @cooldown(1,2, type = commands.BucketType.user)
    async def moeda(self, ctx):
        lados = ["**Cara** <:Cara:905202890900140042>",
        "**Coroa** <:Coroa:905202909216669776>"]
        moeda = random.choice(lados)
        embed = discord.Embed(
            description = f"{ctx.author.mention} jogou a moeda, e caiu: {moeda}",
            color = 0xffbb00,
        )
        embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="slap", aliases = ["tapa"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def slap(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        bite_image = ["https://c.tenor.com/Ws6Dm1ZW_vMAAAAS/girl-slap.gif",
        "https://c.tenor.com/PeJyQRCSHHkAAAAC/saki-saki-mukai-naoya.gif",
        "https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif",
        "https://c.tenor.com/UDo0WPttiRsAAAAd/bunny-girl-slap.gif",
        "https://c.tenor.com/eU5H6GbVjrcAAAAC/slap-jjk.gif",
        "https://c.tenor.com/E3OW-MYYum0AAAAS/no-angry.gif",
        "https://c.tenor.com/FJsjk_9b_XgAAAAC/anime-hit.gif",
        "https://c.tenor.com/BYu41fLSstAAAAAC/when-you-cant-accept-reality-slap.gif",
        "https://c.tenor.com/pHCT4ynbGIUAAAAS/anime-girl.gif",
        "https://c.tenor.com/1-1M4PZpYcMAAAAd/tsuki-tsuki-ga.gif",
        "https://c.tenor.com/VlSXTbFcvDQAAAAC/naruto-anime.gif",
        "https://c.tenor.com/ra17G61QRQQAAAAC/tapa-slap.gif",
        "https://c.tenor.com/noSQI-GitQMAAAAC/mm-emu-emu.gif",
        "https://c.tenor.com/bW9sL6u6V7AAAAAC/fly-away-slap.gif",
        "https://c.tenor.com/rVXByOZKidMAAAAd/anime-slap.gif",
        "https://c.tenor.com/uTT2gXruNtkAAAAC/oreimo-anime.gif",
        "https://c.tenor.com/hNa8BhraaXsAAAAC/anime-nagatoro.gif",
        "https://c.tenor.com/5eI0koENMAAAAAAC/anime-hit.gif",
        "https://c.tenor.com/AlM5Pxv06fUAAAAC/anime-slap.gif",
        "https://c.tenor.com/1lemb3ZmGf8AAAAC/anime-slap.gif",
        "https://c.tenor.com/OuYAPinRFYgAAAAC/anime-slap.gif",
        "https://c.tenor.com/CvBTA0GyrogAAAAC/anime-slap.gif",
        "https://c.tenor.com/DTVNVJrDdJIAAAAC/my-collection-anime.gif",
        "https://c.tenor.com/2HjyotNxqiAAAAAC/cass-will.gif",
        "https://c.tenor.com/j6UWDrX6ZrwAAAAd/arima-ichika-ichika.gif",
        "https://c.tenor.com/Op1oKmvsluwAAAAC/cop-craft-tilarna.gif",
        "https://c.tenor.com/PgHtCt1pU_0AAAAC/smack-dog.gif",
        "https://c.tenor.com/wV8HVCDJXS8AAAAC/angry-fight.gif",
        "https://c.tenor.com/qfTPbGj_JNsAAAAC/konosuba-megumin.gif",
        "https://c.tenor.com/Z7OrR3PfW6IAAAAC/kekkaishi-slap.gif",
        ]
        bite = random.choice(bite_image)
        if member == None:
            bite_image = discord.Embed(
                color = 0xffbb00,
            )
            bite_image.set_image(url=bite)
            bite_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=bite_image)
        else:
            bite_image = discord.Embed(
                description = f"🤚| {ctx.author.mention} deu um tapa em {member.mention}",
                color = 0xffbb00,
            )
            bite_image.set_image(url=bite)
            bite_image.set_footer(text=f"{ctx.author.name} | " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=bite_image)

def setup(bot):
    bot.add_cog(cog_fun(bot))