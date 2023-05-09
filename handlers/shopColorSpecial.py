import discord
import json
import random
from mongoconnection.star import *

class shopColorSpecialRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"shop-color_{random.randint(0, 10000)}", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Escarlate",
            description = "20 estrelas azuis",
            emoji = "🔺",
            value = 1065397010624155738
        ),
        discord.SelectOption(
            label = "Solar",
            description = "20 estrelas azuis",
            emoji = "☀",
            value = 1065397238911741972
        ),
        discord.SelectOption(
            label = "Limão",
            description = "20 estrelas azuis",
            emoji = "🍋",
            value = 1065397426552307812
        ),
        discord.SelectOption(
            label = "Aquamarine",
            description = "20 estrelas azuis",
            emoji = "🌊",
            value = 1065397559264288819
        ),
        discord.SelectOption(
            label = "Ciano",
            description = "20 estrelas azuis",
            emoji = "🔹",
            value = 1065397795500081264
        ),
        discord.SelectOption(
            label = "Azul Marinho",
            description = "20 estrelas azuis",
            emoji = "🔷",
            value = 1065629506188083200
        ),
        discord.SelectOption(
            label = "Carmesim",
            description = "20 estrelas azuis",
            emoji = "🌺",
            value = 1065397983849496716
        ),
        discord.SelectOption(
            label = "Vinho",
            description = "20 estrelas azuis",
            emoji = "🍷",
            value = 1065398133632274563
        ),
        discord.SelectOption(
            label = "Castanho",
            description = "20 estrelas azuis",
            emoji = "🤎",
            value = 1065398310963261500
        ),
        discord.SelectOption(
            label = "Remover cor",
            emoji = "❌",
            value = 0
        )
    ])
    async def shopColorInt(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            alertChannel = self.bot.get_channel(self.json["colorShopAlertChannelId"])
            l = open("../link.json")
            link = json.load(l)
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            if int(value) == 0:
                for color in self.json["colorAvailableIds"]:
                    if int(color) in rolesIds:
                        removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                        await interaction.user.remove_roles(removeColorRole)
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Especiais 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(20, 120, 255)
                )
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                userStars = getStar(interaction.user.id)
                if 1047268807812595802 in rolesIds or 739210760567390250 in rolesIds:
                    price = 0
                else:
                    price = 20
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                if userStars['stars']['4'] >= price: # 20 estrelas azuis
                    colorsBuyEmbed = discord.Embed(title = f"꧁🎨 Cores Especiais 🎨꧂", description = f"Você tem certeza de que deseja comprar esta cor: {colorRole.mention}?", color = discord.Color.from_rgb(20, 120, 255))
                    colorsBuyEmbed.add_field(name = f"Preço:", value = f"{price} {link['stars']['emjs']['4']}", inline = True)
                    colorsBuyEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['4']} {link['stars']['emjs']['4']}", inline = True)
                    colorsBuyEmbed.add_field(name = "『🔷』VIP:", value = f"Os VIP's Safira podem obter esta cor gratuitamente! Confira mais detalhes sobre os vips em <#1047316824976523354> e abra um ticket!", inline = False)
                    await interaction.response.send_message(embed = colorsBuyEmbed, ephemeral = True, view = shopColorConfirmRow(self.bot, self.json, colorRole, price))
                    await alertChannel.send(f"『{link['stars']['emjs']['4']}』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
                else:
                    colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Especiais 🎨꧂", description = f"Você precisa ter **{price}** estrelas azuis para comprar esta cor!", color = discord.Color.from_rgb(20, 120, 255))
                    colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['4']} {link['stars']['emjs']['4']}", inline = True)
                    colorsEmbed.add_field(name = f"Dica:", value = f"Não sabe como ganhar estrelas? Confira o nosso canal de <#1071285010574868501> para saber como obtê-las ;)", inline = False)
                    await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                    await alertChannel.send(f"『{link['stars']['emjs']['4']}』{interaction.user.mention} `({interaction.user.id})` tentou comprar a cor {colorRole}, mas não tinha estrelas azuis suficientes!")
            return
        except Exception as e:
            print(e)

class shopColorConfirmRow(discord.ui.View):
    def __init__(self, bot, json, role, price: int):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.role = role
        self.price = price
    
    @discord.ui.button(label = f"Sim", style = discord.ButtonStyle.green, emoji = "✅")
    async def shopColorConfirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            l = open("../link.json")
            link = json.load(l)
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for color in self.json["colorAvailableIds"]:
                if int(color) in rolesIds:
                    removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                    await interaction.user.remove_roles(removeColorRole)
            alertChannel = self.bot.get_channel(self.json["colorShopAlertChannelId"])
            userStars = removeStars(interaction.user.id, 4, self.price)
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Especiais 🎨꧂", description = f"Você comprou a cor {self.role.mention}!", color = discord.Color.from_rgb(20, 120, 255))
            colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['4']} {link['stars']['emjs']['4']}", inline = True)
            await interaction.user.add_roles(self.role)
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
            await alertChannel.send(f"『🛒』{interaction.user.mention} `({interaction.user.id})` comprou a cor {self.role}!")
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def shopColorCancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Especiais 🎨꧂", description = f"Compra cancelada!", color = discord.Color.from_rgb(20, 120, 255))
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
        except Exception as e:
            print(e)

async def getShopColorSpecial(bot):
    try:
        c = open("../jsons/shop.json", encoding = "utf8")
        shopJson = json.load(c)
        channel = bot.get_channel(shopJson["colorShopChannelId"])
        shopMsg = await channel.fetch_message(shopJson["colorShopSpecialMessageId"])
        shopEmbed = discord.Embed(
            title = f"꧁🎨 Cores Especiais 🎨꧂",
            description = f"『🔺️』<@&1065397010624155738>\n『☀️』<@&1065397238911741972>\n『🍋』<@&1065397426552307812>\n『🌊』<@&1065397559264288819>\n『🔹️』<@&1065397795500081264>\n『🔷』<@&1065629506188083200>\n『🌺』<@&1065397983849496716>\n『🍷』<@&1065398133632274563>\n『🤎』<@&1065398310963261500>",
            color = discord.Color.from_rgb(20, 120, 255)
        )
        shopEmbed.set_image(url = "https://i.imgur.com/oVd0DEa.png")
        shopEmbed.set_footer(text = "Grátis para VIP'S Safira 🔷!", icon_url = bot.user.display_avatar.url)
        await shopMsg.edit(embed = shopEmbed, view = shopColorSpecialRow(bot = bot, json = shopJson))
    except Exception as e:
        print(e)