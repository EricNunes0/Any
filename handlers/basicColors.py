import discord
import json
import random

class colorsClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        print("getBasicColorsRow() disabled")

    @discord.ui.select(custom_id = f"colors_menu_{random.randint(0, 1000)}", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Vermelho",
            emoji = "🔴",
            value = 800815629309181953
        ),
        discord.SelectOption(
            label = "Laranja",
            emoji = "🟠",
            value = 800815989750628412
        ),
        discord.SelectOption(
            label = "Amarelo",
            emoji = "🟡",
            value = 800816207422291988
        ),
        discord.SelectOption(
            label = "Verde",
            emoji = "🟢",
            value = 800816348333867008
        ),
        discord.SelectOption(
            label = "Azul",
            emoji = "🔵",
            value = 800822581648818177
        ),
        discord.SelectOption(
            label = "Roxo",
            emoji = "🟣",
            value = 800816957891805214
        ),
        discord.SelectOption(
            label = "Rosa",
            emoji = "💟",
            value = 800817073299259463
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def colorsInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for color in self.json["roleColors"]:
                    if int(color) in rolesIds:
                        removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                        await interaction.user.remove_roles(removeColorRole)
            if int(value) == 0:
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Básicas 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores básicas", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Básicas 🎨꧂",
                    description = f"Você escolheu a cor {colorRole.mention}!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores básicas", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(colorRole)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
            return
        except Exception as e:
            print(e)

async def getBasicColorsRow(bot):
    try:
        c = open("../jsons/colors.json", encoding = "utf8")
        colorsJson = json.load(c)
        channel = bot.get_channel(colorsJson["colorsChannel"])
        colorsMsg = await channel.fetch_message(colorsJson["colorsMessage"])
        colorsEmbed = discord.Embed(
            title = f"꧁🎨 Cores Básicas 🎨꧂",
            description = f"『🔴』<@&800815629309181953>\n『🟠』<@&800815989750628412>\n『🟡』<@&800816207422291988>\n『🟢』<@&800816348333867008>\n『🔵』<@&800822581648818177>\n『🟣』<@&800816957891805214>\n『💟』<@&800817073299259463>",
            color = discord.Color.from_rgb(220, 220, 20)
        )
        colorsEmbed.set_image(url = "https://i.imgur.com/2SoLIDk.png")
        colorsEmbed.set_footer(text = "Escolha 1 cor no menu abaixo", icon_url = bot.user.display_avatar.url)
        await colorsMsg.edit(content = "", embed = colorsEmbed, view = colorsClass(bot = bot, json = colorsJson))
    except Exception as e:
        print(e)