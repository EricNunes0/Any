import discord
import asyncio
import datetime
import dotenv
import json
import os
import requests

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

async def antiInvite(bot, message):
    try:
        c = open("../jsons/antiInvite.json", encoding = "utf8")
        antiInviteJson = json.load(c)
        for antiInviteText in antiInviteJson['links']:
            if antiInviteText in message.content:
                rolesIds = []
                for role in message.author.roles:
                    print(int(role.id))
                    rolesIds.append(int(role.id))
                for allowedRole in antiInviteJson['allowedRoles']:
                    if allowedRole in rolesIds:
                        print("STAR WALKIN\'")
                        return
                inviteFoundMessage = message.content[:1000]
                await message.delete()
                antiInviteWarnMessage = await message.channel.send(f"『🔴』{message.author.mention}, você não pode enviar convites de outros servidores sem permissão!")
                antiChannel = bot.get_channel(antiInviteJson["antiChannel"])
                antiEmbed = discord.Embed(
                    color = discord.Color.from_rgb(200, 20, 20),
                    timestamp = datetime.datetime.utcnow()
                )
                antiEmbed.set_author(name = "『🚨』Anti-invite:", icon_url= bot.user.display_avatar.url)
                antiEmbed.add_field(name = "『💬』Mensagem:", value = f"{inviteFoundMessage}", inline = False)
                antiEmbed.add_field(name = "『👤』Infrator:", value = f"{message.author.mention} `({message.author.id})`", inline = False)
                antiEmbed.add_field(name = "『🧑‍⚖️』Punição padrão:", value = f"`Mute de 3 dias`", inline = False)
                antiEmbed.set_thumbnail(url = message.author.display_avatar.url)
                antiEmbed.set_footer(text = f"『🔴』「R.11」Divulgação de servidores", icon_url = bot.user.display_avatar.url)
                await antiChannel.send(content = "『🚨』<@&789133849841106994> <@&739210760567390250>", embeds = [antiEmbed], view = antiInviteRow(bot, message, antiInviteJson))
                await asyncio.sleep(10)
                await antiInviteWarnMessage.delete()
                break
    except Exception as e:
        print(e)

class antiInviteRow(discord.ui.View):
    def __init__(self, bot, message, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.message = message
        self.json = json
    
    @discord.ui.button(label = f"Silenciar", style = discord.ButtonStyle.gray, emoji = "🔇")
    async def antiInviteMuteInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            timeZone = datetime.timedelta(hours = -3)
            antiMuteEmbed = discord.Embed(
                title = f"Usuário silenciado!",
                color = discord.Color.from_rgb(200, 20, 20),
                timestamp = datetime.datetime.now()
            )
            antiMuteEmbed.set_author(name = "『🚨』Anti-invite:", icon_url= self.bot.user.display_avatar.url)
            antiMuteEmbed.add_field(name = "『🧑‍⚖️』Punição aplicada:", value = f"`Mute de 3 dias`", inline = False)
            antiMuteEmbed.set_thumbnail(url = self.message.author.display_avatar.url)
            antiMuteEmbed.set_footer(text = f"『🔴』「R.11」Divulgação de servidores", icon_url = self.bot.user.display_avatar.url)
            await self.message.author.timeout(datetime.timedelta(days = 3))
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