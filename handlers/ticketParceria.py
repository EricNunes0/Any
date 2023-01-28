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
    
    @discord.ui.button(label = f"Pedir parceria", style = discord.ButtonStyle.blurple, emoji = "🤝")
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
            channelName = f"『📃』✩⋆parceria-form⋆✩"
            channelTopic = f"Formulário de parceria: {interaction.user.id}"
            for channel in interaction.guild.text_channels:
                if channel.topic == channelTopic:
                    parceriaAlreadyOpenedEmbed = discord.Embed(
                        title = f"꧁🤝 Parceria 🤝꧂",
                        description = f"『📃』Você possui um canal aberto para preencher o formulário: {channel.mention}!",
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
            userOverwrites.read_messages, userOverwrites.send_messages = True, False
            await parceriaFormChannel.set_permissions(interaction.user, overwrite = userOverwrites)
            parceriaOpenedEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📃』Siga as instruções do canal {parceriaFormChannel.mention}!",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            parceriaOpenedEmbed.set_footer(text = "Parcerias!")
            await interaction.response.edit_message(embed = parceriaOpenedEmbed, view = None)
            alertChannel = self.bot.get_channel(self.json["parceriaAlert"])
            await alertChannel.send(f"『🤝』{interaction.user.name} `({interaction.user.id})` mostrou interesse em ser um parceiro!")
            parceriaFormEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📄』Clique no botão \"✍ Responder\" e responda as perguntas abaixo. Após responder, clique em \"✅ Enviar\" para confirmar sua resposta.\n\n『❌』Para cancelar o formulário, clique em \"❌ Cancelar\".\n\n『<a:a_Alert:1063858446853734490>』**Atenção:** todas as respostas precisam obrigatoriamente ser respondidas **sinceramente**. Caso contrário, seu formulário será recusado!",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            parceriaFormEmbed.add_field(name = f"**『✍』Qual o ID do seu servidor?**", value = "`Não informado`", inline = False)
            parceriaFormEmbed.set_footer(text = f"Formulário de {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            ticketUser = interaction.user
            await parceriaFormChannel.send(content = f"『<a:ab_YellowDiamond:938857668888645673>』Bem-vindo(a), {interaction.user.mention}!", embed = parceriaFormEmbed, view = parceriaForm1Row(self.bot, parceriaFormEmbed, self.json, ticketUser))
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

class parceriaForm1Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def parceriaAnswer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(parceriaForm1Modal(self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceria1Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.embed.fields[0].value == "`Não informado`":
                parceriaMissingAnswer1Embed = discord.Embed(
                    title = f"꧁🤝 Parceria 🤝꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(230, 170, 10)
                )
                parceriaMissingAnswer1Embed.set_footer(text = "Parcerias!")
                await interaction.response.send_message(embed = parceriaMissingAnswer1Embed, ephemeral = True)
                return
            self.embed.add_field(name = "**『✍』Seu servidor tem mais de 100 membros (sem contar os bots)?**", value = "`Não informado`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = parceriaForm2Row(self.bot, self.embed, self.json, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceria1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.edit(view = None)
            answerConfirmEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『❌』Seu formulário foi cancelado com sucesso!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerConfirmEmbed.set_footer(text = "Parcerias!")
            await interaction.response.send_message(embeds = [answerConfirmEmbed], ephemeral = True)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            answerAdminsEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『❌』{interaction.user.mention} cancelou o formulário!",
                color = discord.Color.from_rgb(200, 20, 20)
            )
            answerAdminsEmbed.set_footer(text = "Parcerias!")
            await interaction.channel.send(embeds = [answerAdminsEmbed])
        except Exception as e:
            print(e)

class parceriaForm2Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaForm2Yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 1, name = "『☑』Seu servidor tem mais de 100 membros (sem contar os bots)?", value = "`Sim`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor possui um cargo exclusivo para parceiros?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm3Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceriaForm2No(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 1, name = "『☑』Seu servidor tem mais de 100 membros (sem contar os bots)?", value = "`Não`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor possui um cargo exclusivo para parceiros?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm3Row(self.bot, self.embed, self.json, self.user))
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm2Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 1)
        self.embed.set_field_at(index = 0, name = "**『✍』Qual o ID do seu servidor?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm1Row(self.bot, self.embed, self.json, self.user))

class parceriaForm3Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaForm3Yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 2, name = "『☑』Seu servidor possui um cargo exclusivo para parceiros?", value = "`Sim`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor possui um canal para divulgações?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm4Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceriaForm3No(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 2, name = "『☑』Seu servidor possui um cargo exclusivo para parceiros?", value = "`Não`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor possui um canal para divulgações?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm4Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm3Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 2)
        self.embed.set_field_at(index = 1, name = "**『✍』Seu servidor tem mais de 100 membros (sem contar os bots)?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm2Row(self.bot, self.embed, self.json, self.user))

class parceriaForm4Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaForm4Yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 3, name = "『☑』Seu servidor possui um canal para divulgações?", value = "`Sim`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor tem um cargo para avisar os membros sobre as parceiras?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm5Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceriaForm4No(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 3, name = "『☑』Seu servidor possui um canal para divulgações?", value = "`Não`", inline = False)
        self.embed.add_field(name = "**『✍』Seu servidor tem um cargo para avisar os membros sobre as parceiras?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm5Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm4Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 3)
        self.embed.set_field_at(index = 2, name = "**『✍』Seu servidor possui um cargo exclusivo para parceiros?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm3Row(self.bot, self.embed, self.json, self.user))

class parceriaForm5Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaForm5Yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 4, name = "『☑』Seu servidor tem um cargo para avisar os membros sobre as parceiras?", value = "`Sim`", inline = False)
        self.embed.add_field(name = "**『✍』Qual a sua posição no servidor?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm6Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceriaForm5No(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 4, name = "『☑』Seu servidor tem um cargo para avisar os membros sobre as parceiras?", value = "`Não`", inline = False)
        self.embed.add_field(name = "**『✍』Qual a sua posição no servidor?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm6Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm5Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 4)
        self.embed.set_field_at(index = 3, name = "**『✍』Seu servidor possui um canal para divulgações?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm4Row(self.bot, self.embed, self.json, self.user))

class parceriaForm6Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Dono", style = discord.ButtonStyle.gray, emoji = "👑")
    async def parceriaForm6Option1(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 5, name = "『☑』Qual a sua posição no servidor?", value = "`Dono`", inline = False)
        self.embed.add_field(name = "**『✍』Nos conte um pouco sobre o seu servidor:**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm7Row(self.bot, self.embed, self.json, self.user))
    
    @discord.ui.button(label = f"Administrador", style = discord.ButtonStyle.gray, emoji = "🛡")
    async def parceriaForm6Option2(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 5, name = "『☑』Qual a sua posição no servidor?", value = "`Administrador`", inline = False)
        self.embed.add_field(name = "**『✍』Nos conte um pouco sobre o seu servidor:**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm7Row(self.bot, self.embed, self.json, self.user))
    
    @discord.ui.button(label = f"Moderador", style = discord.ButtonStyle.gray, emoji = "🚔")
    async def parceriaForm6Option3(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 5, name = "『☑』Qual a sua posição no servidor?", value = "`Moderador`", inline = False)
        self.embed.add_field(name = "**『✍』Nos conte um pouco sobre o seu servidor:**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm7Row(self.bot, self.embed, self.json, self.user))
    
    @discord.ui.button(label = f"Outro", style = discord.ButtonStyle.gray, emoji = "👤")
    async def parceriaForm6Option4(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.set_field_at(index = 5, name = "『☑』Qual a sua posição no servidor?", value = "`Outro`", inline = False)
        self.embed.add_field(name = "**『✍』Nos conte um pouco sobre o seu servidor:**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm7Row(self.bot, self.embed, self.json, self.user))

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm6Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 5)
        self.embed.set_field_at(index = 4, name = "**『✍』Seu servidor tem um cargo para avisar os membros sobre as parceiras?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm5Row(self.bot, self.embed, self.json, self.user))

class parceriaForm7Row(discord.ui.View):
    def __init__(self, bot, embed, json, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
        self.user = user
    
    @discord.ui.button(label = f"Responder", style = discord.ButtonStyle.blurple, emoji = "✍")
    async def parceriaSendModal7(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(parceriaForm7Modal(self.embed))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaConfirmAnswers7(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            print(self.embed.fields[6].value)
            if self.embed.fields[6].value == "`Não informado`":
                parceriaMissingAnswer7Embed = discord.Embed(
                    title = f"꧁🤝 Parceria 🤝꧂",
                    description = "Você precisa responder a pergunta acima!",
                    color = discord.Color.from_rgb(230, 170, 10)
                )
                parceriaMissingAnswer7Embed.set_footer(text = "Parcerias!")
                await interaction.response.send_message(embed = parceriaMissingAnswer7Embed, ephemeral = True)
                return
            parceriaFinishConfirmEmbed = discord.Embed(
                    title = f"꧁🤝 Parceria 🤝꧂",
                    description = "Você tem certeza de que todas as respostas estão corretas? Uma vez que confirmar as respostas, não será possível alterá-las!",
                    color = discord.Color.from_rgb(230, 170, 10)
                )
            parceriaFinishConfirmEmbed.set_footer(text = "Parcerias!")
            await interaction.response.send_message(embed = parceriaFinishConfirmEmbed, view = parceriaFinishConfirmRow(self.bot, self.embed, self.json), ephemeral = True)
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "◀")
    async def parceriaForm7Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed.remove_field(index = 6)
        self.embed.set_field_at(index = 5, name = "**『✍』Qual a sua posição no servidor?**", value = "`Não informado`", inline = False)
        await interaction.response.defer()
        await interaction.message.edit(embed = self.embed, view = parceriaForm6Row(self.bot, self.embed, self.json, self.user))

class parceriaForm1Modal(discord.ui.Modal, title = "Formulário para parcerias"):
    def __init__(self, embed):
        super().__init__(timeout = None)
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = "ID do servidor:",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 20,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 0, name = "『☑』Qual o ID do seu servidor?", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class parceriaForm7Modal(discord.ui.Modal, title = "Formulário para parcerias"):
    def __init__(self, embed):
        super().__init__(timeout = None)
        self.embed = embed

        self.add_item(discord.ui.TextInput(
            label = "Nos conte um pouco sobre o seu servidor:",
            style = discord.TextStyle.paragraph,
            min_length = 1,
            max_length = 1000,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            answer0 = self.children[0].value
            self.embed.set_field_at(index = 6, name = "『☑』Nos conte um pouco sobre o seu servidor:", value = f"{answer0}", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embeds = [self.embed])
        except Exception as e:
            print(e)

class parceriaFinishConfirmRow(discord.ui.View):
    def __init__(self, bot, embed, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.json = json
    
    @discord.ui.button(label = f"Sim!", style = discord.ButtonStyle.green, emoji = "✅")
    async def parceriaFinishYes(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.embed.color = discord.Color.from_rgb(20, 200, 20)
            repliedMsg = await interaction.channel.fetch_message(interaction.message.reference.message_id)
            await repliedMsg.edit(embed = self.embed, view = None)
            parceriaOpenedEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📃』Suas respostas foram enviadas! Entraremos em contato com você caso seja aprovado.",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            parceriaOpenedEmbed.set_footer(text = "Parcerias!")
            await interaction.response.edit_message(embed = parceriaOpenedEmbed, view = None)
            userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
            userOverwrites.read_messages, userOverwrites.send_messages = False, False
            await interaction.channel.set_permissions(interaction.user, overwrite = userOverwrites)
            parceriaFormEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『📄』{interaction.user.mention} terminou o formulário!",
                color = discord.Color.from_rgb(20, 200, 20)
            )
            await interaction.channel.send(embed = parceriaFormEmbed)
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def parceriaFinishNo(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            canceledFinishedEmbed = discord.Embed(
                title = f"꧁🤝 Parceria 🤝꧂",
                description = f"『❌』Envio cancelado!",
                color = discord.Color.from_rgb(230, 170, 10)
            )
            canceledFinishedEmbed.set_footer(text = "Parcerias!")
            await interaction.response.edit_message(embed = canceledFinishedEmbed, view = None)
            return
        except Exception as e:
            print(e)


async def getTicketParceriaRow(bot):
    try:
        c = open("../jsons/ticket.json", encoding = "utf8")
        ticketJson = json.load(c)
        channel = bot.get_channel(ticketJson["parceriaChannel"])
        ticketMsg = await channel.fetch_message(ticketJson["parceriaTicket"])
        parceriaDescriptionEmbed = discord.Embed(
            title = f"꧁<a:ab_RightArrow:939177432127246427> SEJA UM PARCEIRO <a:ab_LeftArrow:939177402381246514>꧂",
            description =
"""
*Gostaria de fazer uma parceria com o nosso servidor. Então esta é a hora! Basta clicar no botão \"🤝 Pedir parceria\", responder ao nosso formulário e aguardar uma resposta, dizendo se o seu servidor foi aprovado para parceria, ou não e os motivos.*
""",
            color = discord.Color.from_rgb(230, 170, 10)
        )
        parceriaDescriptionEmbed.add_field(name = "『🔰』Requisitos mínimos:", inline = False, value =
"""
➺ O responsável pela parceria precisa obrigatoriamente permanecer neste servidor;
➺ Ter no mínimo 100 membros (sem contar os bots). (Não fazemos parcerias com servidores recém-criados e com mais bots do que pessoas!)
➺ Ter o bot <@911002921594925056> adicionado em seu servidor.
Obs: Caso tenha problemas em adicioná-lo, entre em contato com <@656295512219058196>.
➺ Ter um cargo e um canal para anunciar as parcerias.
Exemplo:
⇀ <#750017382734495775> (Canal para avisos de parcerias)
⇁ <@&979920562883268638> (Cargo para avisar os membros sobre parcerias
"""
        )
        parceriaDescriptionEmbed.add_field(name = "『⚠』Atenção:", inline = False, value =
"""
Responda as perguntas sinceramente. Todas as informações do formulário serão analisadas para comprovar se são verídicas, então não dê informações erradas e/ou falsas em nenhuma das perguntas! Nenhuma das informações do formulário serão compartilhadas com outros usuários ou terceiros, apenas os administradores do servidor terão acesso as informações.
"""
        )
        parceriaDescriptionEmbed.set_image(url = "https://i.imgur.com/rD4teJy.png")
        parceriaDescriptionEmbed.set_footer(text = "Parcerias!", icon_url = bot.user.display_avatar.url)
        await ticketMsg.edit(content = None, embed = parceriaDescriptionEmbed, view = parceriaRequestEntryRow(bot = bot, json = ticketJson))
    except Exception as e:
        print(e)