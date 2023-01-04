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

class cog_misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "misc", aliases = ["diversos", "diverso", "extras", "extra", "infos", "info"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def diversos(self, ctx):
        try:
            miscEmbed = discord.Embed(
                title = f"Comandos diversos 『3』",
                description =  "**`botinfo - ping - uptime`**",
                color = discord.Color.from_rgb(240, 60, 200)
            )
            miscEmbed.set_author(name = f"『🗃️』Diversos:", icon_url = self.bot.user.display_avatar.url)
            miscEmbed.set_footer(text = f"Para obter informações de cada comando, digite {prefix}help <comando>", icon_url = self.bot.user.display_avatar.url)
            miscEmbed.set_thumbnail(url = link["pinkHelp"])
            await ctx.reply(embed = miscEmbed)
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}misc")
    await bot.add_cog(cog_misc(bot))