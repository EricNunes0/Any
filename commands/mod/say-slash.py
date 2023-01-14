import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
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
class cog_say_slash(commands.GroupCog, name = "say"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @discord.app_commands.command(name = "admin", description = "Envie uma mensagem em um canal usando o bot!", nsfw = False)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def say_admin(self, interaction: discord.Integration, message: str, channel: discord.TextChannel = None):
        try:
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.send_message(embed = userPermAdmin, ephemeral = True)
                return
            sayAdminEmbed = discord.Embed(
                title = f"Mensagem enviada!",
                color = discord.Color.from_rgb(50, 100, 255)
            )
            if channel == None:
                channel = interaction.channel
            sayAdminEmbed.set_author(name = f"『👁‍🗨』Say Admin:", icon_url = self.bot.user.display_avatar.url)
            sayAdminEmbed.set_footer(text = f"Pedido por {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            sayAdminEmbed.set_thumbnail(url = link["blueChecked"])
            await interaction.response.send_message(embed = sayAdminEmbed, ephemeral = True)
            await channel.send(content = message)
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"/say")
    await bot.add_cog(cog_say_slash(bot))