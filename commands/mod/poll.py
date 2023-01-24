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

POLL_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

pollsOptionsTexts = []
totalPolls = [
    [], [], [], [], []
]

bot.ses = aiohttp.ClientSession()
class cog_pollVotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "poli", aliases = ["votação"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def poll(self, ctx, channel: discord.TextChannel = None):
        try:
            pollsOptionsTexts.clear()
            for totalPoll in totalPolls:
                totalPoll.clear()
            if channel == None:
                channel = ctx.channel
            pollStandardEmbed = discord.Embed(
                color = discord.Color.from_rgb(20, 90, 255)
            )
            pollStandardEmbed.set_author(name = f"『🗳』Votação:", icon_url = self.bot.user.display_avatar.url)
            await ctx.channel.send(embed = pollStandardEmbed, view = pollSettingsButtons(self.bot, pollStandardEmbed))
            return
        except Exception as e:
            print(e)

    @poll.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)

class pollSettingsButtons(discord.ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
    
    @discord.ui.button(label = "Adicionar opção", style = discord.ButtonStyle.blurple, emoji = f"➕")
    async def pollAddOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(pollModal(self.bot, self.embed))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Remover opção", style = discord.ButtonStyle.red, emoji = f"➖")
    async def pollRemoveOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer()
            if len(pollsOptionsTexts) >= 1:
                pollsOptionsTexts.pop()
            self.embed.remove_field(index = len(pollsOptionsTexts))
            await interaction.message.edit(embeds = [self.embed], view= pollSettingsButtons(self.bot, self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Iniciar votação", style = discord.ButtonStyle.green, emoji = f"🗳")
    async def pollSendOption(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if len(pollsOptionsTexts) < 2:
                await interaction.response.send_message(content = "Escolha pelo menos 2 opções!", ephemeral = True)
                return
            await interaction.response.defer()
            await interaction.message.delete()
            pollStartedEmbed = discord.Embed(
                color = discord.Color.from_rgb(20, 90, 255)
            )
            pollStartedEmbed.set_author(name = f"『🗳』Votação:", icon_url = self.bot.user.display_avatar.url)
            for pollOptionText in pollsOptionsTexts:
                pollStartedEmbed.add_field(name = pollOptionText, value = f"`{len(totalPolls[pollsOptionsTexts.index(pollOptionText)])} votos`", inline = False)
            pollMsg = await interaction.channel.send(embeds = [pollStartedEmbed], view = poll2Options(pollStartedEmbed))
            await asyncio.sleep(60)
            for pollOptionText in pollsOptionsTexts:
                pollStartedEmbed.set_field_at(index = pollsOptionsTexts.index(pollOptionText), name = pollOptionText, value = f"`{len(totalPolls[pollsOptionsTexts.index(pollOptionText)])} votos`", inline = False)
            pollStartedEmbed.set_thumbnail(url = link["blueChecked"])
            pollStartedEmbed.set_footer(text = "Votação encerrada!", icon_url = self.bot.user.display_avatar.url)
            await pollMsg.edit(embeds = [pollStartedEmbed], view = None)
            pollsOptionsTexts.clear()
            for totalPoll in totalPolls:
                totalPoll.clear()
        except Exception as e:
            print(e)

class pollModal(discord.ui.Modal, title = "Criar votação"):
    def __init__(self, bot, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = f"Opção:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            pollName = self.children[0].value
            self.embed.add_field(name = f"『{POLL_EMOJIS[len(pollsOptionsTexts)]}』{pollName}", value = f"`0 votos`", inline = False)
            pollsOptionsTexts.append(pollName)
            await interaction.message.edit(embeds = [self.embed], view = pollSettingsButtons(self.bot, self.embed))
        except Exception as e:
            print(e)

class poll2Options(discord.ui.View):
    def __init__(self, embed):
        super().__init__(timeout = None)
        self.embed = embed
    
    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"{POLL_EMOJIS[0]}")
    async def poll1Option(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            for totalPoll in totalPolls:
                if interaction.user.id in totalPoll:
                    await interaction.response.send_message(content = "Você já votou!", ephemeral = True)
                    return
            await interaction.response.defer()
            totalPolls[0].append(interaction.user.id)
            self.embed.set_field_at(index = 0, name = pollsOptionsTexts[0], value = f"`{len(totalPolls[0])} votos`", inline = False)
            await interaction.message.edit(embeds = [self.embed])
            return
        except Exception as e:
            print(e)

    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"{POLL_EMOJIS[1]}")
    async def poll2Option(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            for totalPoll in totalPolls:
                if interaction.user.id in totalPoll:
                    await interaction.response.send_message(content = "Você já votou!", ephemeral = True)
                    return
            await interaction.response.defer()
            totalPolls[1].append(interaction.user.id)
            self.embed.set_field_at(index = 1, name = pollsOptionsTexts[1], value = f"`{len(totalPolls[1])} votos`", inline = False)
            await interaction.message.edit(embeds = [self.embed])
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"{prefix}poll")
    await bot.add_cog(cog_pollVotes(bot))