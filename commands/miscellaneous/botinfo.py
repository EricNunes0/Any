import discord
from discord.ext import commands
import datetime
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
dateOn = now.strftime("%d/%m/%Y - %H:%M:%S")
dateTimestamp = now.timestamp()

class cog_botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "botinfo", pass_context = True, aliases = ["infobot"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def botinfo(self, ctx):
        try:
            botinfoEmbed = discord.Embed(
                title = f"{link['yellowDiamond']} Olá, sou o {self.bot.user.name} {link['yellowDiamond']}",
                description = f"Olá, meu nome é **{self.bot.user.name}**, e eu sou o bot exclusivo da **Janny City**! Sou o responsável pela moderação do servidor, estou aqui para ajudar a manter as coisas em ordem. 😎\n\nInicialmente, eu fui criado apenas para divertir um grupo de amigos do meu criador, e nem tinha planos de me tornar o bot que sou hoje.\n\nEu fui criado em **[Python](https://www.python.org/)** usando o **[Visual Studio Code](https://code.visualstudio.com/)**. Se você quiser saber como fui criado, você pode ver meu código-fonte **[aqui](https://github.com/EricNunes0/Any)** `(e não esqueça de seguir o meu criador, não custa nada ^-^)`!",
                color = discord.Color.from_rgb(240, 210, 0)
            )
            botinfoEmbed.set_author(name = f"『🤖』Botinfo:", icon_url = self.bot.user.display_avatar.url)
            botinfoEmbed.add_field(name = "『👑』Criado por:", value = "`Eric2605#9133`", inline = True)
            botinfoEmbed.add_field(name = "『🐧』Ping:", value = f"`{round(self.bot.latency * 1000)}ms`", inline = True)
            botinfoEmbed.add_field(name = "『🗓️』Criado às:", value = f"`20/10/2021 às 11:36`", inline = True)
            botinfoEmbed.add_field(name = "『👨‍💻』Desenvolvido em:", value = f"`Python (discord.py)`", inline = True)
            botinfoEmbed.add_field(name = "『⏲️』Ligado em:", value = f"**<t:{int(dateTimestamp)}> (<t:{int(dateTimestamp)}:R>)**", inline = True)
            botinfoEmbed.add_field(name = "『💿』Versão:", value = f"`{config['version']}`", inline = True)
            botinfoEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
            botinfoEmbed.set_thumbnail(url = self.bot.user.display_avatar.url)
            await ctx.reply(embed = botinfoEmbed)
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}botinfo")
    await bot.add_cog(cog_botinfo(bot))