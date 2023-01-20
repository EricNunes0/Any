import discord
import json
import random

class ticketClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Comprar VIP", style = discord.ButtonStyle.blurple, emoji = "💎")
    async def ticketVipInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        alertChannel = self.bot.get_channel(self.json["ticketAlert"])
        await alertChannel.send(f"『💎』{interaction.user.mention} `({interaction.user.id})` abriu um ticket para VIP!")
        ticketEmbed = discord.Embed(
            title = f"꧁💎 Seja VIP 💎꧂",
            description = "Você tem certeza que deseja abrir um ticket? Nossos administradores entrarão em contato com você assim que possível!",
            color = discord.Color.from_rgb(80, 175, 255)
        )
        ticketEmbed.set_footer(text = "Seja VIP!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def ticketVipYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketChannel = await interaction.guild.create_text_channel(name = f"『💎』・✧vip-{random.randint(0, 10)}✧")
            ticketOpenedEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket aberto! Faça seu pedido em {ticketChannel.mention}",
                color = discord.Color.from_rgb(80, 175, 255)
            )
            ticketOpenedEmbed.set_footer(text = "Seja VIP!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            ticketEmbed = discord.Embed(
                title = f"꧁💎 Loja de VIP's 💎꧂",
                description = f"『🎫』Informe o plano VIP que você deseja!\nPara ver todos os planos VIP disponíveis, acesse <#1047316824976523354>\nNossa equipe de administradores irá lhe responder assim que possível.",
                color = discord.Color.from_rgb(80, 175, 255)
            )
            await ticketChannel.send(content = f"{interaction.user.mention}", embed = ticketEmbed)
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketVipNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁💎 Seja VIP 💎꧂",
                description = f"『🎫』Ticket cancelado!",
                color = discord.Color.from_rgb(80, 175, 255)
            )
            ticketEmbed.set_footer(text = "Seja VIP!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
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
            color = discord.Color.from_rgb(80, 175, 255)
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/mxIyBqg.png")
        ticketMenuEmbed.set_footer(text = "Seja VIP", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)