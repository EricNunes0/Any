import discord
import json

class colorsClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__()
        self.bot = bot
        self.json = json
    
    @discord.ui.select(custom_id = f"colors_menu", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Vermelho Escuro",
            emoji = "🟥",
            value = 800819136493649920
        ),
        discord.SelectOption(
            label = "Laranja Escuro",
            emoji = "🟧",
            value = 800820080866361344
        ),
        discord.SelectOption(
            label = "Amarelo Escuro",
            emoji = "🟨",
            value = 800820635395162143
        ),
        discord.SelectOption(
            label = "Verde Escuro",
            emoji = "🟩",
            value = 800816522561585213
        ),
        discord.SelectOption(
            label = "Azul Escuro",
            emoji = "🟦",
            value = 800816798748246076
        ),
        discord.SelectOption(
            label = "Roxo Escuro",
            emoji = "🟪",
            value = 800823824106782735
        ),
        discord.SelectOption(
            label = "Rosa Escuro",
            emoji = "💝",
            value = 800823008876036126
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
                    title = f"꧁🎨 Cores Escuras 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores escuras", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Escuras 🎨꧂",
                    description = f"Você escolheu a cor {colorRole.mention}!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores escuras", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(colorRole)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
            return
        except Exception as e:
            print(e)

async def getDarkColorsRow(bot):
    try:
        c = open("../jsons/colors.json", encoding = "utf8")
        colorsJson = json.load(c)
        channel = bot.get_channel(colorsJson["darkChannel"])
        colorsMsg = await channel.fetch_message(colorsJson["darkMessage"])
        colorsEmbed = discord.Embed(
            title = f"꧁🎨 Cores Escuras 🎨꧂",
            description = f"『🟥』<@&800819136493649920>\n『🟧』<@&800820080866361344>\n『🟨』<@&800820635395162143>\n『🟩』<@&800816522561585213>\n『🟦』<@&800816798748246076>\n『🟪』<@&800823824106782735>\n『💝』<@&800823008876036126>",
            color = discord.Color.from_rgb(220, 220, 20)
        )
        colorsEmbed.set_image(url = "https://i.imgur.com/WzWNGJo.png")
        colorsEmbed.set_footer(text = "Escolha 1 cor no menu abaixo", icon_url = bot.user.display_avatar.url)
        await colorsMsg.edit(content = "", embed = colorsEmbed, view = colorsClass(bot = bot, json = colorsJson))
    except Exception as e:
        print(e)