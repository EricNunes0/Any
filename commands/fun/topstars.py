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

bot.ses = aiohttp.ClientSession()
class cog_topstars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "topstars", aliases = ["topstar"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def topstars(self, ctx):
        try:
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            usersStars = getAllStars()
            countList = []
            usersList = []
            for userStar in usersStars:
                usersList.append(userStar["userId"])
                countList.append(userStar["total"])
            starsEmbed = discord.Embed(
                color = discord.Color.from_rgb(250, 230, 20)
            )
            starsEmbed.set_author(name = f"『🌟』Top Stars:", icon_url = self.bot.user.display_avatar.url)
            emjsPos = ["🥇", "🥈", "🥉", "🔸", "🔸"]
            for i in range(0, 5):
                user = await self.bot.fetch_user(usersList[i])
                print(user)
                starsEmbed.add_field(name = f"『{emjsPos[i]}』{user.name}:", value = f"**{countList[i]}**", inline = False)
            starsEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            starsEmbed.set_thumbnail(url = link["stars"]["thumbs"][f"2"])
            await ctx.reply(embed = starsEmbed)
            return
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}topstars")
    await bot.add_cog(cog_topstars(bot))