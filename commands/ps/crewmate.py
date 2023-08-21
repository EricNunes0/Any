import discord
from discord.ext import commands
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json
import textwrap
import random

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
now = now.strftime("%d/%m/%Y - %H:%M:%S")


class cog_crewmate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "crewmate", aliases = ["crewmates","tripulante","tripulantes"])
    @cooldown(1, 5, type = commands.BucketType.user)
    async def crewmate(self, ctx, member1:discord.Member = None, member2:discord.Member = None, member3:discord.Member = None, member4:discord.Member = None, member5:discord.Member = None, member6:discord.Member = None, member7:discord.Member = None, member8:discord.Member = None, member9:discord.Member = None):
        try:
            members = []
            for member in ctx.guild.members:
                members.append(member)

            if member1 == None:
                member1 = random.choice(members)
            if member2 == None:
                member2 = random.choice(members)
            if member3 == None:
                member3 = random.choice(members)
            if member4 == None:
                member4 = random.choice(members)
            if member5 == None:
                member5 = random.choice(members)
            if member6 == None:
                member6 = random.choice(members)
            if member7 == None:
                member7 = random.choice(members)
            if member8 == None:
                member8 = random.choice(members)
            if member9 == None:
                member9 = random.choice(members)

            url1 = requests.get(member1.display_avatar.url)
            url2 = requests.get(member2.display_avatar.url)
            url3 = requests.get(member3.display_avatar.url)
            url4 = requests.get(member4.display_avatar.url)
            url5 = requests.get(member5.display_avatar.url)
            url6 = requests.get(member6.display_avatar.url)
            url7 = requests.get(member7.display_avatar.url)
            url8 = requests.get(member8.display_avatar.url)
            url9 = requests.get(member9.display_avatar.url)
            avatar1 = Image.open(BytesIO(url1.content))
            avatar1 = avatar1.resize((70,70))
            avatar2 = Image.open(BytesIO(url2.content))
            avatar2 = avatar2.resize((80,80))
            avatar3 = Image.open(BytesIO(url3.content))
            avatar3 = avatar3.resize((90,90))
            avatar4 = Image.open(BytesIO(url4.content))
            avatar4 = avatar4.resize((105,105))
            avatar5 = Image.open(BytesIO(url5.content))
            avatar5 = avatar5.resize((145,145))
            avatar6 = Image.open(BytesIO(url6.content))
            avatar6 = avatar6.resize((105,105))
            avatar7 = Image.open(BytesIO(url7.content))
            avatar7 = avatar7.resize((90,90))
            avatar8 = Image.open(BytesIO(url8.content))
            avatar8 = avatar8.resize((80,80))
            avatar9 = Image.open(BytesIO(url9.content))
            avatar9 = avatar9.resize((70,70))    

            backgroundImage = requests.get("https://cdn.discordapp.com/attachments/1141841573039054920/1142966645439086623/img_crewmate.png")
            img = Image.open(BytesIO(backgroundImage.content))
            img.paste(avatar1, (274, 585)) #Rosa
            img.paste(avatar2, (370, 615)) #Branco
            img.paste(avatar3, (505, 625)) #Azul Escuro
            img.paste(avatar4, (665, 645)) #Marrom
            img.paste(avatar5, (840, 655)) #Preto
            img.paste(avatar6, (1020, 645)) #Vermelho
            img.paste(avatar7, (1200, 625)) #Verde
            img.paste(avatar8, (1340, 618)) #Amarelo
            img.paste(avatar9, (1440, 585)) #Roxo
            img.save('img_crewmate.png')
            psEmbed = discord.Embed(color = discord.Color.from_rgb(255, 100, 20))
            psEmbed.set_image(url = "attachment://img_crewmate.png")
            psEmbed.set_author(name = f"『🛸』Crewmate:", icon_url = self.bot.user.display_avatar.url)
            psEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.send(embed = psEmbed, file=discord.File('img_crewmate.png'))
        except Exception as e:
            print(e)

    
async def setup(bot):
    print("cog_crewmate.py loaded")
    await bot.add_cog(cog_crewmate(bot))