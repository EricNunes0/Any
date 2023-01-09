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
class cog_stars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "stars", aliases = ["star"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def stars(self, ctx, *, user: discord.User = None):
        try:
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            if user == None:
                user = ctx.author
            print(user.id)
            userStars = getStar(user.id)
            print(1, userStars)
            starsList = [userStars['stars']['0'], userStars['stars']['1'], userStars['stars']['2'], userStars['stars']['3'], userStars['stars']['4']]
            starMax = starsList.index(max(starsList))
            starsTotal = 0
            for i in range(0, len(starsList)):    
                starsTotal = starsTotal + starsList[i]
            starsEmbed = discord.Embed(
                color = discord.Color.from_rgb(link["stars"]["colors"][f"{starMax}"][0], link["stars"]["colors"][f"{starMax}"][1], link["stars"]["colors"][f"{starMax}"][2])
            )
            starsEmbed.set_author(name = f"『⭐』Estrelas de {user.name}:", icon_url = self.bot.user.display_avatar.url)
            starsEmbed.add_field(name = f"『🌠』Total:", value = f"**{starsTotal}**", inline = False)
            starsEmbed.add_field(name = f"『🌌』Cores:", value = f"**『{link['stars']['emjs']['0']}』Vermelhas: `{starsList[0]}`\n『{link['stars']['emjs']['1']}』Laranjas: `{starsList[1]}`\n『{link['stars']['emjs']['2']}』Amarelas: `{starsList[2]}`\n『{link['stars']['emjs']['3']}』Verdes: `{starsList[3]}`\n『{link['stars']['emjs']['4']}』Azuis: `{starsList[4]}`**", inline = False)
            starsEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            starsEmbed.set_thumbnail(url = link["stars"]["thumbs"][f"{starMax}"])
            await ctx.reply(embed = starsEmbed)
            return
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}stars")
    await bot.add_cog(cog_stars(bot))