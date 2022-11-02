import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import requests
import dotenv
import random
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import json

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

with open("config.json", "r") as f:
    config = json.load(f)
l = open("link.json")
link = json.load(l)
prefix = config[str("prefix")]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)
print(prefix)
bot = commands.Bot(command_prefix = prefix, case_insensitive = True, intents = intents)
bot.remove_command("help")

cogs = os.listdir("./cogs")
async def loadExtensions():
    for filename in cogs:
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

os.chdir("./images")

@bot.event
async def on_ready():
    activity = discord.Game(name=f"{prefix}help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    welcomeChannel = bot.get_channel(982824719046832188)
    await welcomeChannel.send(content = f"**Estou online! 🟢**")
    print(f"Estou pronto! Eu sou o {bot.user}")
    bot.loop.create_task(statuschange())

async def statuschange():
    activity1 = discord.Game(name=f"120 comandos no AnyBot!", type=3)
    activity2 = discord.Activity(name=f"a!help", type=3)
    activity3 = discord.Game(name=f"Comandos slash em breve...", type=3)
    activity4 = discord.Game(name=f"Janny City Adventures", type=3)
    activity5 = discord.Activity(name=f"vocês :)", type = 3)
    
    while True:
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=activity1)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity2)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity3)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity4)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity5)
        await asyncio.sleep(10)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message[0] == prefix:
        return
    if message.author == bot.user:
        return
    if bot.user.mention in message.content:
        print("on_message()")
        return await message.channel.send(f"Oi, meu prefixo é `{prefix}`. Digite {prefix}help para ver os meus comandos!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        message = await ctx.send(f"❌| {ctx.author.mention}, este comando não existe, ou foi removido!\n❓| Se quiser ver todos os meus comandos, digite `{prefix}comandos`")
        await asyncio.sleep(5)
        await message.delete()
    if isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send("⏱| {}, espera aí! Este comando tem cooldown!\n⏲| Espere `{:.2f}` para usar o comando novamente.".format(ctx.author.mention,error.retry_after))
        await ctx.message.delete()
        await asyncio.sleep(5)
        await message.delete()

@bot.event
async def on_member_join(member):
    try:
        if member.guild.id == 710506024489976028:
            rankRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721298086166568)
            colorRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721809883537458)
            registerRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908728253513080833)
            await member.add_roles(rankRole, colorRole, registerRole)
            welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
            e = random.choice(welEmjs)
            guildMemberAdd = discord.Embed(color = 0x400070)
            guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.display_avatar.url)
            guildMemberAdd.add_field(name = f"『{e}』 Membro novo!", value = f"**『{link['grayDiamond']}』Regras:** <#1026231571776294942>\n**『{link['yellowDiamond']}』Registre-se:** <#770250817684635658>\n**『{link['purpleDiamond']}』F.A.Q.:** <#710506024964063316>")
            guildMemberAdd.set_thumbnail(url = member.display_avatar.url)
            guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = member.display_avatar.url)
            welcomeChannel = bot.get_channel(723155037332832296)
            userAvatar = member.display_avatar.url
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((206,206))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new("L", bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)
            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
            saida.putalpha(mascara)
            saida.save("img_avatar.png")
            img = Image.open("img_entrance(1).png")
            img.paste(avatar, (190, 61), avatar)
            img.save("img_entrance.png")
            file = discord.File("img_entrance.png")
            guildMemberAdd.set_image(url="attachment://img_entrance.png")
            message = await welcomeChannel.send(content = member.mention, embed = guildMemberAdd, file = file)
    except Exception as e:
        print(e)

@bot.command(name = "welcome", aliases = ["wlcm", "wlmc", "wlc"])
async def welcome(ctx, member: discord.Member):
    try:
        if not member:
            member = ctx.author
        if member.guild.id == 710506024489976028:
            rankRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721298086166568)
            colorRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721809883537458)
            registerRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908728253513080833)
            await member.add_roles(rankRole, colorRole, registerRole)
            welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
            e = random.choice(welEmjs)
            userAvatar = member.display_avatar.url
            guildMemberAdd = discord.Embed(color = 0x400070)
            guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = userAvatar)
            guildMemberAdd.add_field(name = f"『{e}』 Membro novo!", value = f"**『{link['grayDiamond']}』Regras:** <#1026231571776294942>\n**『{link['yellowDiamond']}』Registre-se:** <#770250817684635658>\n**『{link['purpleDiamond']}』F.A.Q.:** <#710506024964063316>")
            guildMemberAdd.set_thumbnail(url = userAvatar)
            guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = userAvatar)
            welcomeChannel = bot.get_channel(740760158098948097)
            print(userAvatar)
            url = requests.get(userAvatar)
            avatar = Image.open(BytesIO(url.content)).convert('RGB')
            avatar = avatar.resize((206,206))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new("L", bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)
            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
            saida.putalpha(mascara)
            saida.save("img_avatar.png")
            img = Image.open("img_entrance(1).png")
            img.paste(avatar, (190, 61), avatar)
            img.save("img_entrance.png")
            file = discord.File("img_entrance.png")
            guildMemberAdd.set_image(url="attachment://img_entrance.png")
            message = await welcomeChannel.send(content = member.mention, embed = guildMemberAdd, file = file)
    except Exception as e:
        print(e)
async def main():
    async with bot:
        await loadExtensions()
        await bot.start(TOKEN)

asyncio.run(main())