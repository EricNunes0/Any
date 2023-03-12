import discord
import json
import random
import asyncio
from mongoconnection.ticket import *

class parceriaRequestEntryRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Pedir parceria", style = discord.ButtonStyle.blurple, emoji = "🤝", disabled = False)
    async def parceriaRequestEntryInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        parceriaRequestEmbed = discord.Embed(
            title = f"꧁🤝 Parceria 🤝꧂",
            description = "Você tem certeza de que deseja fazer uma parceria?",
            color = discord.Color.from_rgb(230, 170, 10)
        )
        parceriaRequestEmbed.set_footer(text = "Parcerias!")
        await interaction.response.send_message(embed = parceriaRequestEmbed, view = parceriaEntryConfirmRow(self.bot, self.json), ephemeral = True)

class parceriaEntryConfirmRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim!", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaConfirmEntryInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 990275792074317854)
            channelName = f"『✋』✩⋆parceria-pedido⋆✩"
            channelTopic = f"Pedido de parceria: {interaction.user.id}"
            for channel in interaction.guild.text_channels:
                if channel.topic == channelTopic:
                    parceriaAlreadyOpenedEmbed = discord.Embed(
                        title = f"꧁🤝 Parceria 🤝꧂",
                        description = f"『📃』Você possui um canal aberto para parcerias: {channel.mention}!",
                        color = discord.Color.from_rgb(230, 170, 10)
                    )
                    parceriaAlreadyOpenedEmbed.set_footer(text = "Parcerias!")
                    await interaction.response.edit_message(embed = parceriaAlreadyOpenedEmbed, view = None)
                    return
            parceriaFormChannel = await interaction.guild.create_text_channel(
                name = channelName,
                topic = channelTopic,
                category = ticketCategorie
            )
            serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            serverOverwrites.read_messages, serverOverwrites.send_messages = False, False
            await parceriaFormChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await parceriaFormChannel.set_permissions(interaction.user, overwrite = userOverwrites)
            parceriaOpenedEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📃』Ticket aberto: {parceriaFormChannel.mention}!",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            parceriaOpenedEmbed.set_footer(text = "Parcerias!")
            await interaction.response.edit_message(embed = parceriaOpenedEmbed, view = None)
            alertChannel = self.bot.get_channel(self.json["parceriaAlert"])
            await alertChannel.send(f"『🤝』{interaction.user.name} `({interaction.user.id})` mostrou interesse em ser um parceiro!")
            registerHobbieAdd = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = 1074516317555675217)
            await interaction.user.add_roles(registerHobbieAdd)
            parceriaFormEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📄』Seja bem-vindo! Em breve um de nossos responsáveis pelas parcerias irá lhe responder.",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            parceriaFormEmbed.set_footer(text = f"Pedido de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            await parceriaFormChannel.send(content = f"『<a:ab_YellowDiamond:938857668888645673>』Bem-vindo(a), {interaction.user.mention}!\n<@&1071499645311782912>", embed = parceriaFormEmbed)
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketStaffNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『❌』Pedido cancelado!",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            ticketEmbed.set_footer(text = "Parcerias!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
            return
        except Exception as e:
            print(e)

async def getTicketParceriaNewRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["parceriaNewChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["parceriaNewTicket"])
        parceriaDescriptionEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> SEJA UM PARCEIRO <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
*Gostaria de fazer uma parceria com o nosso servidor? Então esta é a hora! Basta clicar no botão \"🤝 Pedir parceria\" e aguardar até que um de nossos gerenciadores de parceria lhe atenda.*
""",
            color = discord.Color.from_rgb(230, 170, 10)
        )
        parceriaDescriptionEmbed.add_field(name = "『🔰』Requisitos mínimos:", inline = False, value =
"""
➺ O responsável pela parceria precisa obrigatoriamente permanecer neste servidor;
➺ Ter no mínimo 100 membros (sem contar os bots). (Não fazemos parcerias com servidores recém-criados e com mais bots do que pessoas!)
➺ Ter um cargo e um canal para anunciar as parcerias.
Exemplo:
⇀ <#750017382734495775> (Canal para avisos de parcerias)
⇁ <@&979920562883268638> (Cargo para avisar os membros sobre parcerias
"""
        )
        parceriaDescriptionEmbed.set_image(url = "https://i.imgur.com/rD4teJy.png")
        parceriaDescriptionEmbed.set_footer(text = "Parcerias!", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = parceriaDescriptionEmbed, view = parceriaRequestEntryRow(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)