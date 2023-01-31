import discord
import asyncio
import datetime
import json


async def antiLongMessages(bot, message):
    try:
        print(len(message.content))
        if len(message.content) >= 1000:
            c = open("../jsons/antiLongMessages.json", encoding = "utf8")
            antiLongMessagesJson = json.load(c)
            rolesIds = []
            for role in message.author.roles:
                rolesIds.append(int(role.id))
            for allowedRole in antiLongMessagesJson['allowedRoles']:
                if allowedRole in rolesIds:
                    print("AntiLongMessages desativado por cargo")
                    return
            if message.channel.id in antiLongMessagesJson['allowedChannels']:
                print("AntiLongMessages desativado por canal")
                return
            foundLongMessage = message.content[:1000]
            #await message.delete()
            await message.add_reaction("🧐")
            antiInviteWarnMessage = await message.channel.send(f"『🟢』{message.author.mention}, não envie mensagens muito longas fora do <#931019005609779220>!")
            antiChannel = bot.get_channel(antiLongMessagesJson["antiChannel"])
            antiEmbed = discord.Embed(
                color = discord.Color.from_rgb(20, 200, 20),
                timestamp = datetime.datetime.utcnow()
            )
            antiEmbed.set_author(name = "『💬』Mensagem muito longa:", icon_url= bot.user.display_avatar.url)
            antiEmbed.add_field(name = f"『💬』Enviado em {message.channel.name}:", value = f"{foundLongMessage}", inline = False)
            antiEmbed.add_field(name = "『📃』Detalhes:", value = f"`{len(message.content)} caracteres`", inline = False)
            antiEmbed.add_field(name = "『👤』Usuário:", value = f"{message.author.mention} `({message.author.id})`", inline = False)
            antiEmbed.set_thumbnail(url = message.author.display_avatar.url)
            antiEmbed.set_footer(text = f"『🟢』「R.2」Mensagens desnecessariamente longas", icon_url = bot.user.display_avatar.url)
            try:
                await message.author.timeout(datetime.timedelta(hours = 1))
                antiEmbed.add_field(name = "『🧑‍⚖️』Punição aplicada:", value = f"`Mute de 1 hora`", inline = False)
            except Exception as e:
                antiEmbed.add_field(name = "『❌』Erro:", value = f"`{e}`", inline = False)
            antiSpamAlertMessage = await antiChannel.send(content = "『🚨』<@&789133849841106994> <@&739210760567390250>", embeds = [antiEmbed], view = antiInviteRow(bot, message, antiLongMessagesJson))
            try:
                antiDMEmbed = discord.Embed(
                    title = "Você foi silenciado!",
                    color = discord.Color.from_rgb(20, 200, 20),
                    timestamp = datetime.datetime.utcnow()
                )
                antiDMEmbed.add_field(name = f"『🚨』Motivo:", value = f"`Mensagem excessivamente longa no `{message.channel.mention}", inline = False)
                antiDMEmbed.add_field(name = "『📃』Mensagem:", value = f"`{foundLongMessage}`", inline = False)
                antiDMEmbed.add_field(name = "『🔇』Silenciado por:", value = f"`1 hora`", inline = False)
                antiDMEmbed.set_thumbnail(url = message.author.display_avatar.url)
                antiDMEmbed.set_footer(text = f"『🟢』Leia a regra nº 2: Mensagens desnecessáriamente longas", icon_url = bot.user.display_avatar.url)
                await message.author.send(embeds = [antiDMEmbed])
            except Exception as e:
                print(e)
            await asyncio.sleep(10)
            await antiInviteWarnMessage.delete()
            await asyncio.sleep(3600)
            await antiSpamAlertMessage.edit(view = None)
    except Exception as e:
        print(e)

class antiInviteRow(discord.ui.View):
    def __init__(self, bot, message, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.message = message
        self.json = json
    
    @discord.ui.button(label = f"Desilenciar", style = discord.ButtonStyle.gray, emoji = "💬")
    async def antiInviteMuteInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            timeZone = datetime.timedelta(hours = -3)
            antiMuteEmbed = discord.Embed(
                title = f"Mute removido!",
                color = discord.Color.from_rgb(20, 200, 20),
                timestamp = datetime.datetime.now()
            )
            antiMuteEmbed.set_author(name = "『💬』Mensagem longa:", icon_url= self.bot.user.display_avatar.url)
            antiMuteEmbed.add_field(name = "『🧑‍⚖️』Punição removida:", value = f"`Mute de 1 hora`", inline = False)
            antiMuteEmbed.set_thumbnail(url = self.message.author.display_avatar.url)
            antiMuteEmbed.set_footer(text = f"『🟢』「R.2」Mensagens desnecessariamente longas", icon_url = self.bot.user.display_avatar.url)
            await self.message.author.timeout(datetime.timedelta(seconds = 0))
            await interaction.message.edit(view = None)
            await interaction.message.reply(embed = antiMuteEmbed)
        except Exception as e:
            print(e)
            antiMuteEmbed = discord.Embed(
                title = f"Houve um erro!",
                description = f"`{e}`",
                color = discord.Color.from_rgb(200, 20, 20),
                timestamp = datetime.datetime.now()
            )
            antiMuteEmbed.set_author(name = "『🚨』Mensagem longa:", icon_url= self.bot.user.display_avatar.url)
            antiMuteEmbed.set_thumbnail(url = self.message.author.display_avatar.url)
            await interaction.response.send_message(embed = antiMuteEmbed, ephemeral = False)