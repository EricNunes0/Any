import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import json
import aiohttp

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

bot.ses = aiohttp.ClientSession()
class cog_roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "roleslist", aliases = ["rolelist"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def button(self, ctx, message: discord.Message = None):
        try:
            roles1Embed = discord.Embed(
                title = "<a:ab_RedRight:975521519184785428> Cargos da Janny City <a:ab_RedLeft:975521412817248306>",
                description = "Este canal tem o propósito de apresentar os cargos mais importantes do servidor, e as suas respectivas funções!",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            roles1Embed.add_field(name = "Cargos da Administração:", inline = False, value = 
"""
<@&981694221729816607> ➺ Exclusivo para os bots principais do servidor, o <@900346730237820939> e o <@911002921594925056>!

<@&789133849841106994> ➺ Exclusivo para o dono do servidor e criador dos bots **Any** e **Janny**! É a autoridade máxima do servidor, responsável por tomar a maioria das decisões e administrar a cidade.

<@&739210760567390250> ➺ São os administradores do servidor que, assim como o dono, possuem a mesma autoridade e funções, então melhor tomar cuidado com o que faz, os adms estão sempre de olho. <:j_Felizuhul:1058536894805319690>
"""
            )
            roles1Embed.set_image(url = "https://i.imgur.com/u5rTAfS.png")
            roles1Embed.set_footer(text = "Regras da Janny City!")
            await message.edit(content = "", embed = roles1Embed)
            return
        except Exception as e:
            print(e)

    @button.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}roles")
    await bot.add_cog(cog_roles(bot))