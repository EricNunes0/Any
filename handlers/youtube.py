import discord
import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate

global redIcon, yellowIcon, greenIcon, blueIcon
redIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001093507219466/20231028_223658.gif?ex=65502cc9&is=653db7c9&hm=4030901c3061c05e21f553ec858d4545731677bb242988bacd57a91950df0876&"
yellowIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001094174117908/20231028_223852.gif?ex=65502cc9&is=653db7c9&hm=2b3202f6a4657ccadc8f362863dd44b83420235128ecd1d6ede99b7ee3a3fe90&"
greenIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001094857793566/20231028_223730.gif?ex=65502cc9&is=653db7c9&hm=05735f55467cb9e1af26e424872cd40e714270d3eed246a6381cfad35937d8f5&"
blueIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001095361101916/20231028_223759.gif?ex=65502cc9&is=653db7c9&hm=270ab38ab1a371f829b57af064f5386043bce145c25ae8d4a0f37010cabde9ae&"

class sendLocation(discord.ui.View):
    def __init__(self, bot, message, embed):
        super().__init__(timeout = None)
        self.bot = bot
        self.message = message
        self.embed = embed
    
    @discord.ui.button(label = f"Servidor", style = discord.ButtonStyle.blurple, emoji = "🌃", disabled = False)
    async def serverSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            print("🌃 Servidor selecionado!")
            self.embed.set_author(name = "『▶』Youtube Download:", icon_url = yellowIcon)
            self.embed.title = "Processando vídeo..."
            self.embed.color = discord.Color.from_rgb(255, 255, 0)
            await interaction.message.edit(embed=self.embed, view=None)

            link = self.message.content
            try:
                youtubeQuery = YouTube(link)
            except VideoPrivate:
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo está privado"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await interaction.message.edit(embed = self.embed)
                return
            except VideoUnavailable:
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo está indisponível"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await interaction.message.edit(embed = self.embed)
                return
            youtubeObject = youtubeQuery.streams.get_highest_resolution()
            videoName = "resultado.mp4"
            dirPath = str(os.getcwd()) + f"/videos"
            filePath = dirPath + f"/{videoName}"
            try:
                yt = youtubeObject.download(filename = videoName, output_path=dirPath)
            except Exception as e:
                print(e)
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Não foi possível baixar o vídeo"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await self.message.channel.send(embed = self.embed)
                return
            ageRestriction = "Não"
            if youtubeQuery.age_restricted:
                ageRestriction = "Sim"
            self.embed.title = youtubeQuery.title
            self.embed.set_thumbnail(url = youtubeQuery.thumbnail_url)
            self.embed.add_field(name = "『©』Autor:", value = f"[{youtubeQuery.author}]({youtubeQuery.channel_url})")
            self.embed.add_field(name = "『⏫』Data de publicação:", value = f"`{youtubeQuery.publish_date}`")
            self.embed.add_field(name = "『👁』Visualizações:", value = f"`{youtubeQuery.views}`")
            self.embed.add_field(name = "『🔞』Restrição de idade:", value = f"`{ageRestriction}`")
            await interaction.message.edit(embed = self.embed)
            try:
                await self.message.channel.send(content = self.message.author.mention, file = discord.File(filePath))
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = greenIcon)
                self.embed.color = discord.Color.from_rgb(0, 255, 0)
            except Exception as e:
                print("❌", e)
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo é muito grande"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
            await interaction.message.edit(embed = self.embed)
            if os.path.exists(f"videos/{videoName}"):
                os.remove(f"videos/{videoName}")
            return
    
    @discord.ui.button(label = f"DM", style = discord.ButtonStyle.blurple, emoji = "👤", disabled = False)
    async def dmSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            print("👤 DM selecionada!")
            self.embed.set_author(name = "『▶』Youtube Download:", icon_url = yellowIcon)
            self.embed.title = "Processando vídeo..."
            self.embed.color = discord.Color.from_rgb(255, 255, 0)
            await interaction.message.edit(embed=self.embed, view=None)
            link = self.message.content
            try:
                youtubeQuery = YouTube(link)
            except VideoPrivate:
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo está privado"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await interaction.message.edit(embed = self.embed)
                return
            except VideoUnavailable:
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo está indisponível"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await interaction.message.edit(embed = self.embed)
                return
            youtubeObject = youtubeQuery.streams.get_highest_resolution()
            videoName = "resultado.mp4"
            dirPath = str(os.getcwd()) + f"/videos"
            filePath = dirPath + f"/{videoName}"
            try:
                yt = youtubeObject.download(filename = videoName, output_path=dirPath)
            except Exception as e:
                print(e)
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Não foi possível baixar o vídeo"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
                await self.message.channel.send(embed = self.embed)
                return
            ageRestriction = "Não"
            if youtubeQuery.age_restricted:
                ageRestriction = "Sim"
            self.embed.title = youtubeQuery.title
            self.embed.color = discord.Color.from_rgb(0, 255, 0)
            self.embed.set_thumbnail(url = youtubeQuery.thumbnail_url)
            self.embed.add_field(name = "『©』Autor:", value = f"[{youtubeQuery.author}]({youtubeQuery.channel_url})")
            self.embed.add_field(name = "『⏫』Data de publicação:", value = f"`{youtubeQuery.publish_date}`")
            self.embed.add_field(name = "『👁』Visualizações:", value = f"`{youtubeQuery.views}`")
            self.embed.add_field(name = "『🔞』Restrição de idade:", value = f"`{ageRestriction}`")
            self.embed.set_image(url = f"attachment://videos/{videoName}")
            self.embed.set_footer(text = f"Enviado para {self.message.author.name} ⏫", icon_url = self.message.author.display_avatar.url)
            await interaction.message.edit(embed = self.embed)
            try:
                await interaction.user.send(file = discord.File(filePath))
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = greenIcon)
                self.embed.color = discord.Color.from_rgb(0, 255, 0)
            except Exception as e:
                print("❌", e)
                self.embed.set_author(name = "『▶』Youtube Download:", icon_url = redIcon)
                self.embed.title = "Este vídeo é muito grande"
                self.embed.color = discord.Color.from_rgb(255, 0, 0)
            await interaction.message.edit(embed = self.embed)
            if os.path.exists(f"videos/{videoName}"):
                os.remove(f"videos/{videoName}")
            return
    
    @discord.ui.button(label = f"Cancelar", style = discord.ButtonStyle.red, emoji = "❌", disabled = False)
    async def cancelSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.message.delete()


async def youtube(bot, message):
    if message.author.bot == True:
        return
    if not str(message.content).startswith("https://"):
        await message.delete()
        return
    print(message.content)
    ytEmbed = discord.Embed(
        title = "Por onde deseja receber o vídeo?",
        color = discord.Color.from_rgb(50, 100, 255)
    )
    ytEmbed.set_author(name = "『▶』Youtube Download:", icon_url = blueIcon)
    ytEmbed.add_field(name = "『🔗』URL:", value = f"{message.content}", inline = False)
    ytEmbed.set_footer(text = f"Pedido por {message.author.name}", icon_url = message.author.display_avatar.url)
    await message.delete()
    await message.channel.send(content = f"{message.author.mention}", embed = ytEmbed, view = sendLocation(bot=bot, message=message, embed=ytEmbed))