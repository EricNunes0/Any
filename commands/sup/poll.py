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

class pollSettingsButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot
    
    @discord.ui.button(label = "Adicionar opção", style = discord.ButtonStyle.blurple, emoji = f"➕")
    async def ticketsEditAmetista(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ticketVipAmetistaModal())
        except Exception as e:
            print(e)

class ticketVipAmetistaModal(discord.ui.Modal, title = "Tickets Ametista"):
    def __init__(self):
        super().__init__(timeout = None)

        self.add_item(discord.ui.TextInput(
            label="Tickets Ametista",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        setAmetista = self.children[0].value
        setAmetista = int(setAmetista)
        print(setAmetista)
        embed = discord.Embed(
            title = "Tickets alterados!",
            color = discord.Color.from_rgb(175, 80, 240)
        )
        embed.add_field(name = "『<a:ab_PurpleDiamond:938883672717787196>』Tickets Ametista:", value = setAmetista)
        await interaction.response.send_message(embeds = [embed], ephemeral = False)

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

bot.ses = aiohttp.ClientSession()
class cog_poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "poll", aliases = ["votação"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def poll(self, ctx):
        try:
            ticketsEmbed = discord.Embed(
                color = discord.Color.from_rgb(200, 200, 200)
            )
            ticketsEmbed.set_author(name = f"『🗳』Iniciar votação:", icon_url = self.bot.user.display_avatar.url)
            await ctx.reply(embed = ticketsEmbed, view = pollSettingsButtons(self.bot))
            return
        except Exception as e:
            print(e)

    @poll.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}poll")
    await bot.add_cog(cog_poll(bot))