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
    
    @discord.ui.button(label = f"Criar ticket", style = discord.ButtonStyle.blurple, emoji = "🔮")
    async def ticketBoosterInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🔮』{interaction.user.name} `({interaction.user.id})` abriu um ticket para booster!")
        ticketEmbed = discord.Embed(
            title = f"꧁🔮 Seja Booster 🔮꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(175, 50, 200)
        )
        ticketEmbed.set_footer(text = "Seja Booster!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketBoosterYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 1066082691843362917)
            ticketStats = getTicketVipStats()
            channelName = f"『🔮』・✧booster-{int(ticketStats['Boost']) + 1}✧"
            updateTicketBoosterStats()
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
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket aberto! Faça seu pedido em {ticketChannel.mention}",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            ticketOpenedEmbed.set_footer(text = "Seja Booster!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Para ver todos os benefícios de se tornar um booster, acesse <#1048659113107804260>\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            ticketEmbed.set_footer(text = f"Ticket de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:ab_PurpleDiamond:938883672717787196>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250>||", embed = ticketEmbed, view = ticketCloseClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketBoosterNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            ticketEmbed.set_footer(text = "Seja Booster!")
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
    async def ticketBoosterCloseInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『🔮』{interaction.user.mention} `({interaction.user.id})` fechou um ticket para booster!")
        ticketCloseEmbed = discord.Embed(
            title = f"꧁🔮 Seja Booster 🔮꧂",
            description = f"{interaction.user.mention}, você tem certeza que deseja fechar este ticket?",
            color = discord.Color.from_rgb(175, 50, 200)
        )
        ticketCloseEmbed.set_footer(text = "Seja Booster!")
        await interaction.response.send_message(embed = ticketCloseEmbed, view = ticketCancelConfirm(self.bot, self.json, self.user), ephemeral = True)

class ticketCancelConfirm(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketBoosterCloseYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketClosedEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket fechado!",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            ticketClosedEmbed.set_footer(text = "Seja Booster!")
            await interaction.response.edit_message(embed = ticketClosedEmbed, view = None)
            ticketClosedMsgEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket fechado por {interaction.user.mention}!",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            await interaction.channel.send(embed = ticketClosedMsgEmbed, view = ticketReopen(self.bot, self.json, self.user))
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketBoosterNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket reaberto!",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            ticketEmbed.set_footer(text = "Seja Booster!")
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
    async def ticketBoosterReopenInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketReopenedEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『🎫』Ticket aberto por {interaction.user.mention}!",
                color = discord.Color.from_rgb(175, 50, 200)
            )
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketReopenedEmbed)
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Excluir", style = discord.ButtonStyle.red, emoji = "💣")
    async def ticketBoosterNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketDeleteEmbed = discord.Embed(
                title = f"꧁🔮 Seja Booster 🔮꧂",
                description = f"『💥』Este ticket será excluído em 3, 2, 1...!",
                color = discord.Color.from_rgb(255, 70, 20)
            )
            ticketDeleteEmbed.set_image(url = "https://media.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
            ticketDeleteEmbed.set_footer(text = "Seja Booster!")
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketDeleteEmbed, view = None)
            await asyncio.sleep(3)
            await interaction.channel.delete(
                reason = "Ticket excluído!"
            )
            return
        except Exception as e:
            print(e)

async def getTicketBoosterRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["boosterChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["boosterTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> Seja Booster <a:ab_LeftArrow:939177402381246514>꧂",
            description = """ 
🚀 **Seja um membro** <@&960291907030896671> 🚀

✦ O impulso de servidor é uma forma de apoiar e ajudar a evoluir os servidores do Discord ✦
***Como funciona?*** <a:ab_RoundThink:960384227852034059>
Primeiramente você precisa ter o **Nitro Gaming** (um plano do próprio Discord que possui a opção de dar 2 boosts). Após isso, basta impulsionar o servidor.

<a:ab_PurpleDiamond:938883672717787196>  **BENEFÍCIOS** <a:ab_PurpleDiamond:938883672717787196>

<a:ab_RightArrow:939177432127246427> **1 IMPULSO** <a:ab_LeftArrow:939177402381246514>
➺ Cargo destacado na lateral do servidor <@&1005267950212747375>
➺ Permissão para enviar imagens e vídeos em qualquer chat
➺ XP Loritta: 1.5x
➺ Sem tempo de claim nos sorteios 
➺ Imune a requisito dos sorteios
➺ 50% de desconto para compra de VIP
➺ Apostas ilimitadas na <#1053878659829735424>

<a:ab_RightArrow:939177432127246427> **2 IMPULSOS** <a:ab_LeftArrow:939177402381246514>
➺ Cargo destacado na lateral do servidor <@&1047535078806405231>
➺ Cargo exclusivo para dar aos amigos
➺ Call privada para quem tiver seu cargo
➺ Permissão para enviar imagens e vídeos em qualquer chat
➺ Sem tempo de claim nos sorteios 
➺ Imune a requisito dos sorteios
➺ XP Loritta: 2x
➺ 50% de desconto para compra de VIP
➺ Apostas ilimitadas na <#1053878659829735424>

<a:ab_carregando:911073196038582272> Os benefícios permanecerão durante o seu tempo de impulso, se remover o boost, automaticamente perderá o cargo e os privilégios. <a:ab_carregando:911073196038582272>
""",
            color = discord.Color.from_rgb(175, 50, 200)
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/s22ipWD.png")
        ticketMenuEmbed.set_footer(text = "Seja Booster", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)