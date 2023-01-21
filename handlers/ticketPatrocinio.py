import discord
import json
import random
import asyncio
from mongoconnection.ticket import *

class ticketClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Patrocinar sorteio", style = discord.ButtonStyle.green, emoji = "🚀")
    async def ticketPatrocinadorInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🚀』{interaction.user.name} `({interaction.user.id})` abriu um ticket para patrocinador!")
        ticketEmbed = discord.Embed(
            title = f"꧁🚀 Seja Patrocinador 🚀꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(20, 175, 20)
        )
        ticketEmbed.set_footer(text = "Seja Patrocinador!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketPatrocinadorYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 1066082691843362917)
            ticketStats = getTicketVipStats()
            channelName = f"『🚀』・✧patrocinio-{int(ticketStats['Patrocinio']) + 1}✧"
            updateTicketPatrocinioStats()
            ticketChannel = await interaction.guild.create_text_channel(
                name = channelName,
                topic = f"Pedido de {interaction.user.name} ({interaction.user.id})",
                category = ticketCategorie
            )
            serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            serverOverwrites.read_messages, serverOverwrites.send_messages = False, False
            await ticketChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await ticketChannel.set_permissions(interaction.user, overwrite = userOverwrites)
            ticketOpenedEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket aberto! Faça seu pedido em {ticketChannel.mention}",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            ticketOpenedEmbed.set_footer(text = "Seja Patrocinador!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Para ver todos os benefícios de se tornar um patrocinador, acesse <#1049407713488146464>\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            ticketEmbed.set_footer(text = f"Ticket de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:ab_GreenDiamond:938880803692240927>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250>||", embed = ticketEmbed, view = ticketCloseClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketPatrocinadorNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            ticketEmbed.set_footer(text = "Seja Patrocinador!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
            return
        except Exception as e:
            print(e)

class ticketCloseClass(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Fechar ticket", style = discord.ButtonStyle.gray, emoji = "<:d_Vazando:1057493788551028878>")
    async def ticketPatrocinadorCloseInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🚀』{interaction.user.mention} `({interaction.user.id})` fechou um ticket para patrocinador!")
        ticketCloseEmbed = discord.Embed(
            title = f"꧁🚀 Seja Patrocinador 🚀꧂",
            description = f"{interaction.user.mention}, você tem certeza que deseja fechar este ticket?",
            color = discord.Color.from_rgb(20, 175, 20)
        )
        ticketCloseEmbed.set_footer(text = "Seja Patrocinador!")
        await interaction.response.send_message(embed = ticketCloseEmbed, view = ticketCancelConfirm(self.bot, self.json, self.user), ephemeral = True)

class ticketCancelConfirm(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketPatrocinadorCloseYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketClosedEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket fechado!",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            ticketClosedEmbed.set_footer(text = "Seja Patrocinador!")
            await interaction.response.edit_message(embed = ticketClosedEmbed, view = None)
            ticketClosedMsgEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket fechado por {interaction.user.mention}!",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            await interaction.channel.send(embed = ticketClosedMsgEmbed, view = ticketReopen(self.bot, self.json, self.user))
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketPatrocinadorNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket reaberto!",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            ticketEmbed.set_footer(text = "Seja Patrocinador!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
            return
        except Exception as e:
            print(e)

class ticketReopen(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Abrir ticket", style = discord.ButtonStyle.green, emoji = "🔓")
    async def ticketPatrocinadorReopenInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketReopenedEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『🎫』Ticket aberto por {interaction.user.mention}!",
                color = discord.Color.from_rgb(20, 175, 20)
            )
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketReopenedEmbed)
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Excluir", style = discord.ButtonStyle.red, emoji = "💣")
    async def ticketPatrocinadorNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketDeleteEmbed = discord.Embed(
                title = f"꧁🚀 Seja Patrocinador 🚀꧂",
                description = f"『💥』Este ticket será excluído em 3, 2, 1...!",
                color = discord.Color.from_rgb(255, 70, 20)
            )
            ticketDeleteEmbed.set_image(url = "https://media.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
            ticketDeleteEmbed.set_footer(text = "Seja Patrocinador!")
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketDeleteEmbed, view = None)
            await asyncio.sleep(3)
            await interaction.channel.delete(
                reason = "Ticket excluído!"
            )
            return
        except Exception as e:
            print(e)

async def getTicketPatrocinioRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["patrocinioChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["patrocinioTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> Seja Patrocinador <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
*Seja um <@&1047161198682067034> do servidor e nos ajude com o crescimento dele. Você pode patrocinar o seu próprio sorteio, e além de conseguir benefícios com os requisitos, você irá ajudar para que o servidor tenha sorteios frequentes.*
""",
            color = discord.Color.from_rgb(20, 175, 20)
        )
        ticketMenuEmbed.add_field(name = "『<:JannyCoin:969659132913274910>』Requisitos Moedas do Janny:", inline = False, value =
"""
➺ Reputação 4h - 5M
➺ Reputação 6h - 10M
➺ Reputação 8h - 15M

➺ Entrar em Servidor 4h - 5M
➺ Entrar em Servidor 6h - 10M
➺ Entrar em Servidor 8h - 15M
"""
        )
        ticketMenuEmbed.add_field(name = "『☁』Requisitos Sonhos:", inline = False, value =
"""
➺ Reputação 4h - 100k
➺ Reputação 6h - 150k
➺ Reputação 8h - 200k

➺ Entrar em Servidor 4h - 150k
➺ Entrar em Servidor 6h - 200k
➺ Entrar em Servidor 8h - 250k
"""
        )
        ticketMenuEmbed.add_field(name = "『<a:ab_LevelUp:1051238478089822241>』Vantagens:", inline = False, value =
"""
➺ Cargo destacado na lateral do servidor <@&1047161198682067034>
➺ 1 hora de tempo para claim nos sorteios
➺ XP Loritta: **1.5x**
"""
        )
        ticketMenuEmbed.add_field(name = "『⚠』Atenção:", inline = False, value =
"""
➺ Não marcamos @everyone, apenas <@&1047164668088688700>
➺ Podemos analisar pedidos para outros requisitos ou pagamentos com moeda de outros bots
"""
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/tbd7xhv.png")
        ticketMenuEmbed.set_footer(text = "Seja Patrocinador", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)