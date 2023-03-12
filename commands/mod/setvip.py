import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from mongoconnection.star import *

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

def convertTime(arg0, arg1 = None):
    arg0 = arg0.lower()
    if arg1 == None:
        if arg0.endswith("s") or arg0.endswith("m") or arg0.endswith("h") or arg0.endswith("d"):
            t = arg0[:-1]
            t = int(t)
            print(t)
            if arg0.endswith("s"):
                c = t
            if arg0.endswith("m"):
                c = t * 60
            if arg0.endswith("h"):
                c = t * 3600
            if arg0.endswith("d"):
                c = t * (3600 * 24)
            return c
        else:
            return int(arg0)

class setVipForm1(discord.ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
    
    @discord.ui.button(label = f"Usuário", style = discord.ButtonStyle.blurple, emoji = "👤")
    async def setvipAnswer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(setVipModal1(self.bot, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip1Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[0].value == "`Não informado`":
                setvipMissingEmbed1 = discord.Embed(
                    description = "Informe o usuário!",
                    color = discord.Color.from_rgb(220, 20, 255)
                )
                await interaction.response.send_message(embed = setvipMissingEmbed1, ephemeral = True)
                return
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm2(self.bot, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm2(discord.ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
    
    @discord.ui.button(label = f"Ametista", style = discord.ButtonStyle.blurple, emoji = "<a:ab_PurpleDiamond:938883672717787196>")
    async def setvip2Option1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 1, name = "『<a:ab_PurpleDiamond:938883672717787196>』VIP selecionado:", value = f"`{vipNames[0]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Jade", style = discord.ButtonStyle.blurple, emoji = "<a:ab_GreenDiamond:938880803692240927>")
    async def setvip2Option2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 1, name = "『<a:ab_GreenDiamond:938880803692240927>』VIP selecionado:", value = f"`{vipNames[1]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Safira", style = discord.ButtonStyle.blurple, emoji = "<a:ab_BlueDiamond:938850305083314207>")
    async def setvip2Option3(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 1, name = "『<a:ab_BlueDiamond:938850305083314207>』VIP selecionado:", value = f"`{vipNames[2]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm3(discord.ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
    
    @discord.ui.button(label = f"Duração", style = discord.ButtonStyle.blurple, emoji = "⏰")
    async def setvip3Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(setVipModal3(self.bot, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip3Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[2].value == "`Não informado`":
                setvipMissingEmbed1 = discord.Embed(
                    description = "Informe a duração!",
                    color = discord.Color.from_rgb(220, 20, 255)
                )
                await interaction.response.send_message(embed = setvipMissingEmbed1, ephemeral = True)
                return
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = None)
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip3Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipModal1(discord.ui.Modal, title = "Configurar VIP:"):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = "ID do usuário:",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 50,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            answer0 = self.children[0].value
            user = await self.bot.fetch_user(answer0)
            self.embed.set_field_at(index = 0, name = "『👤』Usuário:", value = f"{user.mention} `({user.id})`", inline = False)
        except Exception as e:
            print(e)
            self.embed.set_field_at(index = 0, name = "『👤』Usuário:", value = f"`Não informado`", inline = False)
        await interaction.message.edit(embeds = [self.embed])

class setVipModal3(discord.ui.Modal, title = "Editar duração:"):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = f"Duração (s/m/h/d):",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            time = self.children[0].value
            self.time = convertTime(time)
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            print(timeStamp)
            await interaction.response.send_message(content = f"Duração alterada para {self.time} segundos!", ephemeral = True)
            self.embed.set_field_at(index = 2, name = "『⏰』Duração:", value = f"{time} (<t:{int((timeStamp)) + self.time}>)", inline = False)
            await interaction.message.edit(embeds = [self.embed], view = setVipForm3(self.bot, self.embed))
        except Exception as e:
            print(e)


bot.ses = aiohttp.ClientSession()
class cog_setVip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "setvip", aliases = ["addvip", "vipset", "vipadd"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def setvip(self, ctx, *, user: discord.User = None):
        try:
            setVipEmbed = discord.Embed(
                color = discord.Color.from_rgb(200, 20, 255)
            )
            setVipEmbed.set_author(name = f"『💎』Configurar VIP:", icon_url = self.bot.user.display_avatar.url)
            setVipEmbed.add_field(name = f"『👤』Usuário:", value = f"`Não informado`", inline = False)
            setVipEmbed.add_field(name = f"『💎』VIP selecionado:", value = f"`Não informado`", inline = False)
            setVipEmbed.add_field(name = f"『⏰』Duração:", value = f"`Não informado`", inline = False)
            setVipEmbed.add_field(name = f"『💼』Cargo próprio:", value = f"`Não informado`", inline = False)
            setVipEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.reply(embed = setVipEmbed, view = setVipForm1(self.bot, setVipEmbed))
            return
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}stars")
    await bot.add_cog(cog_setVip(bot))