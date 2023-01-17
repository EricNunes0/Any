import discord
import json

class registerClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__()
        self.bot = bot
        self.json = json
    
    @discord.ui.select(custom_id = f"register_menu", placeholder = f"Escolha apenas 1 cor", options = [
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
            label = "Branco",
            emoji = "⚪",
            value = 800824734526079026
        )
    ])
    async def registerInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            colorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
            registerEmbed = discord.Embed(
                title = f"꧁🎨 Cores 🎨꧂",
                description = f"Você escolheu a cor {colorRole.mention}!",
                color = discord.Color.from_rgb(220, 220, 20)
            )
            registerEmbed.set_footer(text = "Cores coloridas")
            await interaction.user.add_roles(colorRole)
            await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {colorRole}!")
            for color in self.json["roleColors"]:
                print(interaction.user.roles)
                if color in interaction.user.roles:
                    removeColorRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(color))
                    await interaction.user.remove_roles(removeColorRole)
            return
        except Exception as e:
            print(e)

async def getRegisterRow(bot):
    try:
        c = open("../jsons/register.json", encoding = "utf8")
        registerJson = json.load(c)
        channel = bot.get_channel(registerJson["registerChannel"])
        registerMsg = await channel.fetch_message(registerJson["registerMessage"])
        registerEmbed = discord.Embed(
            title = f"꧁🎨 Cores 🎨꧂",
            description = f"『🔴』<@&800815629309181953>\n『🟠』<@&800815989750628412>\n『🟡』<@&800816207422291988>\n『🟢』<@&800816348333867008>\n『🔵』<@&800822581648818177>\n『🟣』<@&800816957891805214>\n『⚪』<@&800824734526079026>",
            color = discord.Color.from_rgb(220, 220, 20)
        )
        await registerMsg.edit(content = "", embed = registerEmbed, view = registerClass(bot = bot, json = registerJson))
    except Exception as e:
        print(e)