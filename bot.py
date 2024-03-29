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
from mongoconnection.connect import getDatabase
from mongoconnection.afk import searchForAfk, reactionSearchForAfk
from mongoconnection.star import *
from handlers.antiInvite import *
from handlers.antiLongMessages import *
from handlers.antiSpam import *
from handlers.register import *
from handlers.shopColor import * #Loja de cores básicas
from handlers.shopColorBright import * # Loja de cores claras
from handlers.shopColorDark import * #Loja de cores escuras
from handlers.shopColorGray import * #Loja de cores neutras
from handlers.shopColorSpecial import * #Loja de cores especiais
from handlers.starRules import *
from handlers.ticketAtendimento import *
from handlers.ticketDenuncia import *
from handlers.ticketVip import *
from handlers.ticketBooster import *
from handlers.ticketParceria import *
from handlers.ticketParceriaNew import *
from handlers.ticketPatrocinio import *
from handlers.ticketMod import *
from handlers.turtle import turtle
from events.on_member_join import *
from handlers.youtube import *

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

with open("config.json", "r") as f:
    config = json.load(f)
l = open("link.json")
link = json.load(l)
starOpen = open("jsons/stars.json")
starJson = json.load(starOpen)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)
prefix = config[str("prefix")]
print(prefix)
bot = commands.Bot(command_prefix = prefix, case_insensitive = True, intents = intents)
bot.remove_command("help")

cogsPaths = []
cogs = os.listdir("commands")
for folder in cogs:
    try:
        for filename in os.listdir(f"commands/{folder}"):
            if filename.endswith(".py"):
                cogsPaths.append(f"commands.{folder}.{filename[:-3]}")
    except Exception as e:
        print(f"commands/{folder} não encontrado")

async def loadExtensions():
    for cogFile in cogsPaths:
        await bot.load_extension(cogFile)

os.chdir("./images")

@bot.event
async def on_ready():
    activity = discord.Game(name=f"{prefix}help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    welcomeChannel = bot.get_channel(982824719046832188)
    #Star Rules
    starRulesChannel = bot.get_channel(1071285010574868501)
    await starRulesLoop(bot = bot, channel = starRulesChannel)
    joinGuild = bot.get_guild(710506024489976028)
    channelGet = bot.get_channel(983902645272059964)
    synced = await bot.tree.sync()
    print(f"{len(synced)} slash commands")
    await welcomeChannel.send(content = f"**『<a:z_GreenDiamond:938880803692240927>』Olá, eu estou online!**")
    print(f"Estou pronto! Eu sou o {bot.user}")
    bot.loop.create_task(reloadServerOptions())
    bot.loop.create_task(statuschange())
    bot.loop.create_task(starRulesLoop(bot = bot, channel = starRulesChannel))
    bot.loop.create_task(editVoiceChannel(channel = channelGet, count = joinGuild.member_count))

async def reloadServerOptions():
    await getShopColor(bot = bot) # Loja de cores básicas
    await getShopColorBright(bot = bot) # Loja de cores claras
    await getShopColorDark(bot = bot) # Loja de cores escuras
    await getShopColorGray(bot = bot) # Loja de cores neutras
    await getShopColorSpecial(bot = bot) # Loja de cores especiais
    await getRegisterRow(bot = bot)
    await getTicketAtendimentoRow(bot = bot)
    await getTicketDenunciaRow(bot = bot)
    await getTicketVipRow(bot = bot)
    await getTicketBoosterRow(bot = bot)
    await getTicketPatrocinioRow(bot = bot)
    await getTicketParceriaRow(bot = bot)
    await getTicketParceriaNewRow(bot = bot)
    await getTicketModRow(bot = bot)

async def statuschange():
    activity1 = discord.Game(name=f"Oi, eu sou o Any!", type=3)
    activity2 = discord.Activity(name=f"a!stars", type=3)
    activity3 = discord.Game(name=f"a!topstars", type=3)
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
    if message.type == discord.MessageType.premium_guild_subscription:
        boosterEmbed = discord.Embed(
            title = "NOVO BOOST!!!",
            description = f"Muito obrigado por impulsionar o servidor, {message.author.mention}! Abra um ticket em <#1048659113107804260> para resgatar seus benefícios.\n\nNosso servidor agora possui **{message.guild.premium_subscription_count}** impulso(s)!",
            color = discord.Color.from_rgb(244, 127, 255)
        )
        boosterEmbed.set_author(name = "Boosts:", icon_url = "https://emoji.discadia.com/emojis/b191da2e-4bd9-4bc1-aa96-93c9b3109039.gif")
        boosterEmbed.set_thumbnail(url = message.author.display_avatar.url)
        boosterEmbed.set_image(url = "https://cdn.discordapp.com/attachments/740760158098948097/1070909269727256576/191d73a89a48d9788a56a5b9ff2db336.png")
        await message.channel.send(content = f"{message.author.mention}", embed = boosterEmbed)
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        prefix = "a!"
        if message.content == f"{prefix}turtle" or message.content == f"{prefix}tartaruga":
            await turtle(message)
        return
    if int(message.channel.id) == 1167917462516408381:
        await youtube(bot = bot, message = message)
        return
    if message.author.bot:
        return
    if message.author == bot.user:
        return
    #「R.1」Flood/spam de mensagens/emojis:
    antispam = await antiSpam(bot = bot, message = message)
    #「R.2」Mensagens desnecessariamente longas:
    antilongMessages = await antiLongMessages(bot = bot, message = message)
    #「R.11」Anti-invite:
    antiinvite = await antiInvite(bot = bot, message = message)
    afk = await searchForAfk(message)
    if afk == 0:
        afkEmbed = discord.Embed(title = "Seu AFK foi desativado!",
        color = discord.Color.from_rgb(50, 100, 255))
        afkEmbed.set_author(name = "『🔔』AFK:", icon_url = bot.user.display_avatar.url)
        afkEmbed.set_thumbnail(url = link["afkOffThumb"])
        afkDisableMsg = await message.reply(embed = afkEmbed)
        await asyncio.sleep(5)
        await afkDisableMsg.delete()
    elif afk != 1:
        afkEmbed = discord.Embed(title = "Este usuário está AFK!", description = f"**『💬』Motivo:** {afk}",
        color = discord.Color.from_rgb(50, 100, 255))
        afkEmbed.set_author(name = "『🔕』AFK:", icon_url = bot.user.display_avatar.url)
        afkEmbed.set_thumbnail(url = link["afkOnThumb"])
        afkWarnMsg = await message.reply(embed = afkEmbed)
        await asyncio.sleep(10)
        await afkWarnMsg.delete()
    try:
        await bot.process_commands(message)
        if message.channel.id in starJson["starsChannels"]:
            emj = random.randint(0, 1000)
            #print(emj)
            if emj >= 0 and emj <= 30:
                emj = 0
            elif emj >= 30 and emj <= 55:
                emj = 1
            elif emj >= 55 and emj <= 75:
                emj = 2
            elif emj >= 75 and emj <= 90:
                emj = 3
            elif emj >= 90 and emj <= 100:
                emj = 4
            if emj >= 0 and emj <= 4:
                await message.add_reaction(link["stars"]["emjs"][f"{emj}"])
    except Exception as e:
        print(e)

@bot.event
async def on_message_edit(before, after):
    try:
        if before.author.bot:
            return
        if before.author == bot.user:
            return
        antiinvite = await antiInvite(bot = bot, message = after)
        afk = await searchForAfk(before)
        print(afk == 1, afk)
        if afk == 0:
            afkEmbed = discord.Embed(title = "Seu AFK foi desativado!",
            color = discord.Color.from_rgb(50, 100, 255))
            afkEmbed.set_author(name = "『🔔』AFK:", icon_url = bot.user.display_avatar.url)
            afkEmbed.set_thumbnail(url = link["afkOffThumb"])
            afkDisableMsg = await before.reply(embed = afkEmbed)
            await asyncio.sleep(5)
            await afkDisableMsg.delete()
        elif afk != 1:
            afkEmbed = discord.Embed(title = "Este usuário está AFK!", description = f"**『💬』Motivo:** {afk}",
            color = discord.Color.from_rgb(50, 100, 255))
            afkEmbed.set_author(name = "『🔕』AFK:", icon_url = bot.user.display_avatar.url)
            afkEmbed.set_thumbnail(url = link["afkOnThumb"])
            afkWarnMsg = await before.reply(embed = afkEmbed)
            await asyncio.sleep(10)
            await afkWarnMsg.delete()
        return
    except Exception as e:
        print(e)

@bot.event
async def on_reaction_add(reaction, user):
    try:
        if user.bot:
            return
        for i in range(5):
            if str(reaction) == link["stars"]["emjs"][f"{i}"]:
                await reaction.message.clear_reactions()
                userStars = updateStar(user.id, i)
                starEmbed = discord.Embed(
                    description = f"『{link['stars']['emjs'][f'{i}']}』Parabéns {user.mention}, você pegou uma estrela e agora tem **{userStars['total'] + 1}** estrelas!",
                    color = discord.Color.from_rgb(link["stars"]["colors"][f"{i}"][0], link["stars"]["colors"][f"{i}"][1], link["stars"]["colors"][f"{i}"][2])
                )
                starEmbed.set_author(name = f"『⭐』Caça as estrelas:", icon_url = user.display_avatar.url)
                starEmbed.set_thumbnail(url = link["stars"]["thumbs"][f"{i}"])
                starEmbed.set_footer(text = f"{user.name}, use \"{prefix}stars\" para ver o seu total de estrelas!", icon_url = user.display_avatar.url)
                reactReply = await reaction.message.channel.send(embed = starEmbed)
                await asyncio.sleep(10)
                await reactReply.delete()
                return

        afk = await reactionSearchForAfk(user.id)
        if afk == 1:
            afkEmbed = discord.Embed(title = "Seu AFK foi desativado!",
            color = discord.Color.from_rgb(50, 100, 255))
            afkEmbed.set_author(name = f"『🔔』AFK de {user.name}:", icon_url = user.display_avatar.url)
            afkEmbed.set_thumbnail(url = link["afkOffThumb"])
            afkDisableMsg = await reaction.message.channel.send(embed = afkEmbed)
            await asyncio.sleep(5)
            await afkDisableMsg.delete()
        return
    except Exception as e:
        print(e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        message = await ctx.send(f"❌| {ctx.author.mention}, este comando não existe, ou foi removido!")
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
        await onMemberJoin(bot, member)
    except Exception as e:
        print(e)
    return

@bot.event
async def on_member_remove(member):
    if not member.guild.id == 710506024489976028:
        print(f"『📤』Um usuário saiu de algum servidor! {member}")
        return
    try:
        if member.guild.id == 710506024489976028:
            print(f"『📤』Um usuário saiu do servidor! {member}")
            joinGuild = bot.get_guild(member.guild.id)
            channelGet = discord.utils.get(joinGuild.channels, id = 983902645272059964)
            await channelGet.edit(name=f"『⭐』Membros: {joinGuild.member_count}")
            return
    except Exception as e:
        print(e)
        return
    return

@bot.command(name = "welcome", aliases = ["wlcm", "wlmc", "wlc"])
async def welcome(ctx, member: discord.Member = None):
    try:
        print(member)
        if member == None:
            member = ctx.author
        if member.guild.id == 710506024489976028:
            rankRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721298086166568)
            colorRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908721809883537458)
            registerRole = discord.utils.get(bot.get_guild(member.guild.id).roles, id = 908728253513080833)
            await member.add_roles(rankRole, colorRole, registerRole)
            welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
            e = random.choice(welEmjs)
            userAvatar = member.display_avatar.url
            guildMemberAdd = discord.Embed(color = 0x40e0d0)
            guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = userAvatar)
            guildMemberAdd.add_field(name = f"『{e}』 Membro novo!", value = f"**『{link['grayDiamond']}』Regras:** <#1026231571776294942>\n**『{link['greenDiamond']}』Registre-se:** <#770250817684635658>\n**『{link['redDiamond']}』Use o Janny:** <#970038786908127273>")
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
            mascara = mascara.resize(avatar.size, Image.Resampling.LANCZOS)
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

getDatabase()

async def main():
    async with bot:
        await loadExtensions()
        await bot.start(TOKEN)

asyncio.run(main())