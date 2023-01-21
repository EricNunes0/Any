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
    
    @discord.ui.button(label = f"Ametista", style = discord.ButtonStyle.blurple, emoji = "<a:ab_PurpleDiamond:938883672717787196>")
    async def ticketVipAmetistaInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『💎』{interaction.user.name} `({interaction.user.id})` abriu um ticket para VIP!")
        ticketEmbed = discord.Embed(
            title = f"꧁💎 Seja VIP 💎꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(50, 30, 200)
        )
        ticketEmbed.add_field(name = "『<a:ab_PurpleDiamond:938883672717787196>』VIP escolhido:", value = "<@&1051948366461939744>", inline = False)
        ticketEmbed.set_footer(text = "Seja VIP!")
        vipRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(1051948366461939744))
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json, vipRole, 1), ephemeral = True)

    @discord.ui.button(label = f"Jade", style = discord.ButtonStyle.blurple, emoji = "<a:ab_GreenDiamond:938880803692240927>")
    async def ticketVipJadeInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『💎』{interaction.user.name} `({interaction.user.id})` abriu um ticket para VIP!")
        ticketEmbed = discord.Embed(
            title = f"꧁💎 Seja VIP 💎꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(50, 30, 200)
        )
        ticketEmbed.add_field(name = "『<a:ab_GreenDiamond:938880803692240927>』VIP escolhido:", value = "<@&1047268770504253561>", inline = False)
        ticketEmbed.set_footer(text = "Seja VIP!")
        vipRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(1047268770504253561))
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json, vipRole, 2), ephemeral = True)

    @discord.ui.button(label = f"Safira", style = discord.ButtonStyle.blurple, emoji = "<a:ab_BlueDiamond:938850305083314207>")
    async def ticketVipSaphireInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『💎』{interaction.user.name} `({interaction.user.id})` abriu um ticket para VIP!")
        ticketEmbed = discord.Embed(
            title = f"꧁💎 Seja VIP 💎꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(50, 30, 200)
        )
        ticketEmbed.add_field(name = "『<a:ab_BlueDiamond:938850305083314207>』VIP escolhido:", value = "<@&1047268807812595802>", inline = False)
        ticketEmbed.set_footer(text = "Seja VIP!")
        vipRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(1047268807812595802))
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json, vipRole, 3), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json, role, code):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.role = role
        self.code = code
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketVipYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 1066082691843362917)
            ticketVipStats = getTicketVipStats()
            if int(self.code) == 1:
                vipChannelName = f"『🟣』・✧vip-{int(ticketVipStats['VipAmetista']) + 1}✧"
                updateTicketVipAmetistaStats()
            elif int(self.code) == 2:
                vipChannelName = f"『✳』・✧vip-{int(ticketVipStats['VipJade']) + 1}✧"
                updateTicketVipJadeStats()
            elif int(self.code) == 3:
                vipChannelName = f"『🔷』・✧vip-{int(ticketVipStats['VipSafira']) + 1}✧"
                updateTicketVipSaphireStats()
            else:
                vipChannelName = f"『🎫』・✧vip-{int(ticketVipStats['Total'])}✧"
            ticketChannel = await interaction.guild.create_text_channel(
                name = vipChannelName,
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
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket aberto! Faça seu pedido em {ticketChannel.mention}",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            ticketOpenedEmbed.set_footer(text = "Seja VIP!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁💎 Loja de VIP's 💎꧂",
                description = f"『🎫』{interaction.user.mention} selecionou o VIP {self.role.mention}!\nPara ver todos os planos VIP disponíveis, acesse <#1047316824976523354>\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            ticketEmbed.set_footer(text = f"Ticket de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:ab_BlueDiamond:938850305083314207>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250>||", embed = ticketEmbed, view = ticketCloseClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketVipNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            ticketEmbed.set_footer(text = "Seja VIP!")
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
    async def ticketVipCloseInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『💎』{interaction.user.mention} `({interaction.user.id})` fechou um ticket para VIP!")
        ticketCloseEmbed = discord.Embed(
            title = f"꧁💎 Seja VIP 💎꧂",
            description = f"{interaction.user.mention}, você tem certeza que deseja fechar este ticket?",
            color = discord.Color.from_rgb(50, 30, 200)
        )
        ticketCloseEmbed.set_footer(text = "Seja VIP!")
        await interaction.response.send_message(embed = ticketCloseEmbed, view = ticketCancelConfirm(self.bot, self.json, self.user), ephemeral = True)

class ticketCancelConfirm(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketVipCloseYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketClosedEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket fechado!",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            ticketClosedEmbed.set_footer(text = "Seja VIP!")
            await interaction.response.edit_message(embed = ticketClosedEmbed, view = None)
            ticketClosedMsgEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket fechado por {interaction.user.mention}!",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            await interaction.channel.send(embed = ticketClosedMsgEmbed, view = ticketReopen(self.bot, self.json, self.user))
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketVipNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket reaberto!",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            ticketEmbed.set_footer(text = "Seja VIP!")
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
    async def ticketVipReopenInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.user)
            userOverwrites = interaction.channel.overwrites_for(self.user)
            userOverwrites.read_messages, userOverwrites.send_messages = True, True
            await interaction.channel.set_permissions(self.user, overwrite = userOverwrites)
            ticketReopenedEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket aberto por {interaction.user.mention}!",
                color = discord.Color.from_rgb(50, 30, 200)
            )
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketReopenedEmbed)
            return
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Excluir", style = discord.ButtonStyle.red, emoji = "💣")
    async def ticketVipNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketDeleteEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『💥』Este ticket será excluído em 3, 2, 1...!",
                color = discord.Color.from_rgb(255, 70, 20)
            )
            ticketDeleteEmbed.set_image(url = "https://media.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
            ticketDeleteEmbed.set_footer(text = "Seja VIP!")
            await interaction.message.edit(view = None)
            await interaction.channel.send(embed = ticketDeleteEmbed, view = None)
            await asyncio.sleep(3)
            await interaction.channel.delete(
                reason = "Ticket excluído!"
            )
            return
        except Exception as e:
            print(e)

async def getTicketVipRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["vipChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["vipTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> SEJA VIP <a:ab_LeftArrow:939177402381246514>꧂",
            description = """ 
*Apoie o servidor de diferentes formas, adquirindo um plano VIP você ganha diversos privilégios e benefícios aqui dentro, além de contribuir com o crescimento e a melhoria da nossa comunidade!*

<a:ab_PurpleDiamond:938883672717787196> __**VIP AMETISTA**__ <a:ab_PurpleDiamond:938883672717787196>
➺ Cargo destacado na lateral do servidor <@&1051948366461939744>;
➺ Permissão para enviar imagens/vídeos no <#723155037332832296>;
➺ +14 cores disponíveis no <#1064641839027724440> (claras e escuras);
➺ Tempo de claim nos sorteios: **30 minutos**;
➺ XP Loritta: **1.5x**;
➺ Sorteios exclusivos;
⇀ **Duração:** 30 dias.
⇁ **Valor:** 20M de Janny Coins ou 100K de sonhos

<a:ab_GreenDiamond:938880803692240927> __**VIP JADE**__ <a:ab_GreenDiamond:938880803692240927>
➺ Cargo destacado na lateral do servidor <@&1047268770504253561>;
➺ Permissão para enviar imagens e vídeos no <#723155037332832296>;
➺ +20 cores disponíveis no <#1064641839027724440> (claras, escuras e neutras);
➺ Cargo exclusivo para dar aos amigos;
➺ Tempo de claim nos sorteios: **1 hora**;
➺ XP Loritta: **2x**;
➺ Sorteios exclusivos;
➺ Entrada 2x em sorteios e drops;
⇀ **Duração:** 30 dias.
⇁ **Valor:** 30M de Janny Coins ou 200K de sonhos.

<a:ab_BlueDiamond:938850305083314207> __**VIP SAFIRA**__ <a:ab_BlueDiamond:938850305083314207>
➺ Cargo destacado na lateral do servidor <@&1047268807812595802>;
➺ Permissão para enviar imagens e vídeos em qualquer chat;
➺ +30 cores disponíveis no <#1064641839027724440> (claras, escuras, neutras e especiais);
➺ Cargo exclusivo para dar aos amigos;
➺ Call privada para quem tiver seu cargo;
➺ Sem tempo de claim nos sorteios;
➺ XP Loritta: **2.5x**;
➺ Sorteios exclusivos;
➺ Entrada 3x em sorteios e drops;
➺ Imune a requisito dos sorteios;
⇀ **Duração:** 30 dias.
⇁ **Valor:** 40M de Janny Coins ou 300K de sonhos.

Se já estiver com um VIP e queira dar um upgrade, os dias restantes serão adicionados no VIP atual. <a:ab_8bitLaserDance:908674226288988230>
""",
            color = discord.Color.from_rgb(50, 30, 200)
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/mxIyBqg.png")
        ticketMenuEmbed.set_footer(text = "Seja VIP", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)