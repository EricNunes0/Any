import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import asyncio
import json
import aiohttp
from io import BytesIO

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

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar cargos`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar cargos`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url = link["error"])

class addemojiButtons(discord.ui.View):
    def __init__(self, bot, userId):
        super().__init__()
        self.bot = bot
        self.userId = userId
    
    @discord.ui.button(label = f"Criar", style = discord.ButtonStyle.blurple, emoji = f"➕")
    async def addemojiDisableButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            
            if int(interaction.user.id) == int(self.userId):
                addemojiDisableEmbed = discord.Embed(title = "Seu addemoji foi desativado!",
                color = discord.Color.from_rgb(50, 100, 255))
                addemojiDisableEmbed.set_author(name = "『🔔』addemoji:", icon_url = self.bot.user.display_avatar.url)
                addemojiDisableEmbed.set_thumbnail(url = link["addemojiOffThumb"])
                await interaction.response.edit_message(embed = addemojiDisableEmbed, view = None)
                return
            else:
                invalidUserEmbed = discord.Embed(title = f"Espera aí!", description = f"『❌』Apenas <@{self.userId}> pode desativar o addemoji!", color = 0xFF0000)
                invalidUserEmbed.set_thumbnail(url = link["error"])
                await interaction.response.send_message(embed = invalidUserEmbed, ephemeral = True)
                return
        except Exception as e:
            print(e)

bot.ses = aiohttp.ClientSession()
class cog_addrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "addrole", aliases = ["ar", "roleadd", "giverole", "rolegive", "adicionarcargo", "cargoadicionar", "darcargo", "cargodar"], pass_context = True)
    @bot_has_permissions(manage_emojis = True)
    @has_permissions(manage_emojis = True)
    @cooldown(1,5, type = commands.BucketType.user)
    async def addrole(self, ctx, user: discord.User = None, role: discord.Role = None):
        try:
            if ctx.author.guild_permissions.manage_roles:
                if user != None and role != None:
                    roleToAdd = discord.utils.get(ctx.guild.roles, name = role.name)
                    print(roleToAdd)
                    addedRole = discord.Embed(title = f"Cargo adicionado!", description = f"『✅』O cargo foi adicionado com sucesso!\n『➡️』Cargo: {roleToAdd.mention}", color = 0x40ffb0)
                    addedRole.set_thumbnail(url = "https://i.imgur.com/nKHOkqE.gif")
                    addedRole.set_footer(text=f"Pedido por {ctx.author}", icon_url= ctx.author.display_avatar.url)
                    await ctx.reply(embed = addedRole)
                else:
                    now = datetime.datetime.now()
                    now = now.strftime("%d/%m/%Y - %H:%M:%S")
                    embed = discord.Embed(title = f"『+💼』{prefix}addrole", color = 0x4070ff)
                    embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.display_avatar.url)
                    embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Cria um cargo para o servidor.`", inline = False)
                    embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{prefix}createrole`", inline = False)
                    embed.add_field(name = f"『⚙️』Uso:", value = f"`{prefix}addrole <nome>`", inline = False)
                    embed.add_field(name = f"『💬』Exemplo:", value = f"`{prefix}addrole Novo cargo`", inline = False)
                    embed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Gerenciar cargos`", inline = False)
                    embed.set_footer(text=f"Pedido por {ctx.author}", icon_url= ctx.author.display_avatar.url)
                    embed.set_thumbnail(url="https://i.imgur.com/FEp8F1G.gif")
                    await ctx.reply(embed=embed)
        except Exception as e:
            print(e)

    @addrole.error
    async def addemoji_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.reply(embed = botPermAdmin)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}addrole")
    await bot.add_cog(cog_addrole(bot))