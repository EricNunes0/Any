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
class cog_amogus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "amogus", aliases = ["sus", "amongus"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def amogus(self, ctx):
        try:
            num = random.randint(0,24)
            squares = ["🟥","🟥","🟧","🟨","🟩","🟪","🟫","⬜","⬛","⏹️",":flag_br:",":flag_es:","🇨🇳","🇬🇧", "🇳🇱", "🇦🇲", "🇦🇷", "🇦🇹", "🇦🇽", "🇦🇿", "🇧🇪", "🇨🇦", "🇫🇷", "🇮🇹", "🇯🇵", "🇰🇷"]
            s = squares[num]
            sus = f"➖➖{s}{s}{s}\n➖{s}{s}🟦🟦🟦\n{s}{s}{s}🟦🟦🟦\n{s}{s}{s}🟦🟦🟦\n{s}{s}{s}{s}{s}{s}\n➖{s}{s}{s}{s}{s}\n➖{s}{s}➖{s}{s}\n➖{s}{s}➖{s}{s}"
            await ctx.send(sus)
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}amogus")
    await bot.add_cog(cog_amogus(bot))