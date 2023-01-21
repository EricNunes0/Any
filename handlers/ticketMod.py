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
    
    @discord.ui.button(label = f"Mov-chat", style = discord.ButtonStyle.gray, emoji = "💬")
    async def ticketStaffInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        ticketEmbed = discord.Embed(
            title = f"꧁💬 Mov-chat 💬꧂",
            description = "Os <@&1054734844434845726> são os responsáveis por manter a atividade no servidor!",
            color = discord.Color.from_rgb(160, 160, 160)
        )
        ticketEmbed.set_footer(text = "Seja Staff!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Tenho interesse!", style = discord.ButtonStyle.green, emoji = "🙋‍♀️")
    async def ticketStaffYesInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketCategorie = discord.utils.get(interaction.guild.categories, id = 1066082691843362917)
            ticketStats = getTicketVipStats()
            channelName = f"『🔰』・✧staff-form✧"
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
            userOverwrites.read_messages, userOverwrites.send_messages = True, False
            await ticketChannel.set_permissions(interaction.user, overwrite = userOverwrites)
            ticketOpenedEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『🔰』Siga as instruções do canal {ticketChannel.mention}!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketOpenedEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            alertChannel = self.bot.get_channel(self.json["staffAlert"])
            await alertChannel.send(f"『💬』{interaction.user.name} `({interaction.user.id})` mostrou interesse em ser um mov-chat!")
            ticketEmbed = discord.Embed(
                title = f"꧁💬 Mov-Chat 💬꧂",
                description = f"『📄』Clique no botão \"✍ Responder\" e responda as perguntas abaixo. Após responder, clique em \"✅ Enviar\" para concluir o formulário.\n\n『❌』Para cancelar o formulário, clique em \"❌ Cancelar\".\n\n『<a:a_Alert:1063858446853734490>』**Atenção:** todas as respostas precisam obrigatoriamente ser respondidas. Caso não as responda, seu formulário será recusado!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketEmbed.add_field(name = f"Qual horário você geralmente está mais ativo no Discord?", value = "`Não informado`", inline = False)
            ticketEmbed.add_field(name = f"Se uma pessoa estiver floodando/spamando mensagens nos canais de conversa, o que você faria?", value = "`Não informado`", inline = False)
            ticketEmbed.set_footer(text = f"Formulário de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:ab_GrayDiamond:938884683771543572>』Bem-vindo(a), {interaction.user.mention}!\n<@&739210760567390250>", embed = ticketEmbed, view = movchatFormClass(self.bot, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketStaffNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Pedido cancelado!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
            return
        except Exception as e:
            print(e)

class movchatFormClass(discord.ui.View):
    def __init__(self, bot, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def movchatAnswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(movchatModal())
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Enviar", style = discord.ButtonStyle.green, emoji = "✅")
    async def movchatConfirmAnswers(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『✅』Sua respostas foram enviadas para os administradores! Entraremos em contato com você caso tenha sido aprovado.",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『✅』{interaction.user.mention} concluiu o formulário!",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250>", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancel", style = discord.ButtonStyle.red, emoji = "❌")
    async def movchatCancelForm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250>", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class movchatModal(discord.ui.Modal, title = "Formulário para Mov-chat"):
    def __init__(self):
        super().__init__(timeout = None)

        self.add_item(discord.ui.TextInput(
            label="Qual horário você está mais ativo?",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 256,
            required = True,
            )
        ),
        self.add_item(discord.ui.TextInput(
            label="O que faria em caso de flood?",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 256,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            answer1 = self.children[1].value
            print(len(answer0), answer0)
            answerEmbed = discord.Embed(
                    title = f"꧁💬 Mov-chat 💬꧂",
                    description = f"『📄』Clique no botão \"✍ Responder\" e responda as perguntas abaixo. Após responder, clique em \"✅ Enviar\" para concluir o formulário.\n\n『❌』Para cancelar o formulário, clique em \"❌ Cancelar\".\n\n『<a:a_Alert:1063858446853734490>』**Atenção:** todas as respostas precisam obrigatoriamente ser respondidas. Caso não as responda, seu formulário será recusado!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
            answerEmbed.add_field(name = "Qual horário você geralmente está mais ativo no Discord?", value = answer0, inline = False)
            answerEmbed.add_field(name = "Se uma pessoa estiver floodando/spamando mensagens nos canais de conversa, o que você faria?", value = answer1, inline = False)
            answerEmbed.set_footer(text = f"Formulário de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            await interaction.message.edit(embeds = [answerEmbed])
            answerConfirmEmbed = discord.Embed(
                title = f"꧁💬 Mov-chat 💬꧂",
                description = f"『✅』Sua respostas foram alteradas! Clique em \"✅ Enviar\" para concluir o formulário!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
        except Exception as e:
            print(e)


async def getTicketModRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["modChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["modTicket"])
        ticketMenuEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> Seja Staff <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
*Gostaria de participar da nossa equipe e nos ajudar a manter o servidor em ordem? Pois estão abertas as vagas para a staff!*
""",
            color = discord.Color.from_rgb(160, 160, 160)
        )
        ticketMenuEmbed.add_field(name = "『🔰』Requisitos mínimos:", inline = False, value =
"""
➺ Ter responsabilidade e comprometimento com as <#1064003850228473876>;
➺ Ter disponibilidade para moderar;
➺ Responder ao formulário **honestamente**!
"""
        )
        ticketMenuEmbed.add_field(name = "『📄』Critérios avaliados:", inline = False, value =
"""
➺ Conversas em canais de conversa/bots;
➺ Tempo online no servidor;
➺ Conhecimento das regras;
➺ Participação das atividades do servidor;
➺ Ficha de infrações cometidas.
"""
        )
        ticketMenuEmbed.set_image(url = "https://i.imgur.com/g4UL6yX.png")
        ticketMenuEmbed.set_footer(text = "Seja Staff", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = ticketMenuEmbed, view = ticketClass(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)