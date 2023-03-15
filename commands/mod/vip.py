import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from mongoconnection.vip import *

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

vipNames = ["Ametista", "Jade", "Safira"]
vipRoles = [1051948366461939744, 1047268770504253561, 1047268807812595802]
vipEmojis = ["<a:ab_PurpleDiamond:938883672717787196>", "<a:ab_GreenDiamond:938880803692240927>", "<a:ab_BlueDiamond:938850305083314207>"]

bot.ses = aiohttp.ClientSession()
class cog_vip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "vip", aliases = ["vippe"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def vip(self, ctx):
        try:
            dbname = getDatabase()
            collectionName = dbname["vip"]
            vip = collectionName.find_one({"User": ctx.author.id})
            print(vip)
            if vip == None:
                noVip = discord.Embed(
                    title = f"Sem VIP!",
                    description = f"『❌』Você não possui um plano VIP ativo no momento. Confira todos os benefícios de se tornar um VIP em <#1047316824976523354>",
                    color = 0xFF0000
                )
                noVip.set_thumbnail(url = link["error"])
                noVip.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
                await ctx.reply(embed = noVip)
                return
            vipEmbed = discord.Embed(
                color = discord.Color.from_rgb(200, 20, 255)
            )
            vipRole = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id = int(vipRoles[vip["Vip"]]))
            if vip["Role"] != None:
                roleFound = discord.utils.get(self.bot.get_guild(ctx.guild.id).roles, id = int(vip["Role"]))
                userRole = roleFound.mention
            else:
                userRole = "`Nenhum`"
            if vip["Channel"] != None:
                foundChannel = discord.utils.get(self.bot.get_guild(ctx.guild.id).voice_channels, id = int(vip["Channel"]))
                userChannel = foundChannel.mention
            else:
                userChannel = "`Nenhum`"
            if len(vip["Friends"]) == 0:
                userFriends = "`Nenhum`"
            else:
                f = []
                for friend in self.config["friends"]:
                    user = await self.bot.fetch_user(int(friend))
                    f.append(f"{user.mention}")
                userFriends = "\n".join(f)
            vipEmbed.set_author(name = f"『💎』VIP:", icon_url = self.bot.user.display_avatar.url)
            vipEmbed.add_field(name = f"『💎』VIP atual:", value = f"{vipRole.mention}", inline = False)
            vipEmbed.add_field(name = f"『⏰』Termina em:", value = f"<t:{vip['EndsAt']}>", inline = False)
            vipEmbed.add_field(name = f"『💼』Seu cargo:", value = userRole, inline = False)
            vipEmbed.add_field(name = f"『🔊』Seu canal:", value = userChannel, inline = False)
            vipEmbed.add_field(name = f"『👥』Amigos:", value = userFriends, inline = False)
            vipEmbed.set_thumbnail(url = ctx.author.display_avatar.url)
            vipEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.reply(embed = vipEmbed)
            return
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}vip")
    await bot.add_cog(cog_vip(bot))