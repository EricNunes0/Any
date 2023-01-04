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

now = datetime.datetime.now()
dateOn = now.strftime("%d/%m/%Y - %H:%M:%S")
dateTimestamp = now.timestamp()

class cog_uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "uptime", pass_context = True, aliases = ["timeup"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def uptime(self, ctx):
        try:
            uptimeEmbed = discord.Embed(color = discord.Color.from_rgb(240, 60, 200))
            uptimeEmbed.set_author(name = f"『🕰』Uptime:", icon_url = self.bot.user.display_avatar.url)
            uptimeEmbed.add_field(name = "『⏲️』Ligado em:", value = f"**<t:{int(dateTimestamp)}> (<t:{int(dateTimestamp)}:R>)**", inline = True)
            uptimeEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.reply(embed = uptimeEmbed)
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}uptime")
    await bot.add_cog(cog_uptime(bot))