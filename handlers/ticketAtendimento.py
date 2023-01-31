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
    
    @discord.ui.button(label = f"Abrir ticket", style = discord.ButtonStyle.gray, emoji = "🎫")
    async def ticketPatrocinadorInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🙋』{interaction.user.name} `({interaction.user.id})` abriu um ticket para o atendimento!")
        ticketEmbed = discord.Embed(
            title = f"꧁🙋 Atendimento 🙋꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(210, 50, 50)
        )
        ticketEmbed.set_footer(text = "Atendimento!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketPatrocinadorYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 736637479616118857)
            ticketStats = getTicketVipStats()
            channelName = f"『🎫』・✧atendimento-{int(ticketStats['Atendimento']) + 1}✧"
            channelTopic = f"Atendimento para {interaction.user.id}"
            for channel in interaction.guild.text_channels:
                if channel.topic == channelTopic:
                    parceriaAlreadyOpenedEmbed = discord.Embed(
                        title = f"꧁🙋 Atendimento 🙋꧂",
                        description = f"『📃』Você possui um canal de atendimento aberto: {channel.mention}! Caso não consiga visualizar, entre em contato com um administrador.",
                        color = discord.Color.from_rgb(210, 50, 50)
                    )
                    parceriaAlreadyOpenedEmbed.set_footer(text = "Atendimento!")
                    await interaction.response.edit_message(embed = parceriaAlreadyOpenedEmbed, view = None)
                    return
            updateTicketAtendimentoStats()
            ticketChannel = await interaction.guild.create_text_channel(
                name = channelName,
                topic = channelTopic,
                category = ticketCategorie
            )
            serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            serverOverwrites.read_messages, serverOverwrites.send_messages = False, False
            await ticketChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await ticketChannel.set_permissions(interaction.user, overwrite = userOverwrites)
            ticketOpenedEmbed = discord.Embed(
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket aberto! Envie seu problema em {ticketChannel.mention}",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            ticketOpenedEmbed.set_footer(text = "Atendimento!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Nos conte o seu problema aqui!\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            ticketEmbed.set_footer(text = f"Ticket de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:z_RedDiamond:938857687788183572>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250>||", embed = ticketEmbed, view = ticketCloseClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketPatrocinadorNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            ticketEmbed.set_footer(text = "Atendimento!")
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
        await alertChannel.send(f"『🙋』{interaction.user.mention} `({interaction.user.id})` fechou um ticket para patrocinador!")
        ticketCloseEmbed = discord.Embed(
            title = f"꧁🙋 Atendimento 🙋꧂",
            description = f"{interaction.user.mention}, você tem certeza que deseja fechar este ticket?",
            color = discord.Color.from_rgb(210, 50, 50)
        )
        ticketCloseEmbed.set_footer(text = "Atendimento!")
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
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket fechado!",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            ticketClosedEmbed.set_footer(text = "Atendimento!")
            await interaction.response.edit_message(embed = ticketClosedEmbed, view = None)
            ticketClosedMsgEmbed = discord.Embed(
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket fechado por {interaction.user.mention}!",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            await interaction.channel.send(embed = ticketClosedMsgEmbed, view = ticketReopen(self.bot, self.json, self.user))
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketPatrocinadorNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket reaberto!",
                color = discord.Color.from_rgb(210, 50, 50)
            )
            ticketEmbed.set_footer(text = "Atendimento!")
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
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『🎫』Ticket aberto por {interaction.user.mention}!",
                color = discord.Color.from_rgb(210, 50, 50)
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
                title = f"꧁🙋 Atendimento 🙋꧂",
                description = f"『💥』Este ticket será excluído em 3, 2, 1...!",
                color = discord.Color.from_rgb(255, 70, 20)
            )
            ticketDeleteEmbed.set_image(url = "https://media.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
            ticketDeleteEmbed.set_footer(text = "Atendimento!")
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketDeleteEmbed, view = None)
            await asyncio.sleep(3)
            await interaction.channel.delete(
                reason = "Ticket excluído!"
            )
            return
        except Exception as e:
            print(e)

async def getTicketAtendimentoRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["atendimentoChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["atendimentoTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> Atendimento <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
*Tem alguma dúvida sobre o Janny, ou está com problemas em usá-lo? Clique no botão abaixo e abra um ticket. Um de nossos administradores irá lhe ajudar assim que possível!*
""",
            color = discord.Color.from_rgb(210, 50, 50)
        )
        ticketMenuEmbed.add_field(name = "『✅』O que resolvemos aqui:", inline = False, value =
"""
➺ Tiramos dúvidas quanto aos comandos e como usá-los;
➺ Discutimos sobre bugs/falhas do bot;
➺ Ajudamos a convidar o bot caso esteja com problemas;
➺ Explicamos melhor sobre os Termos de Serviço e a Política de Privacidade do bot;
➺ Auxiliamos, na medida do possível, outros criadores de bots sobre o desenvolvimento de seus bots.
"""
        )
        ticketMenuEmbed.add_field(name = "『❌』O que não resolvemos aqui:", inline = False, value =
"""
➺ Sugestões para comandos ou funcionalidades. Para isto, use o <#1048041009759653958>;
➺ Assuntos relacionados ao servidor, como canais, tópicos, regras, mapa, cargos, etc.;
➺ Off-topic em geral e conversas paralelas.
"""
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/7p24U3r.png")
        ticketMenuEmbed.set_footer(text = "Atendimento", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)