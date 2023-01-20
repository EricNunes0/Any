import discord
import json

class colorsClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.select(custom_id = f"colors_menu", placeholder = f"Escolha uma cor:", options = [
        discord.SelectOption(
            label = "Escarlate",
            emoji = "🔺",
            value = 1065397010624155738
        ),
        discord.SelectOption(
            label = "Solar",
            emoji = "☀",
            value = 1065397238911741972
        ),
        discord.SelectOption(
            label = "Limão",
            emoji = "🍋",
            value = 1065397426552307812
        ),
        discord.SelectOption(
            label = "Aquamarine",
            emoji = "🌊",
            value = 1065397559264288819
        ),
        discord.SelectOption(
            label = "Ciano",
            emoji = "🔹",
            value = 1065397795500081264
        ),
        discord.SelectOption(
            label = "Azul Marinho",
            emoji = "🔷",
            value = 1065629506188083200
        ),
        discord.SelectOption(
            label = "Carmesim",
            emoji = "🌺",
            value = 1065397983849496716
        ),
        discord.SelectOption(
            label = "Vinho",
            emoji = "🍷",
            value = 1065398133632274563
        ),
        discord.SelectOption(
            label = "Castanho",
            emoji = "🤎",
            value = 1065398310963261500
        ),
        discord.SelectOption(
            label = "Marrom",
            emoji = "🟤",
            value = 800824526384398356
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
            if not 1047268807812595802 in rolesIds:
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Especiais 🎨꧂",
                    color = discord.Color.from_rgb(220, 20, 20)
                )
                colorsEmbed.add_field(name = "『❌』Erro:", value = f"{interaction.user.mention}, você precisa ter o VIP <@&1047268807812595802> para usar estas cores!", inline = False)
                colorsEmbed.add_field(name = "『🔷』Comprar VIP:", value = f"Para comprar o VIP, veja mais detalhes do plano em <#1047316824976523354> e abra um ticket!", inline = False)
                colorsEmbed.set_footer(text = "Cores especiais", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                return
            for color in self.json["roleColors"]:
                    if int(color) in rolesIds:
                        removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                        await interaction.user.remove_roles(removeColorRole)
            if int(value) == 0:
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Especiais 🎨꧂",
                    description = f"Você removeu todas as cores!",
                    color = discord.Color.from_rgb(60, 110, 240)
                )
                colorsEmbed.set_footer(text = "Cores especiais", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as cores!")
                return
            else:
                colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                colorsEmbed = discord.Embed(
                    title = f"꧁🎨 Cores Especiais 🎨꧂",
                    description = f"Você escolheu a cor {colorRole.mention}!",
                    color = discord.Color.from_rgb(60, 110, 240)
                )
                colorsEmbed.set_footer(text = "Cores especiais", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(colorRole)
                await interaction.response.send_message(embed = colorsEmbed, ephemeral = True)
                alertChannel = self.bot.get_channel(self.json["colorsAlert"])
                await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
            return
        except Exception as e:
            print(e)

async def getSpecialColorsRow(bot):
    try:
        c = open("../jsons/colors.json", encoding = "utf8")
        colorsJson = json.load(c)
        channel = bot.get_channel(colorsJson["specialChannel"])
        colorsMsg = await channel.fetch_message(colorsJson["specialMessage"])
        colorsEmbed = discord.Embed(
            title = f"꧁🎨 Cores Especiais 🎨꧂",
            description = f"『🔺️』<@&1065397010624155738>\n『☀️』<@&1065397238911741972>\n『🍋』<@&1065397426552307812>\n『🌊』<@&1065397559264288819>\n『🔹️』<@&1065397795500081264>\n『🔷』<@&1065629506188083200>\n『🌺』<@&1065397983849496716>\n『🍷』<@&1065398133632274563>\n『🤎』<@&1065398310963261500>\n『🟤』<@&800824526384398356>",
            color = discord.Color.from_rgb(60, 110, 240)
        )
        colorsEmbed.set_image(url = "https://i.imgur.com/oVd0DEa.png")
        colorsEmbed.set_footer(text = "Exclusivo para VIP'S Safira 🔷!", icon_url = bot.user.display_avatar.url)
        await colorsMsg.edit(content = "", embed = colorsEmbed, view = colorsClass(bot = bot, json = colorsJson))
    except Exception as e:
        print(e)