import discord
from discord.ext import commands
import datetime
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

class cog_div(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="diversos", aliases = ["🗃️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def diversos(self, ctx):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『🗃️』Diversos [5]",description =  "**`botinfo - dica - ping - uptime - vote`**",color = 0xe61ec8)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {command_prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/oI4uuB3.gif")
        await ctx.reply(embed=embed)

    @commands.command(name="botinfo")
    @cooldown(1,3, type = commands.BucketType.user)
    async def botinfo(self, ctx):
        embed = discord.Embed(title = f"Olá, eu me chamo {self.bot.user.name} 💎",
            description = f"Olá, meu nome é **{self.bot.user.name}**, e eu sou um simples bot criado para testes. No momento, eu estou em desenvolvimento, então sempre estão sendo adicionados novas funções e comandos para mim! 😊\n\nInicialmente, eu fui criado apenas para divertir um grupo de amigos do meu criador, e nem tinha planos de me tornar o bot que sou hoje. Mesmo que eu não esteja pronto, ainda assim quero poder divertir as pessoas, e algum dia (quem sabe...), eu vou ser disponibilizado para convite!\n\nEu fui criado em <:ab_pythonIcon:913931980402483230> **[Python](https://www.python.org/)** utilizando o <:ab_visualCode:913931993895559169> **[Visual Studio Code](https://code.visualstudio.com/)**!\n\n👑 **Dono:** `Eric2605#9133`\n🏓 **Ping:** `{round(self.bot.latency * 1000)}ms`\n👶 **Criado em:** `20/10/2021 às 11:36`", color = 0xe61ec8)
        embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + "| 💰 +1", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #earnings = 1
        #users[str(ctx.author.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        await ctx.reply(embed=embed)

    @commands.command(name="ping", pass_context=True, aliases=["latency", "latencia"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def ping(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        pingEmbed = discord.Embed(description = f"**『🏓』Pong!\n『⏲️』Latência: `{round(self.bot.latency * 1000)}ms`**", color = 0xe61ec8)
        pingEmbed.set_footer(text = f"Pedido por {ctx.author} às {now}")
        await ctx.send(embed = pingEmbed)

def setup(bot):
    bot.add_cog(cog_div(bot))