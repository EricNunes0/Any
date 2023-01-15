import discord
import json



rulesEmbed = discord.Embed(title = f"",
    description = f"**▸ 「R.1」Drops:**\n> 『💬』Todos que vencerem os drops, precisarão obrigatoriamente pagar uma taxa de 90% para o Eric.\n> 『⛔』**Punição:** Banimento imediato!",
    color = 0x202020
)

class rulesClass(discord.ui.View):
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    @discord.ui.button(label = f"Regras", style = discord.ButtonStyle.blurple, emoji = "📃")
    async def ruleInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed = rulesEmbed, ephemeral = True)

async def getRuleRow(bot):
    try:
        c = open("../jsons/rules.json")
        rulesJson = json.load(c)
        print(rulesJson)
        channel = bot.get_channel(rulesJson["rulesChannel"])
        print(channel)
        ruleMsg = await channel.fetch_message(rulesJson["rulesMessage"])
        print(ruleMsg)
        await ruleMsg.edit(view = rulesClass("Não quebre as regras!"))
    except Exception as e:
        print(e)