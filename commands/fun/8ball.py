import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import random
import json
import aiohttp
from mongoconnection.star import *

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

bot.ses = aiohttp.ClientSession()
class cog_8ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "ball", aliases = ["8ball", "pergunta"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def ball(self, ctx, *, message):
        try:
            answers = ["Sim!✔","Não!❌","Provavelmente sim ☑","Provavelmente não ✖","Claro que sim!✅","Claro que não!❎","Acho que sim☑","Acho que não ✖","Minhas fontes dizem que sim ✔","Minhas fontes dizem que não ❌"]
            escolha = random.choice(answers)
            ballEmbed = discord.Embed(color = discord.Color.from_rgb(255, 208, 32))
            ballEmbed.set_author(name = f"『🎱』8ball:", icon_url = self.bot.user.display_avatar.url)
            ballEmbed.add_field(name = "『❔』Pergunta:", value = f"```{message}```", inline = False)
            ballEmbed.add_field(name = "『🎱』Resposta:", value = f"```{escolha}```", inline = False)
            ballEmbed.set_footer(text=f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
            await ctx.send(embed = ballEmbed)
        except Exception as e:
            print(e)
    
    @ball.error
    async def ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            embed = discord.Embed(title = f"『🎱』{prefix}8ball", color = 0xffbb00)
            embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.avatar.url)
            embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Responde qualquer pergunta com 100% de precisão 😎.`", inline = False)
            embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{prefix}ball, {prefix}pergunta`", inline = False)
            embed.add_field(name = f"『⚙️』Uso:", value = f"`{prefix}8ball <pergunta>`", inline = False)
            embed.add_field(name = f"『💬』Exemplos¹ (60 segundos):", value = f"`{prefix}8ball Eu vou ganhar na loteria?`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões do usuário:", value = f"`Nenhuma`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões do bot:", value = f"`Ver canais, Enviar mensagens`", inline = False)
            embed.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar.url)
            embed.set_thumbnail(url="https://i.imgur.com/2nkTc33.gif")
            await ctx.reply(embed=embed)
    
async def setup(bot):
    print(f"{prefix}8ball")
    await bot.add_cog(cog_8ball(bot))