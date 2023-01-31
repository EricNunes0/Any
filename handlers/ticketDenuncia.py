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
    
    @discord.ui.button(label = f"Denunciar", style = discord.ButtonStyle.gray, emoji = "🚔")
    async def ticketDenunciaInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🚔』{interaction.user.name} `({interaction.user.id})` abriu um ticket para denúncia!")
        ticketEmbed = discord.Embed(
            title = f"꧁🚔 Denúncia 🚔꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(20, 20, 60)
        )
        ticketEmbed.set_footer(text = "Denúncia!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketDenunciaYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 736637479616118857)
            ticketStats = getTicketVipStats()
            channelName = f"『🚔』・✧denúncia-{int(ticketStats['Denuncia']) + 1}✧"
            channelTopic = f"Denúncia de {interaction.user.id}"
            for channel in interaction.guild.text_channels:
                if channel.topic == channelTopic:
                    parceriaAlreadyOpenedEmbed = discord.Embed(
                        title = f"꧁🚔 Denúncia 🚔꧂",
                        description = f"『📃』Você possui um canal de denúncia aberto: {channel.mention}! Caso não consiga visualizar, entre em contato com um administrador.",
                        color = discord.Color.from_rgb(20, 20, 60)
                    )
                    parceriaAlreadyOpenedEmbed.set_footer(text = "Denúncia!")
                    await interaction.response.edit_message(embed = parceriaAlreadyOpenedEmbed, view = None)
                    return
            updateTicketDenunciaStats()
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
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket aberto! Envie seu problema em {ticketChannel.mention}",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            ticketOpenedEmbed.set_footer(text = "Denúncia!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Faça a sua denúncia aqui!\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            ticketEmbed.set_footer(text = f"Ticket de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:z_BlueDiamond:938850305083314207>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250>||", embed = ticketEmbed, view = ticketCloseClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketDenunciaNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            ticketEmbed.set_footer(text = "Denúncia!")
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
    async def ticketDenunciaCloseInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🚔』{interaction.user.name} `({interaction.user.id})` fechou um ticket para denúncia!")
        ticketCloseEmbed = discord.Embed(
            title = f"꧁🚔 Denúncia 🚔꧂",
            description = f"{interaction.user.mention}, você tem certeza que deseja fechar este ticket?",
            color = discord.Color.from_rgb(20, 20, 60)
        )
        ticketCloseEmbed.set_footer(text = "Denúncia!")
        await interaction.response.send_message(embed = ticketCloseEmbed, view = ticketCancelConfirm(self.bot, self.json, self.user), ephemeral = True)

class ticketCancelConfirm(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketDenunciaCloseYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketClosedEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket fechado!",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            ticketClosedEmbed.set_footer(text = "Denúncia!")
            await interaction.response.edit_message(embed = ticketClosedEmbed, view = None)
            ticketClosedMsgEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket fechado por {interaction.user.mention}!",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            await interaction.channel.send(embed = ticketClosedMsgEmbed, view = ticketReopen(self.bot, self.json, self.user))
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketDenunciaNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket reaberto!",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            ticketEmbed.set_footer(text = "Denúncia!")
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
    async def ticketDenunciaReopenInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketReopenedEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『🎫』Ticket aberto por {interaction.user.mention}!",
                color = discord.Color.from_rgb(20, 20, 60)
            )
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketReopenedEmbed)
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Excluir", style = discord.ButtonStyle.red, emoji = "💣")
    async def ticketDenunciaNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketDeleteEmbed = discord.Embed(
                title = f"꧁🚔 Denúncia 🚔꧂",
                description = f"『💥』Este ticket será excluído em 3, 2, 1...!",
                color = discord.Color.from_rgb(255, 70, 20)
            )
            ticketDeleteEmbed.set_image(url = "https://media.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
            ticketDeleteEmbed.set_footer(text = "Denúncia!")
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketDeleteEmbed, view = None)
            await asyncio.sleep(3)
            await interaction.channel.delete(
                reason = "Ticket excluído!"
            )
            return
        except Exception as e:
            print(e)

async def getTicketDenunciaRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["denunciaChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["denunciaTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> Denúncias <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
Algum membro está infringindo as <#1064003850228473876>? Aqui você pode denunciar os criminosos que estão descumprindo a lei <:e_Policia:1070011396294721547>!
""",
            color = discord.Color.from_rgb(20, 20, 60)
        )
        ticketMenuEmbed.add_field(name = "『🚔』Como denunciar?", inline = False, value =
"""
Clique no botão \"🚔 Denunciar\" para abrir um ticket. Nele, seja breve e relate a sua denúncia, com provas como prints/vídeos. Após as denúncias serem comprovadas, o acusado será devidamente punido!
"""
        )
        ticketMenuEmbed.add_field(name = "『⚠』Atenção:", inline = False, value =
"""
➺ **Jamais denuncie alguém sem motivo!** Acusar alguém de um crime sem provas resultará em punições, então fique bastante atento;
➺ Não abra tickets desnecessariamente;
➺ Evite off-topic em geral e conversas paralelas.
"""
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/GazWmNS.png")
        ticketMenuEmbed.set_footer(text = "Denúncia", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)