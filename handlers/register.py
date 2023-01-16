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
            emoji = "🔴"
        ),
        discord.SelectOption(
            label = "Laranja",
            emoji = "🟠"
        ),
        discord.SelectOption(
            label = "Amarelo",
            emoji = "🟡"
        ),
        discord.SelectOption(
            label = "Verde",
            emoji = "🟢"
        ),
        discord.SelectOption(
            label = "Azul",
            emoji = "🔵"
        ),
        discord.SelectOption(
            label = "Roxo",
            emoji = "🟣"
        ),
        discord.SelectOption(
            label = "Branco",
            emoji = "⚪"
        )
    ])
    async def registerInteraction(self, interaction: discord.Interaction, select):
        registerEmbed = discord.Embed(
            title = f"꧁🎨 Cores 🎨꧂",
            description = f"Você escolheu a cor `{select.values[0]}`!",
            color = discord.Color.from_rgb(220, 220, 20)
        )
        registerEmbed.set_footer(text = "Cores coloridas")
        await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
        alertChannel = self.bot.get_channel(self.json["registerAlert"])
        await alertChannel.send(f"『🎨』{interaction.user.mention} `({interaction.user.id})` escolheu a cor {select.values[0]}!")

async def getRegisterRow(bot):
    try:
        c = open("../jsons/register.json", encoding = "utf8")
        registerJson = json.load(c)
        channel = bot.get_channel(registerJson["registerChannel"])
        registerMsg = await channel.fetch_message(registerJson["registerMessage"])
        await registerMsg.edit(view = registerClass(bot = bot, json = registerJson))
    except Exception as e:
        print(e)