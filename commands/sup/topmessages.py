import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
import textwrap
from io import BytesIO

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

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

TOPMSG_EMOJIS = ["🥇", "🥈", "🥉", "🔷", "🔷"]
topMsgUsers = []

bot.ses = aiohttp.ClientSession()
class cop_topMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "topmessages", aliases = ["topmsg", "topmgs", "msgtop", "tm", "topm"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def topMessages(self, ctx, channel: discord.TextChannel = None):
        try:
            if channel == None:
                channel = ctx.channel
            topMessagesStandardEmbed = discord.Embed(
                title = f"**<:c_YellowDima:1070043505365352578> __TOP MENSAGENS__ <:c_YellowDima:1070043505365352578>**",
                color = discord.Color.from_rgb(255, 200, 0)
            )
            topMessagesStandardEmbed.set_footer(text = "Top Mensagens", icon_url = self.bot.user.display_avatar.url)
            await ctx.channel.send(embed = topMessagesStandardEmbed, view = topMsgSettingsButtons(self.bot, channel, topMessagesStandardEmbed))
            return
        except Exception as e:
            print(e)

    @topMessages.error
    async def topMessages_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)

class topMsgSettingsButtons(discord.ui.View):
    def __init__(self, bot, channel, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.channel = channel
        self.embed = embed

    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"➕")
    async def topMsgAddOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(topMsgModal(self.bot, self.channel, self.embed))
        except Exception as e:
            print(e)
    
    @discord.ui.button(style = discord.ButtonStyle.red, emoji = f"➖")
    async def topMsgRemoveOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if not len(topMsgUsers) >= 1:
                await interaction.response.send_message(content = "『❌』Não há nenhum usuário no ranking!", ephemeral = True)
                return
            await interaction.response.defer()
            topMsgUsers.pop()
            self.embed.remove_field(index = len(topMsgUsers))
            await interaction.message.edit(embeds = [self.embed], view= topMsgSettingsButtons(self.bot, self.channel, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(style = discord.ButtonStyle.green, emoji = f"✅")
    async def topMsgSendOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(topMsgUsers) < 3:
            await interaction.response.send_message(content = "『❌』É preciso ter pelo menos 3 usuários para montar o Top Chat!", ephemeral = True)
            return
        loadingEmbed = discord.Embed(
                description = "Carregando...",
                color = discord.Color.from_rgb(100, 100, 100)
            )
        await interaction.message.delete()
        loadingMsg = await interaction.channel.send(embed = loadingEmbed, view = None)
        try:
            await interaction.response.defer()
            user0Avatar = topMsgUsers[0].display_avatar.url
            user1Avatar = topMsgUsers[1].display_avatar.url
            user2Avatar = topMsgUsers[2].display_avatar.url
            url0 = requests.get(user0Avatar)
            url1 = requests.get(user1Avatar)
            url2 = requests.get(user2Avatar)
            avatar0 = Image.open(BytesIO(url0.content))
            avatar1 = Image.open(BytesIO(url1.content))
            avatar2 = Image.open(BytesIO(url2.content))
            avatar0 = avatar0.resize((234, 231))
            avatar1 = avatar1.resize((182, 180))
            avatar2 = avatar2.resize((171, 169))
            bigavatar0 = (avatar0.size[0] * 3, avatar0.size[1] * 3)
            bigavatar1 = (avatar1.size[0] * 3, avatar1.size[1] * 3)
            bigavatar2 = (avatar2.size[0] * 3, avatar2.size[1] * 3)
            mascara0 = Image.new('L', bigavatar0, 0)
            mascara1 = Image.new('L', bigavatar1, 0)
            mascara2 = Image.new('L', bigavatar2, 0)
            recortar0 = ImageDraw.Draw(mascara0)
            recortar1 = ImageDraw.Draw(mascara1)
            recortar2 = ImageDraw.Draw(mascara2)
            recortar0.ellipse((0, 0) + bigavatar0, fill=255)
            recortar1.ellipse((0, 0) + bigavatar1, fill=255)
            recortar2.ellipse((0, 0) + bigavatar2, fill=255)
            mascara0 = mascara0.resize(avatar0.size, Image.ANTIALIAS)
            mascara1 = mascara0.resize(avatar1.size, Image.ANTIALIAS)
            mascara2 = mascara0.resize(avatar2.size, Image.ANTIALIAS)
            avatar0.putalpha(mascara0)
            avatar1.putalpha(mascara1)
            avatar2.putalpha(mascara2)
            saida0 = ImageOps.fit(avatar0, mascara0.size, centering=(0.5, 0.5))
            saida1 = ImageOps.fit(avatar1, mascara1.size, centering=(0.5, 0.5))
            saida2 = ImageOps.fit(avatar2, mascara2.size, centering=(0.5, 0.5))
            saida0.putalpha(mascara0)
            saida1.putalpha(mascara1)
            saida2.putalpha(mascara2)
            #saida.save('img_avatar.png')
            img = Image.open("img_topchat(2).png")
            imgBase = Image.open("img_topchat(1).png")
            fonte = ImageFont.truetype("font_coolvetica_rg.ttf", 35)
            img.paste(avatar0, (383, 185), avatar0)
            img.paste(avatar1, (183, 264), avatar1)
            img.paste(avatar2, (639, 300), avatar2)
            img.paste(imgBase, (0, 0), imgBase)
            img.save("img_topchat.png")
            self.embed.set_image(url = "attachment://img_topchat.png")
            await self.channel.send(embeds = [self.embed], file = discord.File("img_topchat.png"))
        except Exception as e:
            loadingEmbed.color = discord.Color.from_rgb(255, 20, 20)
            loadingEmbed.title = "Erro:"
            loadingEmbed.description = f"{e}"
            await loadingMsg.edit(embed = loadingEmbed)
            print(e)
            return
        await loadingMsg.delete()

class topMsgModal(discord.ui.Modal, title = "Editar top mensagens"):
    def __init__(self, bot, channel, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.channel = channel
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = f"Adicionar usuário:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
        self.add_item(discord.ui.TextInput(
            label = f"Mensagens enviadas:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            userInput = self.children[0].value
            msgInput = self.children[1].value
            user = await self.bot.fetch_user(userInput)
            if user in topMsgUsers:
                await interaction.response.send_message(content = "『❌』Este usuário já está no ranking!", ephemeral = True)
                return
            await interaction.response.defer()
            if len(topMsgUsers) >= len(TOPMSG_EMOJIS):
                topEmj = "🔶"
            else:
                topEmj = TOPMSG_EMOJIS[len(topMsgUsers)]
            self.embed.add_field(name = f"『{topEmj}』{user.name}", value = f"**{msgInput}** mensagens.", inline = False)
            topMsgUsers.append(user)
            await interaction.message.edit(embeds = [self.embed], view = topMsgSettingsButtons(self.bot, self.channel, self.embed))
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}topmessages")
    await bot.add_cog(cop_topMessages(bot))