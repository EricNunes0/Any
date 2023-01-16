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
from handlers.rules import *
from handlers.register import *

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
    synced = await bot.tree.sync()
    print(f"{len(synced)} slash commands")
    await welcomeChannel.send(content = f"**『<a:z_GreenDiamond:938880803692240927>』Olá, eu estou online!**")
    print(f"Estou pronto! Eu sou o {bot.user}")
    bot.loop.create_task(statuschange())

async def statuschange():
    activity1 = discord.Game(name=f"Oi, eu sou o Any!", type=3)
    activity2 = discord.Activity(name=f"a!stars", type=3)
    activity3 = discord.Game(name=f"a!topstars", type=3)
    activity4 = discord.Game(name=f"Janny City Adventures", type=3)
    activity5 = discord.Activity(name=f"vocês :)", type = 3)
    
    while True:
        await getRuleRow(bot = bot)
        await getRegisterRow(bot = bot)
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
    if message.author.bot:
        return
    if message.author == bot.user:
        return
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
                    description = f"『{link['stars']['emjs'][f'{i}']}』Parabéns {user.mention}, você conseguiu uma estrela e agora tem **{userStars['total'] + 1}** estrelas!",
                    color = discord.Color.from_rgb(link["stars"]["colors"][f"{i}"][0], link["stars"]["colors"][f"{i}"][1], link["stars"]["colors"][f"{i}"][2])
                )
                starEmbed.set_author(name = f"『⭐』Caça as estrelas:", icon_url = user.display_avatar.url)
                starEmbed.set_thumbnail(url = link["stars"]["thumbs"][f"{i}"])
                starEmbed.set_footer(text = f"{user.name}, use \"{prefix}stars\" para ver o seu total de estrelas!", icon_url = user.display_avatar.url)
                reactReply = await reaction.message.channel.send(embed = starEmbed)
                await asyncio.sleep(10)
                await reactReply.delete()
                print("Estrela desativada")
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
    guildToJoinId = 710506024489976028
    sendWelcomeChannelId = 723155037332832296
    editChannelNameId = 983902645272059964
    if not member.guild.id == guildToJoinId:
        print(f"『📤』Um usuário entrou em algum servidor! {member}")
        return
    try:
        if member.guild.id == guildToJoinId:
            print(f"『📤』Um usuário entrou no servidor! {member}")
            joinGuild = bot.get_guild(guildToJoinId)
            channelGet = discord.utils.get(joinGuild.channels, id = editChannelNameId)
            await channelGet.edit(name=f"『🌟』Membros: {joinGuild.member_count}")
            welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
            e = random.choice(welEmjs)
            guildMemberAdd = discord.Embed(title = f"{e} Seja bem-vindo(a)! {e}", color = 0x4070e0)
            guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.display_avatar.url)
            guildMemberAdd.add_field(name = f"〔⏬〕Confira:", value = f"**『{link['grayDiamond']}』Regras:** <#1064003850228473876>\n**『{link['greenDiamond']}』Registre-se:** <#770250817684635658>\n**『{link['redDiamond']}』Use o Janny:** <#970038786908127273>")
            guildMemberAdd.set_thumbnail(url = member.display_avatar.url)
            guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = member.display_avatar.url)
            welcomeChannel = bot.get_channel(sendWelcomeChannelId)
            await welcomeChannel.send(content = member.mention, embed = guildMemberAdd)
            print("Membro entrou com sucesso")
            return
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