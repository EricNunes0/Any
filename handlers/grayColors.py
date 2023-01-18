import discord
import json

class colorsClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__()
        self.bot = bot
        self.json = json
    
    @discord.ui.select(custom_id = f"colors_menu", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Branco",
            emoji = "🤍",
            value = 800824734526079026
        ),
        discord.SelectOption(
            label = "Cinza Claro",
            emoji = "⚪",
            value = 800825064697626624
        ),
        discord.SelectOption(
            label = "Cinza Prata",
            emoji = "⬜",
            value = 1065310669592866836
        ),
        discord.SelectOption(
            label = "Cinza Escuro",
            emoji = "🖤",
            value = 800825175938433036
        ),
        discord.SelectOption(
            label = "Cinza Chumbo",
            emoji = "⚫",
            value = 1065310983079350332
        ),
        discord.SelectOption(
            label = "Preto",
            emoji = "⬛",
            value = 800825219651862548
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
                    title = f"꧁🎨 Cores Neutras 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores neutras", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Neutras 🎨꧂",
                    description = f"Você escolheu a cor {colorRole.mention}!",
                    color = discord.Color.from_rgb(220, 220, 20)
                )
                colorsEmbed.set_footer(text = "Cores neutras", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(colorRole)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
            return
        except Exception as e:
            print(e)

async def getGrayColorsRow(bot):
    try:
        c = open("../jsons/colors.json", encoding = "utf8")
        colorsJson = json.load(c)
        channel = bot.get_channel(colorsJson["grayChannel"])
        colorsMsg = await channel.fetch_message(colorsJson["grayMessage"])
        colorsEmbed = discord.Embed(
            title = f"꧁🎨 Cores Neutras 🎨꧂",
            description = f"『🤍』<@&800824734526079026>\n『⚪』<@&800825064697626624>\n『⬜』<@&1065310669592866836>\n『🖤』<@&800825175938433036>\n『⚫』<@&1065310983079350332>\n『⬛』<@&800825219651862548>",
            color = discord.Color.from_rgb(220, 220, 20)
        )
        colorsEmbed.set_image(url = "https://i.imgur.com/N7ziAww.png")
        colorsEmbed.set_footer(text = "Escolha 1 cor no menu abaixo", icon_url = bot.user.display_avatar.url)
        await colorsMsg.edit(content = "", embed = colorsEmbed, view = colorsClass(bot = bot, json = colorsJson))
    except Exception as e:
        print(e)