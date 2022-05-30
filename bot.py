import discord
from discord import *
import dotenv
import datetime
from pprint import pprint
from discord_slash import SlashCommand
import random
from random import randint
from discord.ext import commands, tasks
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord_components import *
import re
import textwrap
import json
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = discord.Client()
bot = commands.Bot(command_prefix = "a!", case_insensitive = True,  intents = intents)
command_prefix = "a!"
bot.remove_command("help")

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
    
    while True:
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=activity1)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity2)
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.online, activity=activity3)
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    activity = discord.Game(name=f"a!help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Estou pronto! Eu sou o {bot.user}")
    DiscordComponents(client)
    bot.loop.create_task(statuschange())

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

@bot.command(name = "cmds", aliases = ["comandos", "commands"])
async def cmds(ctx):
        options = [ActionRow(
            Button(custom_id='mod',emoji="⚙️",style=ButtonStyle.gray),
            Button(custom_id='fun',emoji="🤣",style=ButtonStyle.gray)),
        ]
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        embed = discord.Embed(description = f"<:NarutoPaint:819963300389453874> • Oi {ctx.author.mention}, eu sou o **AnyBot**. Estou aqui para divertir você(s). Meu prefixo padrão é `a!`, e meu prefixo neste servidor é `{command_prefix}`\n<:SakuraPaint:820513193260089365> • Gostaria de sugerir algum comando para mim? Entre em contato com o meu criador: `Eric2605#9133`\n<:ShikamaruPaint:820479198211997716> • Atualmente eu tenho **125** comandos. Digite `{command_prefix}comandos` para ver os meus comandos.",color = 0x2dffe7)
        embed.set_author(name = f"Central de Ajuda do {bot.user.name}", icon_url=bot.user.avatar_url)
        embed.set_footer(text="• Para obter informações de cada comando, digite a!help <comando>")
        embed.add_field(name="Categorias:", value="```fix\nMod - Fun - NSFW - Util - Photoshop - Diversos - Jogos\n```", inline=True)
        embed.add_field(name="Extras:", value="**[Meu servidor](https://discord.gg/77ax3PyXgn) | [Canal YT](https://www.youtube.com/channel/UCoo5WAMn4tMl-b0lW0KL9Ug) | [Vote](https://top.gg/bot/900346730237820939/vote)**", inline=False)
        embed.set_thumbnail(url=bot.user.avatar_url)
        print(f'{command_prefix}cmds')
        await ctx.reply(embed = embed, components = options)

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)