import discord
import json
import random
from mongoconnection.star import *

class shopColorGrayRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"shop-color_{random.randint(0, 10000)}", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Branco",
            description = "20 estrelas verdes",
            emoji = "🤍",
            value = 800824734526079026
        ),
        discord.SelectOption(
            label = "Cinza Claro",
            description = "20 estrelas verdes",
            emoji = "⚪",
            value = 800825064697626624
        ),
        discord.SelectOption(
            label = "Cinza Prata",
            description = "20 estrelas verdes",
            emoji = "⬜",
            value = 1065310669592866836
        ),
        discord.SelectOption(
            label = "Cinza Escuro",
            description = "20 estrelas verdes",
            emoji = "🖤",
            value = 800825175938433036
        ),
        discord.SelectOption(
            label = "Cinza Chumbo",
            description = "20 estrelas verdes",
            emoji = "⚫",
            value = 1065310983079350332
        ),
        discord.SelectOption(
            label = "Preto",
            description = "20 estrelas verdes",
            emoji = "⬛",
            value = 800825219651862548
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
                    title = f"꧁🎨 Cores Neutras 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(20, 255, 20)
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
                if userStars['stars']['3'] >= price:
                    colorsBuyEmbed = discord.Embed(title = f"꧁🎨 Cores Neutras 🎨꧂", description = f"Você tem certeza de que deseja comprar esta cor: {colorRole.mention}?", color = discord.Color.from_rgb(20, 255, 20))
                    colorsBuyEmbed.add_field(name = f"Preço:", value = f"{price} {link['stars']['emjs']['3']}", inline = True)
                    colorsBuyEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['3']} {link['stars']['emjs']['3']}", inline = True)
                    colorsBuyEmbed.add_field(name = "『🔷』VIP:", value = f"Os VIP's Safira podem obter esta cor gratuitamente! Confira mais detalhes sobre os vips em <#1047316824976523354> e abra um ticket!", inline = False)
                    await interaction.response.send_message(embed = colorsBuyEmbed, ephemeral = True, view = shopColorConfirmRow(self.bot, self.json, colorRole, price))
                    await alertChannel.send(f"『{link['stars']['emjs']['3']}』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
                else:
                    colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Neutras 🎨꧂", description = f"Você precisa ter **{price}** estrelas verdes para comprar esta cor!", color = discord.Color.from_rgb(20, 255, 20))
                    colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['3']} {link['stars']['emjs']['3']}", inline = True)
                    colorsEmbed.add_field(name = f"Dica:", value = f"Não sabe como ganhar estrelas? Confira o nosso canal de <#1071285010574868501> para saber como obtê-las ;)", inline = False)
                    await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                    await alertChannel.send(f"『{link['stars']['emjs']['3']}』{interaction.user.mention} `({interaction.user.id})` tentou comprar a cor {colorRole}, mas não tinha estrelas verdes suficientes!")
            return
        except Exception as e:
            print(e)

class shopColorConfirmRow(discord.ui.View):
    def __init__(self, bot, json, role, price):
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
            userStars = removeStars(interaction.user.id, 3, self.price)
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Neutras 🎨꧂", description = f"Você comprou a cor {self.role.mention}!", color = discord.Color.from_rgb(20, 255, 20))
            colorsEmbed.add_field(name = f"Suas estrelas:", value = f"{userStars['stars']['3']} {link['stars']['emjs']['3']}", inline = True)
            await interaction.user.add_roles(self.role)
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
            await alertChannel.send(f"『🛒』{interaction.user.mention} `({interaction.user.id})` comprou a cor {self.role}!")
        except Exception as e:
            print(e)

    @discord.ui.button(label = f"Não", style = discord.ButtonStyle.red, emoji = "❌")
    async def shopColorCancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            colorsEmbed = discord.Embed(title = f"꧁🎨 Cores Neutras 🎨꧂", description = f"Compra cancelada!", color = discord.Color.from_rgb(20, 255, 20))
            await interaction.response.edit_message(embed = colorsEmbed, view = None)
        except Exception as e:
            print(e)

async def getShopColorGray(bot):
    try:
        c = open("../jsons/shop.json", encoding = "utf8")
        shopJson = json.load(c)
        channel = bot.get_channel(shopJson["colorShopChannelId"])
        shopMsg = await channel.fetch_message(shopJson["colorShopGrayMessageId"])
        shopEmbed = discord.Embed(
            title = f"꧁🎨 Cores Neutras 🎨꧂",
            description = f"『🤍』<@&800824734526079026>\n『⚪』<@&800825064697626624>\n『⬜』<@&1065310669592866836>\n『🖤』<@&800825175938433036>\n『⚫』<@&1065310983079350332>\n『⬛』<@&800825219651862548>",
            color = discord.Color.from_rgb(20, 255, 20)
        )
        shopEmbed.set_image(url = "https://i.imgur.com/N7ziAww.png")
        shopEmbed.set_footer(text = "Grátis para VIP'S Safira 🔷!", icon_url = bot.user.display_avatar.url)
        await shopMsg.edit(embed = shopEmbed, view = shopColorGrayRow(bot = bot, json = shopJson))
    except Exception as e:
        print(e)