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

userPermAdmin = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar emojis`", color = 0xFF0000)
userPermAdmin.set_thumbnail(url = link["error"])
botPermAdmin = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar emojis`", color = 0xFF0000)
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
class cog_addemoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "addemoji", aliases = ["ce", "addemj", "createemoji", "createemj", "createmj", "criaremoji", "criaremj", "emjadd", "emjcreate", "emjcriar", "emojiadd", "emojicreate", "emojicriar"], pass_context = True)
    @bot_has_permissions(manage_emojis = True)
    @has_permissions(manage_emojis = True)
    @cooldown(1,5, type = commands.BucketType.user)
    async def addemoji(self, ctx, url: str = None, name = None):
        try:
            checkReply = ctx.message.reference != None
            if len(ctx.message.attachments) != 0:
                name = url
                url = ctx.message.attachments[0]
            elif checkReply == True:
                repliedMsg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
                if not repliedMsg.attachments[0]:
                    url = url
                else:
                    name = url
                    url = repliedMsg.attachments[0]
            addemojiHelp = discord.Embed(title = f"『😀』{prefix}addemoji", color = discord.Color.from_rgb(20, 90, 255))
            addemojiHelp.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.display_avatar.url)
            addemojiHelp.add_field(name = f"『ℹ️』Descrição:", value = f"`Crie um emoji através de um anexo/link.`", inline = False)
            addemojiHelp.add_field(name = f"『🔀』Sinônimos:", value = f"`{prefix}createemoji, {prefix}criaremoji`", inline = False)
            addemojiHelp.add_field(name = f"『⚙️』Uso:", value = f"`{prefix}addemoji <URL> <nome>`", inline = False)
            addemojiHelp.add_field(name = f"『💬』Exemplo:", value = f"`{prefix}addemoji <URL> new_emoji`", inline = False)
            addemojiHelp.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Gerenciar emojis e figurinhas`", inline = False)
            addemojiHelp.set_footer(text = f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
            addemojiHelp.set_thumbnail(url = link["blueHelp"])
            if url == None or name == None:
                await ctx.reply(embed = addemojiHelp)
            print(url, name)
            async with aiohttp.ClientSession() as ses:
                async with ses.get(str(url)) as r:
                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await ctx.guild.create_custom_emoji(image = b_value, name = name)
                            dateTimeNow = datetime.datetime.now()
                            timeStamp = dateTimeNow.timestamp()
                            createdEmoji = discord.Embed(title = f"Emoji criado: {emoji.name}",
                            #description = f"『✅』O emoji foi criado com sucesso!\n『➡️』Emoji: {emoji}",
                            color = discord.Color.from_rgb(20, 90, 255)
                            )
                            createdEmoji.set_author(name = f"『😀』Add emoji:", icon_url = self.bot.user.display_avatar.url)
                            createdEmoji.add_field(name = "『😀』Emoji criado:", value = f"{emoji} `({emoji.id})`", inline = False)
                            createdEmoji.add_field(name = "『👤』Pedido por:", value = f"{ctx.author.mention} `({ctx.author.id})`", inline = False)
                            createdEmoji.add_field(name = "『🕐』Criado em:", value = f"<t:{int(timeStamp)}> (<t:{int(timeStamp)}:R>)", inline = False)
                            createdEmoji.add_field(name = "『🔣』Menção:", value = f"`{emoji}`", inline = False)
                            createdEmoji.add_field(name = "『🔗』URL:", value = f"[Clique aqui para baixar]({emoji.url})", inline = False)
                            createdEmoji.set_thumbnail(url = link["blueChecked"])
                            createdEmoji.set_footer(text = f"Pedido por {ctx.author.name}", icon_url= ctx.author.display_avatar.url)
                            await ctx.reply(embed = createdEmoji)
                            await ses.close()
                        else:
                            await ctx.send(f'『❌』{ctx.author.mention}, houve um erro ao criar o emoji! Informe o link da imagem, e o nome do emoji!\n『💬』Exemplo: `{prefix}addemoji <link> <nome do emoji>`')
                            await ses.close()
                    except discord.HTTPException:
                        await ctx.send(f'『❌』{ctx.author.mention}, o tamanho do arquivo é muito grande.')
        except Exception as e:
            print(e)
    @addemoji.error
    async def addemoji_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.reply(embed = botPermAdmin)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}addemoji")
    await bot.add_cog(cog_addemoji(bot))