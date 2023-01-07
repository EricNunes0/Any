import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
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

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

class afkButtons(discord.ui.View):
    def __init__(self, bot, userId):
        super().__init__()
        self.bot = bot
        self.userId = userId
    
    @discord.ui.button(label = f"Desativar", style = discord.ButtonStyle.blurple, emoji = f"{link['afkOffEmj']}")
    async def afkDisableButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            
            if int(interaction.user.id) == int(self.userId):
                afkDisableEmbed = discord.Embed(title = "Seu AFK foi desativado!",
                color = discord.Color.from_rgb(50, 100, 255))
                afkDisableEmbed.set_author(name = "『🔔』AFK:", icon_url = self.bot.user.display_avatar.url)
                afkDisableEmbed.set_thumbnail(url = link["afkOffThumb"])
                await interaction.response.edit_message(embed = afkDisableEmbed, view = None)
                #disableAfk(self.userId)
                return
            else:
                invalidUserEmbed = discord.Embed(title = f"Espera aí!", description = f"『❌』Apenas <@{self.userId}> pode desativar o AFK!", color = 0xFF0000)
                invalidUserEmbed.set_thumbnail(url = link["error"])
                await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
                return
        except Exception as e:
            print(e)

bot.ses = aiohttp.ClientSession()
class cog_stars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "stars", aliases = ["star"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def stars(self, ctx, *, user: discord.User = None):
        try:
            #afkHelpEmbed = discord.Embed(title = f"『🔕』{prefix}afk", color = discord.Color.from_rgb(20, 90, 255))
            #afkHelpEmbed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.display_avatar.url)
            #afkHelpEmbed.add_field(name = f"『ℹ️』Descrição:", value = f"`Ative o modo AFK para que todos saibam que você não pode responder mensagens no momento!`", inline = False)
            #afkHelpEmbed.add_field(name = f"『🔀』Sinônimos:", value = f"`{prefix}awayfromkeyboard`", inline = False)
            #afkHelpEmbed.add_field(name = f"『⚙️』Uso:", value = f"`{prefix}afk (motivo)`", inline = False)
            #afkHelpEmbed.add_field(name = f"『🔔』Como ligar:", value = f"`{prefix}afk Estou trabalhando`", inline = False)
            #afkHelpEmbed.add_field(name = f"『🔕』Como desligar:", value = f"`O AFK será desativado automaticamente assim que você enviar uma mensagem.`", inline = False)
            #afkHelpEmbed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Administrador`", inline = False)
            #afkHelpEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
            #afkHelpEmbed.set_thumbnail(url = link["blueHelp"])
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            if user == None:
                user = ctx.author
            print(user.id)
            userStars = getStar(user.id)
            starsList = [userStars['stars']['0'], userStars['stars']['1'], userStars['stars']['2'], userStars['stars']['3'], userStars['stars']['4']]
            starMax = starsList.index(max(starsList))
            starsTotal = 0
            for i in range(0, len(starsList)):    
                starsTotal = starsTotal + starsList[i]
            starsEmbed = discord.Embed(
                color = discord.Color.from_rgb(link["stars"]["colors"][f"{starMax}"][0], link["stars"]["colors"][f"{starMax}"][1], link["stars"]["colors"][f"{starMax}"][2])
            )
            starsEmbed.set_author(name = f"『⭐』Estrelas:", icon_url = self.bot.user.display_avatar.url)
            starsEmbed.add_field(name = f"『🌠』Total:", value = f"**{starsTotal}**", inline = False)
            starsEmbed.add_field(name = f"『🌌』Cores:", value = f"**『{link['stars']['emjs']['0']}』Vermelhas: `{starsList[0]}`\n『{link['stars']['emjs']['1']}』Laranjas: `{starsList[1]}`\n『{link['stars']['emjs']['2']}』Amarelas: `{starsList[2]}`\n『{link['stars']['emjs']['3']}』Verdes: `{starsList[3]}`\n『{link['stars']['emjs']['4']}』Azuis: `{starsList[4]}`**", inline = False)
            starsEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            starsEmbed.set_thumbnail(url = link["stars"]["thumbs"][f"{starMax}"])
            await ctx.reply(embed = starsEmbed)
            return
        except Exception as e:
            print(e)

    @stars.error
    async def afk_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}afk")
    await bot.add_cog(cog_stars(bot))