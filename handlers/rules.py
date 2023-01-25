import discord
import json

class rulesClass(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    @discord.ui.button(label = f"Leves", style = discord.ButtonStyle.blurple, emoji = "🟢")
    async def ruleGreenInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        rulesListed = []
        for i in range(1, 5):
            rulesListed.append(f"{self.json[f'rule{i}']['ruleTitle']}\n{self.json[f'rule{i}']['ruleDesc']}")
        rulesEmbed = discord.Embed(
            title = f"꧁🟢 Infrações leves 🟢꧂",
            description = f"\n\n".join(rulesListed),
            color = discord.Color.from_rgb(20, 220, 20)
        )
        rulesEmbed.set_footer(text = "Infrações leves")
        await interaction.response.send_message(embed = rulesEmbed, ephemeral = True)
        alertChannel = self.bot.get_channel(self.json["rulesAlert"])
        await alertChannel.send(f"『🟢』{interaction.user.mention} `({interaction.user.id})` abriu as infrações leves!")

    @discord.ui.button(label = f"Médias", style = discord.ButtonStyle.blurple, emoji = "🟡")
    async def ruleYellowInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        rulesListed = []
        for i in range(5, 11):
            rulesListed.append(f"{self.json[f'rule{i}']['ruleTitle']}\n{self.json[f'rule{i}']['ruleDesc']}")
        rulesEmbed = discord.Embed(
            title = f"꧁🟡 Infrações médias 🟡꧂",
            description = f"\n\n".join(rulesListed),
            color = discord.Color.from_rgb(245, 220, 20)
        )
        rulesEmbed.set_footer(text = "Infrações médias")
        await interaction.response.send_message(embed = rulesEmbed, ephemeral = True)
        alertChannel = self.bot.get_channel(self.json["rulesAlert"])
        await alertChannel.send(f"『🟡』{interaction.user.mention} `({interaction.user.id})` abriu as infrações médias!")

    @discord.ui.button(label = f"Graves", style = discord.ButtonStyle.blurple, emoji = "🔴")
    async def ruleRedInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        rulesListed = []
        for i in range(11, 18):
            rulesListed.append(f"{self.json[f'rule{i}']['ruleTitle']}\n{self.json[f'rule{i}']['ruleDesc']}")
        rulesEmbed = discord.Embed(
            title = f"꧁🔴 Infrações graves 🔴꧂",
            description = f"\n\n".join(rulesListed),
            color = discord.Color.from_rgb(220, 20, 20)
        )
        rulesEmbed.set_footer(text = "Infrações graves")
        await interaction.response.send_message(embed = rulesEmbed, ephemeral = True)
        alertChannel = self.bot.get_channel(self.json["rulesAlert"])
        await alertChannel.send(f"『🔴』{interaction.user.mention} `({interaction.user.id})` abriu as infrações graves!")

    @discord.ui.button(label = f"Extremas", style = discord.ButtonStyle.blurple, emoji = "⚫")
    async def ruleGrayInteraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        rulesListed = []
        for i in range(18, 28):
            rulesListed.append(f"{self.json[f'rule{i}']['ruleTitle']}\n{self.json[f'rule{i}']['ruleDesc']}")
        rulesEmbed = discord.Embed(
            title = f"꧁⚫ Infrações extremas ⚫꧂",
            description = f"\n\n".join(rulesListed),
            color = discord.Color.from_rgb(20, 20, 20)
        )
        rulesEmbed.set_footer(text = "Infrações extremas")
        await interaction.response.send_message(embed = rulesEmbed, ephemeral = True)
        alertChannel = self.bot.get_channel(self.json["rulesAlert"])
        await alertChannel.send(f"『⚫』{interaction.user.mention} `({interaction.user.id})` abriu as infrações extremas!")

async def getRuleRow(bot):
    try:
        c = open("../jsons/rules.json", encoding = "utf8")
        rulesJson = json.load(c)
        channel = bot.get_channel(rulesJson["rulesChannel"])
        ruleMsg = await channel.fetch_message(rulesJson["rulesMessage"])
        await ruleMsg.edit(view = rulesClass(bot = bot, json = rulesJson))
    except Exception as e:
        print(e)