import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import os
import json
import aiohttp
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate

c = open("../config.json")
config = json.load(c)

l = open("../link.json")
link = json.load(l)

intents = discord.Intents.default()
intents.members = True

prefix = config["prefix"]
bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec = 0, per_min = 0, per_hour = 0, type = commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

bot.ses = aiohttp.ClientSession()
class cog_play_slash(commands.GroupCog, name = "play"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @discord.app_commands.command(name = "song", description = "『🎵』Toca uma música de uma URL do Youtube!", nsfw = False)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def play_song(self, interaction: discord.Interaction, url: str):
        try:
            await interaction.response.defer(ephemeral=True, thinking=True)
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.edit_message(embed = userPermAdmin, ephemeral = True)
                return
            
            playEmbed = discord.Embed(
                title = f"Procurando música...",
                color = discord.Color.from_rgb(210, 30, 255)
            )
            playEmbed.set_author(name = f"『🎵』Play Youtube:", icon_url = self.bot.user.display_avatar.url)
            playEmbed.set_footer(text = f"Pedido por {interaction.user.name}", icon_url = interaction.user.display_avatar.url)
            playEmbed.set_thumbnail(url = "https://i.imgur.com/9oIvET7.gif")
            #msg = await interaction.response.send_message(embed = playEmbed, ephemeral = True)

            youtubeQuery = YouTube(url)
            youtubeObject = youtubeQuery.streams.get_highest_resolution()
            videoName = f"song.mp3"
            dirPath = str(os.getcwd()) + f"/audios"
            filePath = dirPath + f"/{videoName}"
            yt = youtubeObject.download(filename = videoName, output_path=dirPath)
            playEmbed.title = youtubeQuery.title
            playEmbed.set_thumbnail(url = youtubeQuery.thumbnail_url)
            playEmbed.add_field(name = "『©』Autor:", value = f"[{youtubeQuery.author}]({youtubeQuery.channel_url})")
            playEmbed.add_field(name = "『⏫』Data de publicação:", value = f"`{youtubeQuery.publish_date}`")
            playEmbed.add_field(name = "『👁』Visualizações:", value = f"`{youtubeQuery.views}`")
            
            msg = await interaction.original_response()
            await msg.edit(embed = playEmbed)
            voice_channel = interaction.user.voice.channel
            print(voice_channel)
            if voice_channel != None:
                vc = await voice_channel.connect()
                audioSource = discord.FFmpegPCMAudio(f"{videoName}")
                vc.play(audioSource, after=None)
            return
        except Exception as e:
            print(e)

async def setup(bot):
    print(f"/play")
    await bot.add_cog(cog_play_slash(bot))