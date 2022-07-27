import discord
from discord import *
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import dotenv
import datetime
import random
from pprint import pprint
import discord_slash
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord_components import DiscordComponents, ActionRow, ComponentsBot, Button, ButtonStyle, Select, SelectOption
import re
import json
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = discord.Client()
bot = commands.Bot(command_prefix = "a!", case_insensitive = True,  intents = intents)
DiscordComponents(bot)
command_prefix = "a!"
bot.remove_command("help")
slash = discord_slash.SlashCommand(bot, sync_commands = True)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

os.chdir("./images")

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
async def on_ready():
    activity = discord.Game(name=f"a!help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Estou pronto! Eu sou o {bot.user}")
    bot.loop.create_task(statuschange())

@bot.event
async def on_message(message):
    if message.content.startswith(bot.user.mention):
        await message.channel.send(f"Oi, meu prefixo é `{command_prefix}`. Digite {command_prefix}help para ver os meus comandos!")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        message = await ctx.send(f"❌| {ctx.author.mention}, este comando não existe, ou foi removido!\n❓| Se quiser ver todos os meus comandos, digite `{command_prefix}comandos`")
        await asyncio.sleep(5)
        await message.delete()
    if isinstance(error, commands.CommandOnCooldown):
        message = await ctx.send("⏱| {}, espera aí! Este comando tem cooldown!\n⏲| Espere `{:.2f}` para usar o comando novamente.".format(ctx.author.mention,error.retry_after))
        await ctx.message.delete()
        await asyncio.sleep(5)
        await message.delete()

@bot.event
async def on_member_join(member):
    if member.guild.id == 710506024489976028:
        rankRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721298086166568)
        colorRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721809883537458)
        registerRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908728253513080833)
        await member.add_roles(rankRole, colorRole, registerRole)
        welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
        e = random.choice(welEmjs)
        guildMemberAdd = discord.Embed(title = f"{e} Membro novo!", color = 0xffbb00)
        guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.avatar_url)
        guildMemberAdd.add_field(name = "『<a:ab_BlueDiamond:938850305083314207>』Regras:", value = "<#736658586012483594>", inline = True)
        guildMemberAdd.add_field(name = "『<a:ab_YellowDiamond:938857668888645673>』Registre-se:", value = "<#770250817684635658>", inline = True)
        guildMemberAdd.add_field(name = "『<a:ab_GreenDiamond:938880803692240927>』Mapa:", value = "<#710506024964063316>", inline = True)
        guildMemberAdd.set_thumbnail(url = member.avatar_url)
        guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = member.avatar_url)
        welcomeChannel = bot.get_channel(723155037332832296)
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        avatar = Image.open(BytesIO(url.content)).convert('RGB')
        avatar = avatar.resize((206,206))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save("img_avatar.png", format="png", lossless=True)
        img = Image.open("img_background(1).png")
        img.paste(avatar, (190, 61), avatar)
        img.save('img_background.png')
        file = discord.File("img_background.png")
        guildMemberAdd.set_image(url="attachment://img_background.png")
        message = await welcomeChannel.send(content = member.mention, embed = guildMemberAdd, file = file)

@bot.command(name = "welcome")
async def welcome(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    if member.guild.id == 710506024489976028:
        rankRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721298086166568)
        colorRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721809883537458)
        registerRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908728253513080833)
        await member.add_roles(rankRole, colorRole, registerRole)
        welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
        e = random.choice(welEmjs)
        guildMemberAdd = discord.Embed(title = f"{e} Membro novo!", color = 0xffbb00)
        guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.avatar_url)
        guildMemberAdd.add_field(name = "『<a:ab_BlueDiamond:938850305083314207>』Regras:", value = "<#736658586012483594>", inline = True)
        guildMemberAdd.add_field(name = "『<a:ab_YellowDiamond:938857668888645673>』Registre-se:", value = "<#770250817684635658>", inline = True)
        guildMemberAdd.add_field(name = "『<a:ab_GreenDiamond:938880803692240927>』Mapa:", value = "<#710506024964063316>", inline = True)
        guildMemberAdd.set_thumbnail(url = member.avatar_url)
        guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = member.avatar_url)
        welcomeChannel = bot.get_channel(740760158098948097)
        #welcomeChannel = bot.get_channel(723155037332832296)
        userAvatar = member.avatar_url
        url = requests.get(userAvatar)
        avatar = Image.open(BytesIO(url.content)).convert('RGB')
        avatar = avatar.resize((206,206))
        bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', bigavatar, 0)
        recortar = ImageDraw.Draw(mascara)
        recortar.ellipse((0, 0) + bigavatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
        saida.putalpha(mascara)
        saida.save("img_avatar.png", format="png", lossless=True)
        img = Image.open("img_background(1).png")
        img.paste(avatar, (190, 61), avatar)
        img.save('img_background.png')
        file = discord.File("img_background.png")
        guildMemberAdd.set_image(url="attachment://img_background.png")
        message = await welcomeChannel.send(content = member.mention, embed = guildMemberAdd, file = file)

@bot.command(name = "heart")
async def heart(ctx):
    userAvatar = ctx.author.avatar_url
    url = requests.get(userAvatar)
    avatar = Image.open(BytesIO(url.content))
    avatar = avatar.resize((206,206))
    bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
    mascara = Image.new('L', bigavatar, 0)
    recortar = ImageDraw.Draw(mascara)
    recortar.ellipse((0, 0) + bigavatar, fill=255)
    mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mascara)
    saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 1.5))
    saida.putalpha(mascara)
    saida.save('img_avatar.png')
    heart = Image.open("img_heart.png")
    heart = heart.resize((100,100))
    img = Image.open("img_background(2).png")
    img.paste(avatar, (190, 61), avatar)
    img.paste(heart, (50, 50), heart)
    img.paste(heart, (50, 200), heart)
    img.paste(heart, (450, 50), heart)
    img.paste(heart, (450, 200), heart)
    fonte1 = ImageFont.truetype("font_coolvetica_rg.ttf", 35)
    fonte2 = ImageFont.truetype("font_coolvetica_rg.ttf", 35)
    escrever = ImageDraw.Draw(img)
    escrever.text(xy=(40,300), text=f"R-ROI PRINCESA, LOVE", fill=(0, 0, 0), font=fonte1)
    escrever.text(xy=(40,301), text=f"R-ROI PRINCESA, LOVE", fill=(255, 255, 255), font=fonte2)
    img.save('img_background.png')
    file = discord.File("img_background.png")
    heartEmbed = discord.Embed(title = f"『❤️』Cidade do Amor!", color = 0xff2020,  timestamp=datetime.datetime.utcnow())
    heartEmbed.set_footer(text = f"O amor está no ar", icon_url = ctx.author.avatar_url)
    heartEmbed.set_image(url="attachment://img_background.png")
    await ctx.reply(content = ctx.author.mention, embed = heartEmbed, file = file)

@bot.command(name = "join")
@bot_has_permissions(add_reactions = True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name = "leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)