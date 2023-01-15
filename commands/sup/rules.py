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

class rulesClass(discord.ui.View):
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    @discord.ui.button(label = f"Regras", style = discord.ButtonStyle.blurple, emoji = "📃")
    async def ruleInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.text, ephemeral = True)

bot.ses = aiohttp.ClientSession()
class cog_rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "rules", aliases = ["rule"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def button(self, ctx, message: discord.Message = None):
        try:
            print(message)
            await message.edit(view = rulesClass("Não quebre as regras!"))
            return
        except Exception as e:
            print(e)

    @button.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}rules")
    await bot.add_cog(cog_rules(bot))