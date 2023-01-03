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

class cog_misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="diversos", aliases = ["misc", "🗃️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def diversos(self, ctx):
        try:
            embed = discord.Embed(title = f"『🗃️』Diversos [5]", description =  "**`botinfo - dica - ping - uptime - vote`**", color = 0xf020d0)
            embed.set_footer(text = f"• Para obter informações de cada comando, digite a!help <comando>", icon_url = self.bot.user.display_avatar.url)
            embed.set_thumbnail(url = "https://i.imgur.com/oI4uuB3.gif")
            await ctx.reply(embed = embed)
        except Exception as e:
            print(e)

    @commands.command(name="botinfo", aliases = ["infobot"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def botinfo(self, ctx):
        try:
            l = open("..\\link.json")
            link = json.load(l)
            embed = discord.Embed(title = f"『{link['yellowDiamond']}』 Olá, eu me chamo {self.bot.user.name} 『{link['yellowDiamond']}』", description = f"Olá, meu nome é **{self.bot.user.name}**, e eu sou o bot exclusivo da **Janny City**! Sou o responsável pela moderação do servidor, estou aqui para ajudar a manter as coisas em ordem. 😎\n\nInicialmente, eu fui criado apenas para divertir um grupo de amigos do meu criador, e nem tinha planos de me tornar o bot que sou hoje.\n\nEu fui criado em **[Python](https://www.python.org/)** usando o **[Visual Studio Code](https://code.visualstudio.com/)**!", color = 0xf020d0)
            embed.add_field(name = "『👑』Criado por:", value = "`Eric2605#9133`", inline = True)
            embed.add_field(name = "『🐧』Ping:", value = f"`{round(self.bot.latency * 1000)}ms`", inline = True)
            embed.add_field(name = "『👶』Criado às:", value = f"`20/10/2021 às 11:36`", inline = True)
            embed.add_field(name = "『👨‍💻』Desenvolvido em:", value = f"`Python (discord.py)`", inline = True)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now, icon_url= ctx.author.display_avatar.url)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            await ctx.reply(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(name="ping", pass_context=True, aliases=["latency", "latencia"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def ping(self, ctx):
        l = open("..\\link.json")
        link = json.load(l)
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        pingEmbed = discord.Embed(title = f"**『{link['pinkDiamond']}』Pinguim?**", color = 0xf020d0)
        pingEmbed.add_field(name = "『⏲️』Latência:", value = f"**`{round(self.bot.latency * 1000)}ms`**", inline = True)
        pingEmbed.set_thumbnail(url = "https://i.imgur.com/rqZKRFx.png")
        pingEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
        await ctx.reply(embed = pingEmbed)

async def setup(bot):
    print("cog_misc.py loaded")
    await bot.add_cog(cog_misc(bot))