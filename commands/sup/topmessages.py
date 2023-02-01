import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp

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
        try:
            await interaction.response.defer()
            await interaction.message.delete()
            await self.channel.send(embeds = [self.embed])
            
        except Exception as e:
            print(e)

class topMsgModal(discord.ui.Modal, title = "Editar votação"):
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