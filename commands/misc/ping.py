import discord
from discord.ext import commands
import datetime
import json

c = open("../config.json")
config = json.load(c)

l = open("../link.json")
link = json.load(l)

intents = discord.Intents.default()
intents.members = True

prefix = config["prefix"]
bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class cog_ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping", pass_context = True, aliases = ["latency", "latencia", "latência"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def ping(self, ctx):
        try:
            pingEmbed = discord.Embed(title = f"**『{link['pinkDiamond']}』Pinguim?**", color = discord.Color.from_rgb(240, 60, 200))
            pingEmbed.add_field(name = "『⏲️』Latência:", value = f"**`{round(self.bot.latency * 1000)}ms`**", inline = True)
            pingEmbed.set_thumbnail(url = "https://i.imgur.com/rqZKRFx.png")
            pingEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.reply(embed = pingEmbed)
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}ping")
    await bot.add_cog(cog_ping(bot))