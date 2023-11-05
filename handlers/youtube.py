import discord
import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate

global redIcon, yellowIcon, greenIcon, blueIcon
redIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001093507219466/20231028_223658.gif?ex=65502cc9&is=653db7c9&hm=4030901c3061c05e21f553ec858d4545731677bb242988bacd57a91950df0876&"
yellowIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001094174117908/20231028_223852.gif?ex=65502cc9&is=653db7c9&hm=2b3202f6a4657ccadc8f362863dd44b83420235128ecd1d6ede99b7ee3a3fe90&"
greenIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001094857793566/20231028_223730.gif?ex=65502cc9&is=653db7c9&hm=05735f55467cb9e1af26e424872cd40e714270d3eed246a6381cfad35937d8f5&"
blueIcon = "https://cdn.discordapp.com/attachments/1167884725382299718/1168001095361101916/20231028_223759.gif?ex=65502cc9&is=653db7c9&hm=270ab38ab1a371f829b57af064f5386043bce145c25ae8d4a0f37010cabde9ae&"

async def downloadVideo(bot, message, embed, interaction, format: str, submit: str):
    embed.set_author(name = "『▶』Youtube Downloader:", icon_url = yellowIcon)
    embed.title = "Processando vídeo..."
    embed.color = discord.Color.from_rgb(255, 255, 0)
    await interaction.message.edit(embed=embed, view=None)
    link = message.content
    try:
        youtubeQuery = YouTube(link)
    except VideoPrivate:
        embed.set_author(name = "『▶』Youtube Downloader:", icon_url = redIcon)
        embed.title = "Este vídeo está privado"
        embed.color = discord.Color.from_rgb(255, 0, 0)
        await interaction.message.edit(embed = embed)
        return
    except VideoUnavailable:
        embed.set_author(name = "『▶』Youtube Downloader:", icon_url = redIcon)
        embed.title = "Este vídeo está indisponível"
        embed.color = discord.Color.from_rgb(255, 0, 0)
        await interaction.message.edit(embed = embed)
        return
    youtubeObject = youtubeQuery.streams.get_highest_resolution()
    videoName = f"resultado.{format}"
    dirPath = str(os.getcwd()) + f"/videos"
    filePath = dirPath + f"/{videoName}"
    try:
        yt = youtubeObject.download(filename = videoName, output_path=dirPath)
    except Exception as e:
        print(e)
        embed.set_author(name = "『▶』Youtube Downloader:", icon_url = redIcon)
        embed.title = "Não foi possível baixar o vídeo"
        embed.color = discord.Color.from_rgb(255, 0, 0)
        await message.channel.send(embed = embed)
        return
    ageRestriction = "Não"
    if youtubeQuery.age_restricted:
        ageRestriction = "Sim"
    embed.title = youtubeQuery.title
    embed.set_thumbnail(url = youtubeQuery.thumbnail_url)
    embed.add_field(name = "『©』Autor:", value = f"[{youtubeQuery.author}]({youtubeQuery.channel_url})")
    embed.add_field(name = "『⏫』Data de publicação:", value = f"`{youtubeQuery.publish_date}`")
    embed.add_field(name = "『👁』Visualizações:", value = f"`{youtubeQuery.views}`")
    embed.add_field(name = "『🔞』Restrição de idade:", value = f"`{ageRestriction}`")
    await interaction.message.edit(embed = embed)

    try:
        match submit:
            case "server":
                await message.channel.send(content = message.author.mention, file = discord.File(filePath))
            case "dm":
                await interaction.user.send(file = discord.File(filePath))
            case "topic":
                topic = await interaction.message.create_thread(name = youtubeQuery.title[:100])
                await topic.send(content = message.author.mention, file = discord.File(filePath))
        embed.set_author(name = "『▶』Youtube Downloader:", icon_url = greenIcon)
        embed.color = discord.Color.from_rgb(0, 255, 0)
    except Exception as e:
        print("❌", e)
        embed.set_author(name = "『▶』Youtube Downloader:", icon_url = redIcon)
        embed.title = "Este vídeo é muito grande"
        embed.color = discord.Color.from_rgb(255, 0, 0)
    await interaction.message.edit(embed = embed)
    if os.path.exists(f"videos/{videoName}"):
        os.remove(f"videos/{videoName}")
    return

class ytFormatView1(discord.ui.View):
    def __init__(self, bot, message, embed, configs):
        super().__init__(timeout = None)
        self.bot = bot
        self.message = message
        self.embed = embed
        self.configs = configs

    @discord.ui.button(label = f"MP3", style = discord.ButtonStyle.blurple, emoji = "🔊", disabled = False)
    async def mp3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "mp3"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))

    @discord.ui.button(label = f"WAV", style = discord.ButtonStyle.gray, emoji = "🔊", disabled = False)
    async def wav(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "wav"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))
    
    @discord.ui.button(label = f"OGG", style = discord.ButtonStyle.gray, emoji = "🔊", disabled = False)
    async def ogg(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "ogg"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))
    
    @discord.ui.button(label = f"M4A", style = discord.ButtonStyle.gray, emoji = "🔊", disabled = False)
    async def m4a(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "m4a"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))

    @discord.ui.button(label = f"FLAC", style = discord.ButtonStyle.gray, emoji = "🔊", disabled = False)
    async def flac(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "flac"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))

    @discord.ui.button(label = f"MP4", style = discord.ButtonStyle.blurple, emoji = "📹", disabled = False)
    async def mp4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "mp4"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))
    
    @discord.ui.button(label = f"MP2", style = discord.ButtonStyle.gray, emoji = "🔊", disabled = False)
    async def mp2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "mp2"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))
        
    @discord.ui.button(label = f"AAC", style = discord.ButtonStyle.gray, emoji = "📹", disabled = False)
    async def aac(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "aac"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))
    
    @discord.ui.button(label = f"M4R", style = discord.ButtonStyle.gray, emoji = "📹", disabled = False)
    async def m4r(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "m4r"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))

    @discord.ui.button(label = f"WMA", style = discord.ButtonStyle.gray, emoji = "📹", disabled = False)
    async def wma(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            fileFormat = "wma"
            self.embed.add_field(name = "『⏬』Formato:", value = f"`.{fileFormat}`", inline = True)
            self.configs["format"] = fileFormat
            self.embed.title = "Por onde deseja receber o vídeo?"
            await interaction.message.edit(embed=self.embed, view=ytSubmitView(bot=self.bot, message=self.message, embed=self.embed, configs = self.configs))

class ytSubmitView(discord.ui.View):
    def __init__(self, bot, message, embed, configs):
        super().__init__(timeout = None)
        self.bot = bot
        self.message = message
        self.embed = embed
        self.configs = configs
    
    @discord.ui.button(label = f"Servidor", style = discord.ButtonStyle.blurple, emoji = "🌃", disabled = False)
    async def serverSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            self.configs["submit"] = "server"
            print(self.configs)
            await downloadVideo(self.bot, self.message, self.embed, interaction, self.configs["format"], self.configs["submit"])
        
    @discord.ui.button(label = f"DM", style = discord.ButtonStyle.blurple, emoji = "👤", disabled = False)
    async def dmSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            self.configs["submit"] = "dm"
            print(self.configs)
            await downloadVideo(self.bot, self.message, self.embed, interaction, self.configs["format"], self.configs["submit"])
    
    @discord.ui.button(label = f"Tópico", style = discord.ButtonStyle.blurple, emoji = "🗨", disabled = False)
    async def topicSend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.message.author.id == interaction.user.id:
            await interaction.response.defer()
            self.configs["submit"] = "topic"
            print(self.configs)
            await downloadVideo(self.bot, self.message, self.embed, interaction, self.configs["format"], self.configs["submit"])

async def youtube(bot, message):
    if message.author.bot == True:
        return
    if not str(message.content).startswith("https://"):
        await message.delete()
        return
    print(message.content)
    configs = {
        "format": None,
        "submit": None
    }
    ytEmbed = discord.Embed(
        title = "Selecione o formato do vídeo",
        color = discord.Color.from_rgb(50, 100, 255)
    )
    ytEmbed.set_author(name = "『▶』Youtube Downloader:", icon_url = blueIcon)
    ytEmbed.add_field(name = "『🔗』URL:", value = f"{message.content}", inline = False)
    ytEmbed.set_footer(text = f"Pedido por {message.author.name}", icon_url = message.author.display_avatar.url)
    await message.delete()
    await message.channel.send(content = f"{message.author.mention}", embed = ytEmbed, view = ytFormatView1(bot=bot, message=message, embed=ytEmbed, configs = configs))