import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from mongoconnection.vip import *

c = open("../config.json")
config = json.load(c)

l = open("../link.json")
link = json.load(l)

intents = discord.Intents.default()
intents.members = True

prefix = config["prefix"]
bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec = 0, per_min = 0, per_hour = 0, type = commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

def invalidUserInteraction(collectedUser, allowedUser):
    noPerm = discord.Embed(
        title = f"Sem VIP!",
        description = f"『❌』Apenas {allowedUser.mention} pode configurar este VIP!",
        color = 0xFF0000
    )
    noPerm.set_thumbnail(url = link["error"])
    noPerm.set_footer(text = f"Pedido por {collectedUser.name}", icon_url = collectedUser.display_avatar.url)
    return noPerm

vipNames = ["Ametista", "Jade", "Safira"]
vipRoles = [1051948366461939744, 1047268770504253561, 1047268807812595802]
vipEmojis = ["<a:ab_PurpleDiamond:938883672717787196>", "<a:ab_GreenDiamond:938880803692240927>", "<a:ab_BlueDiamond:938850305083314207>"]

def convertTime(arg0, arg1 = None):
    arg0 = arg0.lower()
    if arg1 == None:
        if arg0.endswith("s") or arg0.endswith("m") or arg0.endswith("h") or arg0.endswith("d"):
            t = arg0[:-1]
            t = int(t)
            print(t)
            if arg0.endswith("s"):
                c = t
            if arg0.endswith("m"):
                c = t * 60
            if arg0.endswith("h"):
                c = t * 3600
            if arg0.endswith("d"):
                c = t * (3600 * 24)
            return c
        else:
            return int(arg0)

class setVipForm1(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Usuário", style = discord.ButtonStyle.blurple, emoji = "👤")
    async def setvipAnswer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.send_modal(setVipModal1(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip1Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            if self.embed.fields[0].value == "`Não informado`":
                setvipMissingEmbed1 = discord.Embed(
                    description = "Informe o usuário!",
                    color = discord.Color.from_rgb(220, 20, 255)
                )
                await interaction.response.send_message(embed = setvipMissingEmbed1, ephemeral = True)
                return
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm2(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip1Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm2(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Ametista", style = discord.ButtonStyle.blurple, emoji = "<a:ab_PurpleDiamond:938883672717787196>")
    async def setvip2Option1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            self.config["vip"] = 0
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[0])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.add_roles(vipRoleFound)
            self.embed.set_field_at(index = 1, name = "『<a:ab_PurpleDiamond:938883672717787196>』VIP selecionado:", value = f"`{vipNames[0]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Jade", style = discord.ButtonStyle.blurple, emoji = "<a:ab_GreenDiamond:938880803692240927>")
    async def setvip2Option2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            self.config["vip"] = 1
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[1])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.add_roles(vipRoleFound)
            self.embed.set_field_at(index = 1, name = "『<a:ab_GreenDiamond:938880803692240927>』VIP selecionado:", value = f"`{vipNames[1]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)
    
    @discord.ui.button(label = f"Safira", style = discord.ButtonStyle.blurple, emoji = "<a:ab_BlueDiamond:938850305083314207>")
    async def setvip2Option3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            self.config["vip"] = 2
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[2])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.add_roles(vipRoleFound)
            self.embed.set_field_at(index = 1, name = "『<a:ab_BlueDiamond:938850305083314207>』VIP selecionado:", value = f"`{vipNames[2]}`", inline = False)
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "↩")
    async def setvip2Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            self.config["vip"] = "`Não informado`"
            self.config["user"] = "`Não informado`"
            self.embed.set_field_at(index = 1, name = "『💎』Vip selecionado:", value = f"`Não informado`", inline = False)
            self.embed.set_field_at(index = 0, name = "『👤』Usuário:", value = f"`Não informado`", inline = False)
            print(self.config)
            await interaction.message.edit(embed = self.embed, view = setVipForm1(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip2Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm3(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Duração", style = discord.ButtonStyle.blurple, emoji = "⏰")
    async def setvip3Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.send_modal(setVipModal3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip3Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            if self.embed.fields[2].value == "`Não informado`":
                setvipMissingEmbed1 = discord.Embed(
                    description = "Informe a duração!",
                    color = discord.Color.from_rgb(220, 20, 255)
                )
                await interaction.response.send_message(embed = setvipMissingEmbed1, ephemeral = True)
                return
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm4(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "↩")
    async def setvip3Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[self.config["vip"]])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.remove_roles(vipRoleFound)
            self.config["endsAt"] = "`Não informado`"
            self.config["vip"] = "`Não informado`"
            self.embed.set_field_at(index = 2, name = "『⏰』Duração:", value = f"`Não informado`", inline = False)
            self.embed.set_field_at(index = 1, name = "『💎』Vip selecionado:", value = f"`Não informado`", inline = False)
            print(self.config)
            await interaction.message.edit(embed = self.embed, view = setVipForm2(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip3Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[self.config["vip"]])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.remove_roles(vipRoleFound)
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)

        except Exception as e:
            print(e)

class setVipForm4(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Cargo", style = discord.ButtonStyle.gray, emoji = "💼")
    async def setvip4Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.send_modal(setVipModal4(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip4Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            if self.embed.fields[3].value == "`Não informado`":
                self.config["role"] = "`Não informado`"
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm5(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "↩")
    async def setvip4Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            self.config["endsAt"] = "`Não informado`"
            self.embed.set_field_at(index = 2, name = "『⏰』Duração:", value = f"`Não informado`", inline = False)
            print(self.config)
            await interaction.message.edit(embed = self.embed, view = setVipForm3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip4Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[self.config["vip"]])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.remove_roles(vipRoleFound)
            if self.config["role"] != "`Não informado`":
                vipExclusiveRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(self.config["role"]))
                await vipExclusiveRoleFound.delete()
                
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm5(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Canal", style = discord.ButtonStyle.gray, emoji = "🔊")
    async def setvip5Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.send_modal(setVipModal5(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip5Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            if self.embed.fields[4].value == "`Não informado`":
                self.config["channel"] = "`Não informado`"
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm6(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "↩")
    async def setvip5Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            print(self.config)
            await interaction.message.edit(embed = self.embed, view = setVipForm4(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip5Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[self.config["vip"]])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.remove_roles(vipRoleFound)
            if self.config["role"] != "`Não informado`":
                vipExclusiveRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(self.config["role"]))
                await vipExclusiveRoleFound.delete()
            if self.config["channel"] != "`Não informado`":
                vipExclusiveChannelFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).voice_channels, id = int(self.config["channel"]))
                await vipExclusiveChannelFound.delete()
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipForm6(discord.ui.View):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user
    
    @discord.ui.button(label = f"Novo amigo", style = discord.ButtonStyle.gray, emoji = "➕")
    async def setvip6Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.send_modal(setVipModal6(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Confirmar", style = discord.ButtonStyle.green, emoji = "✅")
    async def setvip6Confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = None)
            if self.config["role"] == "`Não informado`":
                self.config["role"] = None
            if self.config["channel"] == "`Não informado`":
                self.config["channel"] = None
            dbname = getDatabase()
            collectionName = dbname["vip"]
            newVip = {
                "User": self.config["user"],
                "Vip": self.config["vip"],
                "EndsAt": self.config["endsAt"],
                "Role": self.config["role"],
                "Channel": self.config["channel"],
                "Friends": self.config["friends"]
            }
            newProfile = collectionName.insert_one(newVip)
            await interaction.message.add_reaction("✅")
            return newProfile
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Voltar", style = discord.ButtonStyle.blurple, emoji = "↩")
    async def setvip6Return(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            await interaction.response.defer()
            await interaction.message.edit(embed = self.embed, view = setVipForm5(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌")
    async def setvip6Cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            invalidUserEmbed = invalidUserInteraction(interaction.user, self.user)
            await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
            return
        try:
            vipRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = vipRoles[self.config["vip"]])
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
            await user.remove_roles(vipRoleFound)
            if self.config["role"] != "`Não informado`":
                vipExclusiveRoleFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(self.config["role"]))
                await vipExclusiveRoleFound.delete()
            if self.config["channel"] != "`Não informado`":
                vipExclusiveChannelFound = discord.utils.get(self.bot.get_guild(interaction.guild.id).voice_channels, id = int(self.config["channel"]))
                await vipExclusiveChannelFound.delete()
            await interaction.message.edit(view = None)
            setvipCancelEmbed = discord.Embed(
                description = f"『❌』Configuração de VIP encerrada!",
                color = discord.Color.from_rgb(200, 20, 255)
            )
            await interaction.response.send_message(embeds = [setvipCancelEmbed], ephemeral = True)
        except Exception as e:
            print(e)

class setVipModal1(discord.ui.Modal, title = "Configurar VIP:"):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = "ID do usuário:",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 50,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        answer0 = self.children[0].value
        dbname = getDatabase()
        collectionName = dbname["vip"]
        vip = collectionName.find_one({"User": int(answer0)})
        print(vip)
        if vip != None:
            alreadyVip = discord.Embed(
                title = f"VIP encontrado!",
                description = f"『❌』Este usuário já possui um plano VIP ativo no momento!",
                color = 0xFF0000
            )
            alreadyVip.set_thumbnail(url = link["error"])
            await interaction.response.send_message(embed = alreadyVip, ephemeral = True)
            return
        await interaction.response.defer()
        try:
            user = await self.bot.fetch_user(answer0)
            self.embed.set_field_at(index = 0, name = "『👤』Usuário:", value = f"{user.mention} `({user.id})`", inline = False)
            self.config["user"] = user.id
            print(self.config)
        except Exception as e:
            print(e)
            self.embed.set_field_at(index = 0, name = "『👤』Usuário:", value = f"`Não informado`", inline = False)
        await interaction.message.edit(embeds = [self.embed])

class setVipModal3(discord.ui.Modal, title = "Editar duração:"):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = f"Duração (s/m/h/d):",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            time = self.children[0].value
            self.time = convertTime(time)
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            self.config["endsAt"] = int((timeStamp)) + self.time
            print(self.config)
            await interaction.response.send_message(content = f"Duração alterada para {self.time} segundos!", ephemeral = True)
            self.embed.set_field_at(index = 2, name = "『⏰』Duração:", value = f"{time} (<t:{int((timeStamp)) + self.time}>)", inline = False)
            await interaction.message.edit(embeds = [self.embed], view = setVipForm3(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

class setVipModal4(discord.ui.Modal, title = "Cargo próprio:"):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = f"Nome do cargo:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )

        self.add_item(discord.ui.TextInput(
            label = f"RGB (0 100 255):",
            style = discord.TextStyle.short,
            min_length = 1,
            max_length = 20,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            roleName = self.children[0].value
            roleColorInput = self.children[1].value
            roleColor = roleColorInput.split(" ")
            r = int(roleColor[0])
            g = int(roleColor[1])
            b = int(roleColor[2])
            if self.config["role"] == "`Não informado`":
                createdRole = await interaction.guild.create_role(name = roleName, color = discord.Color.from_rgb(r = r, g = g, b = b))
                user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = self.config["user"])
                await user.add_roles(createdRole)
                self.config["role"] = f"{createdRole.id}"
                await interaction.response.send_message(content = f"Cargo criado: {createdRole.mention}", ephemeral = True)
                self.embed.set_field_at(index = 3, name = "『💼』Cargo próprio:", value = createdRole.mention, inline = False)
            else:
                foundRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(self.config["role"]))
                editedRole = await foundRole.edit(name = roleName, color = discord.Color.from_rgb(r = r, g = g, b = b))
                self.config["role"] = editedRole.id
                await interaction.response.send_message(content = f"Cargo editado: {editedRole.mention}", ephemeral = True)
                self.embed.set_field_at(index = 3, name = "『💼』Cargo próprio:", value = editedRole.mention, inline = False)
            print(self.config)
            await interaction.message.edit(embeds = [self.embed], view = setVipForm4(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

class setVipModal5(discord.ui.Modal, title = "Canal próprio:"):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = f"Nome do canal:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            channelName = self.children[0].value
            user = await self.bot.fetch_user(self.config["user"])
            vipCategorie = discord.utils.get(interaction.guild.categories, id = 723156857132285994)
            if self.config["channel"] == "`Não informado`":
                vipChannel = await interaction.guild.create_voice_channel(
                name = channelName,
                category = vipCategorie
                )
                serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                serverOverwrites.view_channel, serverOverwrites.send_messages, serverOverwrites.speak, serverOverwrites.connect = True, False, False, False
                userOverwrites.view_channel, userOverwrites.send_messages, userOverwrites.speak, userOverwrites.connect = True, True, True, True
                await vipChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
                await vipChannel.set_permissions(user, overwrite = userOverwrites)
                self.config["channel"] = f"{vipChannel.id}"
                await interaction.response.send_message(content = f"Cargo criado: {vipChannel.mention}", ephemeral = True)
                self.embed.set_field_at(index = 4, name = "『🔊』Canal próprio:", value = vipChannel.mention, inline = False)
            else:
                vipChannel = discord.utils.get(self.bot.get_guild(interaction.guild.id).voice_channels, id = int(self.config["channel"]))
                await vipChannel.edit(name = channelName, category = vipCategorie)
                serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                serverOverwrites.view_channel, serverOverwrites.send_messages, serverOverwrites.speak, serverOverwrites.connect = True, False, False, False
                userOverwrites.view_channel, userOverwrites.send_messages, userOverwrites.speak, userOverwrites.connect = True, True, True, True
                await vipChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
                await vipChannel.set_permissions(user, overwrite = userOverwrites)
                self.config["channel"] = f"{vipChannel.id}"
                await interaction.response.send_message(content = f"Cargo editado: {vipChannel.mention}", ephemeral = True)
                self.embed.set_field_at(index = 4, name = "『🔊』Canal próprio:", value = vipChannel.mention, inline = False)
            print(self.config)
            await interaction.message.edit(embeds = [self.embed], view = setVipForm5(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

class setVipModal6(discord.ui.Modal, title = "Adicionar amigo:"):
    def __init__(self, bot, embed, config, user):
        super().__init__(timeout = None)
        self.bot = bot
        self.embed = embed
        self.config = config
        self.user = user

        self.add_item(discord.ui.TextInput(
            label = f"ID do amigo:",
            style = discord.TextStyle.short,
            min_length = 1,
            required = True,
            )
        )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            friendId = self.children[0].value
            user = discord.utils.get(self.bot.get_guild(interaction.guild.id).members, id = int(friendId))
            print(user)
            if self.config["role"] != "`Não informado`":
                vipExclusiveRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(self.config["role"]))
                await user.add_roles(vipExclusiveRole)
            if self.config["channel"] != "`Não informado`":
                vipChannel = discord.utils.get(self.bot.get_guild(interaction.guild.id).channels, id = int(self.config["channel"]))
                serverOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                userOverwrites = interaction.channel.overwrites_for(interaction.guild.default_role)
                serverOverwrites.view_channel, serverOverwrites.send_messages, serverOverwrites.speak, serverOverwrites.connect = True, False, False, False
                userOverwrites.view_channel, userOverwrites.send_messages, userOverwrites.speak, userOverwrites.connect = True, True, True, True
                await vipChannel.set_permissions(interaction.guild.default_role, overwrite = serverOverwrites)
                await vipChannel.set_permissions(user, overwrite = userOverwrites)
            f = []
            self.config["friends"].append(f"{user.id}")
            for friend in self.config["friends"]:
                user = await self.bot.fetch_user(int(friend))
                f.append(f"{user.mention} `({user.id})`")
            await interaction.response.send_message(content = f"『👤』Novo amigo: {user.mention}\n『👥』Total de amigos: " + '\n'.join(f), ephemeral = True)
            self.embed.set_field_at(index = 5, name = "『👥』Amigos:", value = '\n'.join(f), inline = False)
            print(self.config)
            await interaction.message.edit(embeds = [self.embed], view = setVipForm6(self.bot, self.embed, self.config, self.user))
        except Exception as e:
            print(e)

bot.ses = aiohttp.ClientSession()
class cog_setVip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "setvip", aliases = ["addvip", "vipset", "vipadd"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def setvip(self, ctx, user: discord.User = None, vipRole: discord.Role = None):
        try:
            dbname = getDatabase()
            collectionName = dbname["vip"]
            vip = {
                "user": "`Não informado`",
                "vip": "`Não informado`",
                "endsAt": "`Não informado`",
                "role": "`Não informado`",
                "channel": "`Não informado`",
                "friends": []
            }
            setVipEmbed = discord.Embed(
                color = discord.Color.from_rgb(200, 20, 255)
            )
            setVipEmbed.set_author(name = f"『💎』Configurar VIP:", icon_url = self.bot.user.display_avatar.url)
            setVipEmbed.add_field(name = f"『👤』Usuário:", value = vip["user"], inline = False)
            setVipEmbed.add_field(name = f"『💎』VIP selecionado:", value = vip["vip"], inline = False)
            setVipEmbed.add_field(name = f"『⏰』Duração:", value = vip["endsAt"], inline = False)
            setVipEmbed.add_field(name = f"『💼』Cargo próprio:", value = vip["role"], inline = False)
            setVipEmbed.add_field(name = f"『🔊』Canal próprio:", value = vip["channel"], inline = False)
            setVipEmbed.add_field(name = f"『👥』Amigos:", value = "`Não informado`", inline = False)
            setVipEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
            if vipRole != None:
                index = vipRoles.index(vipRole.id)
                vip["vip"] = index
                print(vipRole.id, index)
                setVipEmbed.set_field_at(index = 1, name = f"『{vipEmojis[index]}』VIP selecionado:", value = f"`{vipNames[index]}`", inline = False)
            if user != None:
                vipCheck = collectionName.find_one({"User": user.id})
                print(vipCheck)
                if vipCheck != None:
                    noVip = discord.Embed(
                        title = f"VIP já registrado!",
                        description = f"『❌』Este usuário já possui um plano VIP ativo!",
                        color = 0xFF0000
                    )
                    noVip.set_thumbnail(url = link["error"])
                    noVip.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
                    await ctx.reply(embed = noVip)
                    return
                vip["user"] = user.id
                setVipEmbed.set_field_at(index = 0, name = f"『👤』Usuário:", value = f"{user.mention} `({user.id})`", inline = False)
            print(vip)
            await ctx.reply(embed = setVipEmbed, view = setVipForm1(self.bot, setVipEmbed, vip, ctx.author))
            return
        except Exception as e:
            print(e)
    
    @setvip.error
    async def setvip_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            print("a!setvip sem permissão")
            #await ctx.reply("❤")
            return
async def setup(bot):
    print(f"{prefix}setvip")
    await bot.add_cog(cog_setVip(bot))