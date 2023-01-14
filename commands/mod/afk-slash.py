import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from mongoconnection.afk import *

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
class cog_afk_slash(commands.GroupCog, name = "afk"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @discord.app_commands.command(name = "on", description = "Ative o modo AFK para que todos saibam que você não pode responder mensagens no momento!", nsfw = False)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def afk_on(self, interaction: discord.Integration, reason: str = None):
        try:
            print(interaction.user.guild_permissions.administrator)
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.send_message(embed = userPermAdmin, ephemeral = True)
                return
            if reason == None:
                reason = "Não informado"
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            findOneAfkAndUpdate(interaction.user.id, True, reason, int(timeStamp))
            afkOnEmbed = discord.Embed(
                title = f"AFK ligado!",
                color = discord.Color.from_rgb(50, 100, 255)
            )
            afkOnEmbed.set_author(name = f"『🔕』AFK:", icon_url = self.bot.user.display_avatar.url)
            afkOnEmbed.add_field(name = f"『⏰』Definido em:", value = f"<t:{int(timeStamp)}> (<t:{int(timeStamp)}:R>)", inline = True)
            afkOnEmbed.add_field(name = f"『💬』Mensagem:", value = f"`{reason}`", inline = False)
            afkOnEmbed.set_footer(text = f"Pedido por {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            afkOnEmbed.set_thumbnail(url = link["afkOnThumb"])
            await interaction.response.send_message(embed = afkOnEmbed, ephemeral = True)
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"/afk")
    await bot.add_cog(cog_afk_slash(bot))