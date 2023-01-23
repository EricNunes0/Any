import discord
import asyncio
import datetime
import json

timeMilliseconds = 5 * 1000
maxMessages = 5
authorMsgTimes = {}

async def antiSpam(bot, message):
    try:
        global author_msg_counts
        currentTime = datetime.datetime.now().timestamp() * 1000
        if not authorMsgTimes.get(message.author.id, False):
            authorMsgTimes[message.author.id] = []
        authorMsgTimes[message.author.id].append(currentTime)
        expiresTime = currentTime - timeMilliseconds
        expiredMessages = [
            msgTime for msgTime in authorMsgTimes[message.author.id]
            if msgTime < expiresTime
        ]
        for msgTime in expiredMessages:
            authorMsgTimes[message.author.id].remove(msgTime)
        print(len(authorMsgTimes[message.author.id]), maxMessages)
        if len(authorMsgTimes[message.author.id]) > maxMessages:
            authorMsgTimes.clear()
            c = open("../jsons/antiSpam.json", encoding = "utf8")
            antiSpamJson = json.load(c)
            rolesIds = []
            for role in message.author.roles:
                rolesIds.append(int(role.id))
            for allowedRole in antiSpamJson['allowedRoles']:
                if allowedRole in rolesIds:
                    print("Anti-desativado por cargo")
                    return
            if message.channel.id in antiSpamJson['allowedChannels']:
                print("Anti-desativado por canal")
                return
            inviteFoundMessage = message.content[:1000]
            await message.delete()
            antiInviteWarnMessage = await message.channel.send(f"『🟢』{message.author.mention}, você não pode spamar mensagens fora do <#931019005609779220>!")
            antiChannel = bot.get_channel(antiSpamJson["antiChannel"])
            antiEmbed = discord.Embed(
                color = discord.Color.from_rgb(20, 200, 20),
                timestamp = datetime.datetime.utcnow()
            )
            antiEmbed.set_author(name = "『💬』Anti-spam:", icon_url= bot.user.display_avatar.url)
            antiEmbed.add_field(name = f"『💬』Spam em {message.channel.mention}:", value = f"{inviteFoundMessage}", inline = False)
            antiEmbed.add_field(name = "『📃』Detalhes:", value = f"`{len(authorMsgTimes[message.author.id])} mensagens enviadas em menos de {int(timeMilliseconds / 1000)} segundos`", inline = False)
            antiEmbed.add_field(name = "『👤』Infrator:", value = f"{message.author.mention} `({message.author.id})`", inline = False)
            antiEmbed.set_thumbnail(url = message.author.display_avatar.url)
            antiEmbed.set_footer(text = f"『🟢』「R.1」Flood/spam de mensagens/emojis", icon_url = bot.user.display_avatar.url)
            try:
                await message.author.timeout(datetime.timedelta(hours = 1))
                antiEmbed.add_field(name = "『🧑‍⚖️』Punição aplicada:", value = f"`Mute de 1 hora`", inline = False)
            except Exception as e:
                antiEmbed.add_field(name = "『❌』Erro:", value = f"`{e}`", inline = False)
            antiSpamAlertMessage = await antiChannel.send(content = "『🚨』<@&789133849841106994> <@&739210760567390250>", embeds = [antiEmbed], view = antiInviteRow(bot, message, antiSpamJson))
            try:
                antiDMEmbed = discord.Embed(
                    title = "Você foi silenciado!",
                    color = discord.Color.from_rgb(20, 200, 20),
                    timestamp = datetime.datetime.utcnow()
                )
                antiDMEmbed.add_field(name = f"『🚨』Motivo:", value = f"`Flood/spam de mensagens no `{message.channel.mention}", inline = False)
                antiDMEmbed.add_field(name = "『📃』Spam:", value = f"`{len(authorMsgTimes[message.author.id])} mensagens enviadas em menos de {int(timeMilliseconds / 1000)} segundos`", inline = False)
                antiDMEmbed.add_field(name = "『🔇』Silenciado por:", value = f"`1 hora`", inline = False)
                antiDMEmbed.set_thumbnail(url = message.author.display_avatar.url)
                antiDMEmbed.set_footer(text = f"『🟢』Leia a regra nº 1: Flood/spam de mensagens/emojis", icon_url = bot.user.display_avatar.url)
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
            antiMuteEmbed.set_author(name = "『💬』Anti-spam:", icon_url= self.bot.user.display_avatar.url)
            antiMuteEmbed.add_field(name = "『🧑‍⚖️』Punição removida:", value = f"`Mute de 1 hora`", inline = False)
            antiMuteEmbed.set_thumbnail(url = self.message.author.display_avatar.url)
            antiMuteEmbed.set_footer(text = f"『🟢』「R.1」Flood/spam de mensagens/emojis", icon_url = self.bot.user.display_avatar.url)
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
            antiMuteEmbed.set_author(name = "『🚨』Anti-invite:", icon_url= self.bot.user.display_avatar.url)
            antiMuteEmbed.set_thumbnail(url = self.message.author.display_avatar.url)
            await interaction.response.send_message(embed = antiMuteEmbed, ephemeral = False)