import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from mongoconnection.ticket import *

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

class ticketButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot
    
    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"{link['purpleDiamond']}")
    async def ticketsEditAmetista(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ticketVipAmetistaModal())
        except Exception as e:
            print(e)
    
    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"🙋")
    async def ticketsEditAtendimento(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ticketAtendimentoModal())
        except Exception as e:
            print(e)

    @discord.ui.button(style = discord.ButtonStyle.blurple, emoji = f"🚔")
    async def ticketsEditDenuncia(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ticketDenunciaModal())
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
        setVipAmetistaStats(int(self.children[0].value))
        await interaction.response.send_message(embeds = [embed], ephemeral = False)

class ticketAtendimentoModal(discord.ui.Modal, title = "Tickets Atendimento"):
    def __init__(self):
        super().__init__(timeout = None)

        self.add_item(discord.ui.TextInput(
            label="Tickets Atendimento",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        setAtendimento = self.children[0].value
        setAtendimento = int(setAtendimento)
        print(setAtendimento)
        embed = discord.Embed(
            title = "Tickets alterados!",
            color = discord.Color.from_rgb(210, 50, 50)
        )
        embed.add_field(name = "『🙋』Tickets Atendimento:", value = setAtendimento)
        setAtendimentoStats(int(self.children[0].value))
        await interaction.response.send_message(embeds = [embed], ephemeral = False)

class ticketDenunciaModal(discord.ui.Modal, title = "Tickets Denúncia"):
    def __init__(self):
        super().__init__(timeout = None)

        self.add_item(discord.ui.TextInput(
            label="Tickets Denúncia",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        setDenuncia = self.children[0].value
        setDenuncia = int(setDenuncia)
        print(setDenuncia)
        embed = discord.Embed(
            title = "Tickets alterados!",
            color = discord.Color.from_rgb(20, 20, 60)
        )
        embed.add_field(name = "『🚔』Tickets Denúncia:", value = setDenuncia)
        setDenunciaStats(int(self.children[0].value))
        await interaction.response.send_message(embeds = [embed], ephemeral = False)

bot.ses = aiohttp.ClientSession()
class cog_tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "tickets", aliases = ["ticket", "alltickets"], pass_context = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def tickets(self, ctx):
        try:
            ticketsStats = getTicketVipStats()
            print(ticketsStats)
            ticketsEmbed = discord.Embed(
                color = discord.Color.from_rgb(200, 200, 200)
            )
            ticketsEmbed.set_author(name = f"『🎫』Tickets criados ({ticketsStats['Total']}):", icon_url = self.bot.user.display_avatar.url)
            ticketsEmbed.add_field(name = f"『💎』Vips:", value = f"**{ticketsStats['Vips']}**", inline = True)
            ticketsEmbed.add_field(name = f"『🔮』Boost:", value = f"**{ticketsStats['Boost']}**", inline = True)
            ticketsEmbed.add_field(name = f"『🚀』Patrocinador:", value = f"**{ticketsStats['Patrocinio']}**", inline = True)
            ticketsEmbed.add_field(name = f"『{link['purpleDiamond']}』Ametista:", value = f"**{ticketsStats['VipAmetista']}**", inline = True)
            ticketsEmbed.add_field(name = f"『{link['greenDiamond']}』Jade:", value = f"**{ticketsStats['VipJade']}**", inline = True)
            ticketsEmbed.add_field(name = f"『{link['blueDiamond']}』Safira:", value = f"**{ticketsStats['VipSafira']}**", inline = True)
            ticketsEmbed.add_field(name = f"『🙋』Atendimento:", value = f"**{ticketsStats['Atendimento']}**", inline = True)
            ticketsEmbed.add_field(name = f"『🚔』Denúncia:", value = f"**{ticketsStats['Denuncia']}**", inline = True)
            ticketsEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            await ctx.reply(embed = ticketsEmbed, view = ticketButtons(self.bot))
            return
        except Exception as e:
            print(e)
    
async def setup(bot):
    print(f"{prefix}tickets")
    await bot.add_cog(cog_tickets(bot))