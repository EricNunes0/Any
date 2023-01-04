import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import json
import aiohttp

now = datetime.datetime.now()
date = now.strftime("%d/%m/%Y - %H:%M:%S")
ts = now.timestamp()
print(ts)

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

async def create_afk(userId):
    users = await get_afk_users()
    if str(userId) in users:
        return False
    else:
        users[str(userId)] = {}
        users[str(userId)]["afk"] = False
        users[str(userId)]["reason"] = "Não informado"
        users[str(userId)]["time"] = "Não definido"

    with open("../jsons/afk.json","w") as f:
        json.dump(users, f)
    return True

async def get_afk_users():
    with open("../jsons/afk.json", "r") as f:
        users = json.load(f)
    return users

async def update_afk(userId, status, reason, time):
    users = await get_afk_users()
    users[str(userId)]["afk"] = status
    if reason == None:
        users[str(userId)]["reason"] = "Não informado"
    else:
        users[str(userId)]["reason"] = reason
    if time != None:
        users[str(userId)]["time"] = time
    with open("../jsons/afk.json","w") as f:
        json.dump(users, f)
    stats = users[str(userId)]["afk"]
    return stats

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Administrador`", color = 0xFF0000)
botPermAdmin.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")

bot.ses = aiohttp.ClientSession()
class cog_afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "afk", aliases = ["awayfromkeyboard"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def afk(self, ctx, option: str = None, *, reason: str = None):
        try:
            afkHelpEmbed = discord.Embed(title = f"『🔕』{prefix}afk", color = discord.Color.from_rgb(20, 90, 255))
            afkHelpEmbed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.display_avatar.url)
            afkHelpEmbed.add_field(name = f"『ℹ️』Descrição:", value = f"`Ative o modo AFK para que todos saibam que você não pode responder mensagens no momento!`", inline = False)
            afkHelpEmbed.add_field(name = f"『🔀』Sinônimos:", value = f"`{prefix}awayfromkeyboard`", inline = False)
            afkHelpEmbed.add_field(name = f"『⚙️』Uso:", value = f"`{prefix}afk <on/off> (motivo)`", inline = False)
            afkHelpEmbed.add_field(name = f"『🟢』Ligar:", value = f"`{prefix}afk on Estou trabalhando`", inline = False)
            afkHelpEmbed.add_field(name = f"『🔴』Desligar:", value = f"`{prefix}afk off`", inline = False)
            afkHelpEmbed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Administrador`", inline = False)
            afkHelpEmbed.set_footer(text=f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
            afkHelpEmbed.set_thumbnail(url = link["blueHelp"])
            if option == None:
                await ctx.reply(embed = afkHelpEmbed)
                return
            dateTimeNow = datetime.datetime.now()
            timeStamp = dateTimeNow.timestamp()
            if option.lower() == "on":
                await create_afk(ctx.author.id)
                if reason == None:
                    reason = "Não informado"
                await update_afk(ctx.author.id, True, reason, int(timeStamp))
                afkOnEmbed = discord.Embed(
                    title = f"AFK ligado!",
                    description = f"O afk será desativado assim que você enviar uma mensagem.",
                    color = discord.Color.from_rgb(50, 100, 255)
                )
                afkOnEmbed.set_author(name = f"『🔕』AFK:", icon_url = self.bot.user.display_avatar.url)
                afkOnEmbed.add_field(name = f"『👤』Usuário:", value = f"{ctx.author.mention} `({ctx.author.id})`", inline = True)
                afkOnEmbed.add_field(name = f"『⏰』Definido em:", value = f"<t:{int(timeStamp)}> (<t:{int(timeStamp)}:R>)", inline = True)
                afkOnEmbed.add_field(name = f"『💬』Mensagem:", value = f"`{reason}`", inline = False)
                afkOnEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
                afkOnEmbed.set_thumbnail(url = link["blueChecked"])
                await ctx.reply(embed = afkOnEmbed)
                return
            elif option.lower() == "off":
                await create_afk(ctx.author.id)
                if reason == None:
                    reason = "Não informado"
                await update_afk(ctx.author.id, False, reason, None)
                afkOnEmbed = discord.Embed(
                    title = f"AFK desligado!",
                    description = f"Seu afk foi desativado com sucesso!",
                    color = discord.Color.from_rgb(50, 100, 255)
                )
                afkOnEmbed.set_author(name = f"『🔔』AFK:", icon_url = self.bot.user.display_avatar.url)
                afkOnEmbed.set_footer(text = f"Pedido por {ctx.author.name}", icon_url = ctx.author.display_avatar.url)
                afkOnEmbed.set_thumbnail(url = link["blueChecked"])
                await ctx.reply(embed = afkOnEmbed)
                return
            else:
                await ctx.reply(embed = afkHelpEmbed)
        except Exception as e:
            print(e)

    @afk.error
    async def afk_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print("a!afk ligado!")
    await bot.add_cog(cog_afk(bot))