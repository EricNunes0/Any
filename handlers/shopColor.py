import discord
import json
import random
from mongoconnection.star import *

class shopColorRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"shop-color_{random.randint(0, 10000)}", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Vermelho",
            description = "10 estrelas vermelhas",
            emoji = "🔴",
            value = 800815629309181953
        ),
        discord.SelectOption(
            label = "Laranja",
            description = "10 estrelas vermelhas",
            emoji = "🟠",
            value = 800815989750628412
        ),
        discord.SelectOption(
            label = "Amarelo",
            description = "10 estrelas vermelhas",
            emoji = "🟡",
            value = 800816207422291988
        ),
        discord.SelectOption(
            label = "Verde",
            description = "10 estrelas vermelhas",
            emoji = "🟢",
            value = 800816348333867008
        ),
        discord.SelectOption(
            label = "Azul",
            description = "10 estrelas vermelhas",
            emoji = "🔵",
            value = 800822581648818177
        ),
        discord.SelectOption(
            label = "Roxo",
            description = "10 estrelas vermelhas",
            emoji = "🟣",
            value = 800816957891805214
        ),
        discord.SelectOption(
            label = "Rosa",
            description = "10 estrelas vermelhas",
            emoji = "💟",
            value = 800817073299259463
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
            if int(value) == 0:            
                rolesIds = []
                for role in interaction.user.roles:
                    rolesIds.append(int(role.id))
                for color in self.json["colorAvailableIds"]:
                    if int(color) in rolesIds:
                        removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                        await interaction.user.remove_roles(removeColorRole)
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Básicas 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(255, 20, 20)
                )
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                userStars = getStar(interaction.user.id)
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                price = 10
                if userStars['stars']['0'] >= price: # 10 estrelas vermelhas
                    colorsBuyEmbed = discord.Embed(title = f"꧁🎨 Cores Básicas 🎨꧂", description = f"Você tem certeza de que deseja comprar esta cor: {colorRole.mention}?", color = discord.Color.from_rgb(255, 20, 20))
                    colorsBuyEmbed.add_field(name = f"Preço:", value = f"{price} {link['stars']['emjs']['0']}", inline = True)
                    colorsBuyEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['0']} {link['stars']['emjs']['0']}", inline = True)
                    await interaction.response.send_message(embed = colorsBuyEmbed, ephemeral = True, view = shopColorConfirmRow(self.bot, self.json, colorRole))
                    await alertChannel.send(f"『{link['stars']['emjs']['0']}』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
                else:
                    colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Básicas 🎨꧂", description = f"Você precisa ter **10** estrelas vermelhas para comprar esta cor!", color = discord.Color.from_rgb(255, 20, 20))
                    colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['0']} {link['stars']['emjs']['0']}", inline = True)
                    colorsEmbed.add_field(name = f"Dica:", value = f"Não sabe como ganhar estrelas? Confira o nosso canal de <#1071285010574868501> para saber como obtê-las ;)", inline = False)
                    await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                    await alertChannel.send(f"『{link['stars']['emjs']['0']}』{interaction.user.mention} `({interaction.user.id})` tentou comprar a cor {colorRole}, mas não tinha estrelas vermelhas!")
            return
        except Exception as e:
            print(e)

class shopColorConfirmRow(discord.ui.View):
    def __init__(self, bot, json, role):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
        self.role = role
    
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
            userStars = removeStars(interaction.user.id, 0, 10)
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Básicas 🎨꧂", description = f"Você comprou a cor {self.role.mention}!", color = discord.Color.from_rgb(255, 20, 20))
            colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['0']} {link['stars']['emjs']['0']}", inline = True)
            await interaction.user.add_roles(self.role)
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
            await alertChannel.send(f"『🛒』{interaction.user.mention} `({interaction.user.id})` comprou a cor {self.role}!")
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def staffFormA3Answer2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Básicas 🎨꧂", description = f"Compra cancelada!", color = discord.Color.from_rgb(255, 20, 20))
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
        except Exception as e:
            print(e)

async def getShopColor(bot):
    try:
        c = open("../jsons/shop.json", encoding = "utf8")
        shopJson = json.load(c)
        channel = bot.get_channel(shopJson["colorShopChannelId"])
        shopMsg = await channel.fetch_message(shopJson["colorShopMessageId"])
        shopEmbed = discord.Embed(
            title = f"꧁🎨 Cores Básicas 🎨꧂",
            description = f"『🔴』<@&800815629309181953>\n『🟠』<@&800815989750628412>\n『🟡』<@&800816207422291988>\n『🟢』<@&800816348333867008>\n『🔵』<@&800822581648818177>\n『🟣』<@&800816957891805214>\n『💟』<@&800817073299259463>",
            color = discord.Color.from_rgb(255, 20, 20)
        )
        shopEmbed.set_image(url = "https://i.imgur.com/2SoLIDk.png")
        shopEmbed.set_footer(text = "Escolha a sua cor no menu abaixo:", icon_url = bot.user.display_avatar.url)
        await shopMsg.edit(embed = shopEmbed, view = shopColorRow(bot = bot, json = shopJson))
    except Exception as e:
        print(e)