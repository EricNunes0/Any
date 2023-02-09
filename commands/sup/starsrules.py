import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import random
import json
import aiohttp
from handlers.starRules import *

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
class cog_starsRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "starsrules", aliases = ["starrules", "starrule", "rulesstars", "rulestars", "regrasstars", "regrasstar", "regrastar"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 1, type = commands.BucketType.user)
    async def starsrules(self, ctx,):
        try:
            starRulesChannel = self.bot.get_channel(1071285010574868501)
            await starRulesLoop(bot = self.bot, channel = starRulesChannel)
            return
        except Exception as e:
            print(e)

    @starsrules.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}starsrules")
    await bot.add_cog(cog_starsRules(bot))