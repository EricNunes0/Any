import discord
import json
import random
import asyncio
from mongoconnection.ticket import *

QUESTION_BASE = "Em qual área você deseja ingressar?"
QUESTION_A1 = "Qual a sua idade?"
QUESTION_A2 = "Há quanto tempo você usa o Discord?"
QUESTION_A3 = "Em qual parte do dia você é mais ativo no Discord?"
QUESTION_A4 = "Você já participou da staff de outro servidor? Se sim, qual e por quanto tempo?"
QUESTION_A5 = "Por que você deveria ser contratado para a staff?"
QUESTION_A6 = "Em que você vai ajudar na moderação?"
QUESTION_A7 = "1º situação hipotética: Um membro está sendo preconceituoso (racista, homofóbico, xenofóbico, etc.) com outros membros no chat. Conte o que você faria:"
QUESTION_A8 = "2º situação hipotética: Um membro está cometendo assédio (ou outros atos desagradáveis). Como lidaria com a situação?"
QUESTION_A9 = "3º situação hipotética: Um membro está floodando/spamando mensagens nos canais de conversa. O que faria a respeito?"
QUESTION_A10 = "4º situação hipotética: Dois membros estão discutindo no chat, e atrapalhando a conversa de outros membros. Como agiria neste caso?"

class ticketClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Participar", style = discord.ButtonStyle.gray, emoji = "🎫")
    async def ticketStaffInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        ticketEmbed = discord.Embed(
            title = f"꧁🔰 Seja Staff 🔰꧂",
            description = "Você será redirecionado para o formulário de staff. Você tem certeza de que deseja continuar?",
            color = discord.Color.from_rgb(160, 160, 160)
        )
        ticketEmbed.set_footer(text = "Seja Staff!")
        await interaction.response.send_message(embed = ticketEmbed, view = ticketCreateConfirm(self.bot, self.json), ephemeral = True)

class ticketCreateConfirm(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
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
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『🔰』Siga as instruções do canal {ticketChannel.mention}!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketOpenedEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.edit_message(embed = ticketOpenedEmbed, view = None)
            alertChannel = self.bot.get_channel(self.json["staffAlert"])
            await alertChannel.send(f"『💬』{interaction.user.name} `({interaction.user.id})` mostrou interesse em ser um mov-chat!")
            ticketEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『🔘』Nas perguntas objetivas, clique em um dos botões abaixo para responder!\n\n『✍』Nas perguntas dissertativas (escritas), clique no botão **\"✍ Responder\"** e para alterar a resposta, em seguida em **\"✅ Confirmar\"** para enviá-la.\n\n『◀』Caso tenha preenchido uma resposta incorretamente e queira corrigi-la, clique em **\"◀ Voltar\"**.\n\n『❌』Para cancelar o formulário, clique em **\"❌ Cancelar\"**.\n\n『<a:a_Alert:1063858446853734490>』**Atenção:** todas as respostas precisam obrigatoriamente ser respondidas. Caso não as responda, seu formulário será recusado!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketEmbed.add_field(name = f"『🔘』{QUESTION_BASE}", value = "`Não informado`", inline = False)
            ticketEmbed.set_footer(text = f"Formulário de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await ticketChannel.send(content = f"『<a:ab_GrayDiamond:938884683771543572>』Bem-vindo(a), {interaction.user.mention}!\n||<@&739210760567390250 >||", embed = ticketEmbed, view = staffQuestionBase1Row(self.bot, ticketEmbed, self.json, ticketUser))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def ticketStaffNoInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ticketEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Inscrição cancelada!",
                color = discord.Color.from_rgb(160, 160, 160)
            )
            ticketEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.edit_message(embed = ticketEmbed, view = None)
            return
        except Exception as e:
            print(e)

class staffQuestionBase1Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Moderador", style = discord.ButtonStyle.blurple, emoji = "🚔")
    async def staffForm1Answer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 0, name = f"『☑』{QUESTION_BASE}", value = "`Moderador`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A1}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA1Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Mov-chat", style = discord.ButtonStyle.blurple, emoji = "💬", disabled = True)
    async def staffForm1Answer2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 0, name = f"『☑』{QUESTION_BASE}", value = "`Mov-chat`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A1}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA1Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Divulgador", style = discord.ButtonStyle.blurple, emoji = "📢", disabled = True)
    async def staffForm1Answer3(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 0, name = f"『☑』{QUESTION_BASE}", value = "`Divulgador`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A1}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA1Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffForm1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA1Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA1Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA1Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA1Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[1].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A2}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA2Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA1Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 1)
            self.embed.set_field_at(index = 0, name = f"**『🔘』{QUESTION_BASE}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionBase1Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA2Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA2Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA2Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA2Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[2].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『🔘』{QUESTION_A3}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA3Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA2Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 2)
            self.embed.set_field_at(index = 1, name = f"**『✍』{QUESTION_A1}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA1Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA2Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA3Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Manhã", style = discord.ButtonStyle.blurple, emoji = "🌄")
    async def staffFormA3Answer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 3, name = f"『☑』{QUESTION_A3}", value = "`Manhã`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A4}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA4Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Tarde", style = discord.ButtonStyle.blurple, emoji = "☀")
    async def staffFormA3Answer2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 3, name = f"『☑』{QUESTION_A3}", value = "`Tarde`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A4}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA4Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Noite", style = discord.ButtonStyle.blurple, emoji = "🌙")
    async def staffFormA3Answer3(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 3, name = f"『☑』{QUESTION_A3}", value = "`Noite`", inline = False)
            self.embed.add_field(name = f"**『✍』{QUESTION_A4}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA4Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA3Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 3)
            self.embed.set_field_at(index = 2, name = f"**『✍』{QUESTION_A2}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA2Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA3Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA4Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA2Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA4Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA4Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[4].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A5}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA5Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA4Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 4)
            self.embed.set_field_at(index = 3, name = f"**『🔘』{QUESTION_A3}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA3Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA4Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA5Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA5nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA5Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA5Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[5].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A6}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA6Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA5Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 5)
            self.embed.set_field_at(index = 4, name = f"**『✍』{QUESTION_A4}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA4Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA5Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA6Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA6nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA6Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA6Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[6].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A7}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA7Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA6Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 6)
            self.embed.set_field_at(index = 5, name = f"**『✍』{QUESTION_A5}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA5Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA6Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA7Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA7nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA7Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA7Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[7].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A8}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA8Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA7Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 7)
            self.embed.set_field_at(index = 6, name = f"**『✍』{QUESTION_A6}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA6Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA7Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA8Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA8nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA8Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA8Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[8].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A9}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA9Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA8Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 8)
            self.embed.set_field_at(index = 7, name = f"**『✍』{QUESTION_A7}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA7Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA8Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA9Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA9nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA9Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA9Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[9].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『✍』{QUESTION_A10}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA10Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA9Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 9)
            self.embed.set_field_at(index = 8, name = f"**『✍』{QUESTION_A8}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA8Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA9Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA10Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def staffFormA10nswer(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(staffQuestionA10Modal(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormA10Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[10].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🔰 Seja Staff 🔰꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(160, 160, 160)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Seja staff!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = f"**『⚠』Aviso final:**", value = "`Após responder este formulário, suas respostas serão enviadas para os administradores e revisadores, para que possam ser analisadas. Caso você tenha sido aprovado, entraremos em contato com você. Pedimos que entenda que os administradores tem seus compromissos e seu próprio tempo. Portanto, não insista para analisarmos imediatamente o seu formulário. Você está de acordo com isso?`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionFinishRow(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA10Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 10)
            self.embed.set_field_at(index = 9, name = f"**『✍』{QUESTION_A9}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA9Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA10Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionFinishRow(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def staffFormFinishConfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.set_field_at(index = 11, name = f"『✅』Aviso final:", value = "`Aceito!`", inline = False)
            self.embed.color = discord.Color.from_rgb(20, 200, 20)
            await interaction.message.edit(embed = self.embed, view = None)
            parceriaOpenedEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『📃』Suas respostas foram enviadas! Entraremos em contato com você caso seja aprovado.",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            parceriaOpenedEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embed = parceriaOpenedEmbed, ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            parceriaFormEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『📄』{interaction.user.mention} terminou o formulário!",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            await interaction.channel.send(embed = parceriaFormEmbed)

        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def staffFormA11Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.remove_field(index = 11)
            self.embed.set_field_at(index = 10, name = f"**『✍』{QUESTION_A10}**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = staffQuestionA10Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA10Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Seja Staff!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🔰 Seja Staff 🔰꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Seja Staff!")
            await interaction.channel.send(content = "<@&739210760567390250 >", embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class staffQuestionA1Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "Qual a sua idade?",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 10,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 1, name = f"『☑』{QUESTION_A1}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA2Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "Há quanto tempo você usa o Discord?",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 50,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 2, name = f"『☑』{QUESTION_A2}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA4Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "Já participou de outra staff?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 300,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 4, name = f"『☑』{QUESTION_A4}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA5Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "Por que você deveria ser contratado?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 400,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 5, name = f"『☑』{QUESTION_A5}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA6Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "Em que você vai ajudar?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 400,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 6, name = f"『☑』{QUESTION_A6}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA7Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "O que faria?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 300,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 7, name = f"『☑』{QUESTION_A7}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA8Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "O que faria?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 300,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 8, name = f"『☑』{QUESTION_A8}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA9Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "O que faria?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 300,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 9, name = f"『☑』{QUESTION_A9}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class staffQuestionA10Modal(discord.ui.Modal, title = "Formulário para staff"):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "O que faria?",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 300,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 10, name = f"『☑』{QUESTION_A10}", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
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
➺ Obedecer as ordens de seus superiores;
➺ Responder ao formulário **honestamente**!
"""
        )
        ticketMenuEmbed.add_field(name = "『💼』Áreas disponíveis:", inline = False, value =
        """
<@&793689864469217290> ➺ São os responsáveis por moderar os chats de conversa e, caso necessário, punir membros que estejam infrinjindo as regras;

<@&1054734844434845726> ➺ São os responsáveis por manter os chats de conversa ativos, incentivando os membros a participarem mais ativamente no servidor;

<@&912505147907788890> ➺ São os responsáveis por divulgar nosso servidor e buscar parcerias.
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