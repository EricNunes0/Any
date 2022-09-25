import discord
from discord.ext import commands
import datetime
import json

intents = discord.Intents.default()
intents.members = True
now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

#def get_prefix(bot, message):
#    with open('prefixes.json', 'r') as f:
#        prefixes = json.load(f)
#    return prefixes[str(message.guild.id)]
command_prefix = "a!"
bot = commands.Bot(command_prefix = "a!", intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class cog_sup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="support", aliases = ["sup", "suporte"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def diversos(self, ctx):
        embed = discord.Embed(title = f"『❕』Suporte [1]",description =  "**`ticket`**",color = 0xc8c8c8)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {command_prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/djyLLS5.gif")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(cog_sup(bot))