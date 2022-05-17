import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import math
import asyncio
import datetime
from io import BytesIO
import json
import aiohttp

now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

intents = discord.Intents.default()
intents.members = True

#def get_prefix(bot, message):
#    with open('prefixes.json', 'r') as f:
#        prefixes = json.load(f)
#    return prefixes[str(message.guild.id)]
command_prefix = "a!"
bot = commands.Bot(command_prefix = "a!", intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

#async def open_account(user):
#    users = await get_bank_data()

#    if str(user.id) in users:
#        return False
#    else:
#        users[str(user.id)] = {}
#        users[str(user.id)]["wallet"] = 0
#        users[str(user.id)]["bank"] = 0

#    with open("mainbank.json","w") as f:
#        json.dump(users, f)
#    return True

#async def get_bank_data():
#    with open("mainbank.json","r") as f:
#        users=json.load(f)

#    return users

#async def update_bank(user, change = 0, mode = "wallet"):
#    users = await get_bank_data()
#    users[str(user.id)][mode] += change 

#    with open("mainbank.json","w") as f:
#        json.dump(users, f)
#    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
#    return bal

userPermEmoji = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar emojis`", color = 0xFF0000)
userPermEmoji.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
botPermEmoji = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar emojis`", color = 0xFF0000)
botPermEmoji.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")

userPermRole = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar cargos`", color = 0xFF0000)
userPermRole.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
botPermRole = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar cargos`", color = 0xFF0000)
botPermRole.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")

userPermMsg = discord.Embed(title = f"Sem permissão", description = f"『❌』Você não tem as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar mensagens`", color = 0xFF0000)
userPermMsg.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
botPermMsg = discord.Embed(title = f"Eu não tenho permissão", description = f"『❌』Eu não tenho as permissões necessárias para usar este comando!\n『🛠️』Permissões necessárias: `Gerenciar mensagens`", color = 0xFF0000)
botPermMsg.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")

bot.ses = aiohttp.ClientSession()
class cog_mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mod", aliases = ["⚙️"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def mod(self, ctx):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title = f"『⚙』Moderação [28]『<a:ab_GemBlue:936824926671892530>』",description = f"**`addemoji - addrole - ban - clear - clone - createchannel - createinvite - deletechannel - deleteinvites - invites - kick - listban - lock - mute - nuke - removeemoji - removerole - renamechannel - say - sayembed - setguildicon - setguildname - setnick - setprefix - slowmode - unban - unlock - unmute`**",color = 0x0055c5)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {command_prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/Zyaj8U0.gif")
        await ctx.reply(embed=embed)

    @commands.command(name='addemoji', aliases=['createemoji','criaremoji'], pass_context = True)
    @bot_has_permissions(manage_emojis = True)
    @has_permissions(manage_emojis = True)
    @cooldown(1,5, type = commands.BucketType.user)
    async def addemoji(self, ctx, url: str, name):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200,299):
                            emoji = await ctx.guild.create_custom_emoji(image=b_value, name = name)
                            createdEmoji = discord.Embed(title = f"Emoji criado", description = f"『✅』O emoji foi criado com sucesso!\n『➡️』Emoji: {emoji}", color = 0x40ffb0)
                            createdEmoji.set_thumbnail(url = "https://i.imgur.com/nKHOkqE.gif")
                            createdEmoji.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
                            await ctx.reply(embed = createdEmoji)
                            await ses.close()
                        else:
                            await ctx.send(f'『❌』{ctx.author.mention}, houve um erro ao criar o emoji! Informe o link da imagem, e o nome do emoji!\n『💬』Exemplo: `{command_prefix}addemoji <link> <nome do emoji>`')
                            await ses.close()
                    except discord.HTTPException:
                        await ctx.send(f'『❌』{ctx.author.mention}, o tamanho do arquivo é muito grande.')

    @addemoji.error
    async def addemoji_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.reply(embed = botPermEmoji)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermEmoji)
        elif isinstance(error, commands.MissingRequiredArgument):
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            embed = discord.Embed(title = f"『😀』{command_prefix}addemoji", color = 0x4070ff)
            embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.avatar_url)
            embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Cria um emoji com um link.`", inline = False)
            embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{command_prefix}createemoji, {command_prefix}criaremoji`", inline = False)
            embed.add_field(name = f"『⚙️』Uso:", value = f"`{command_prefix}addemoji <URL> <nome>`", inline = False)
            embed.add_field(name = f"『💬』Exemplo:", value = f"`{command_prefix}addemoji <URL> new_emoji`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Gerenciar emojis e figurinhas`", inline = False)
            embed.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/FEp8F1G.gif")
            await ctx.reply(embed=embed)

    @commands.command(name="addrole", aliases=["createrole"])
    @bot_has_permissions(manage_roles = True)
    @has_permissions(manage_roles = True)
    @cooldown(1,3, type = commands.BucketType.user)
    async def addrole(self, ctx, *, name):
        if ctx.author.guild_permissions.manage_roles:
            await ctx.guild.create_role(name = name)
            role = discord.utils.get(ctx.guild.roles, name = name)
            createdRole = discord.Embed(title = f"Emoji criado", description = f"『✅』O cargo foi criado com sucesso!\n『➡️』Cargo: {role.mention}", color = 0x40ffb0)
            createdRole.set_thumbnail(url = "https://i.imgur.com/nKHOkqE.gif")
            createdRole.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
            await ctx.reply(embed = createdRole)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.reply(embed = botPermRole)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermRole)
        elif isinstance(error, commands.MissingRequiredArgument):
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            embed = discord.Embed(title = f"『+💼』{command_prefix}addrole", color = 0x4070ff)
            embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.avatar_url)
            embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Cria um cargo para o servidor.`", inline = False)
            embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{command_prefix}createrole`", inline = False)
            embed.add_field(name = f"『⚙️』Uso:", value = f"`{command_prefix}addrole <nome>`", inline = False)
            embed.add_field(name = f"『💬』Exemplo:", value = f"`{command_prefix}addrole Novo cargo`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Gerenciar cargos`", inline = False)
            embed.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/FEp8F1G.gif")
            await ctx.reply(embed=embed)

    @commands.command(name='clear', aliases= ['purge','delete'])
    @bot_has_permissions(manage_messages = True)
    @has_permissions(manage_messages = True)
    @cooldown(1,3, type = commands.BucketType.user)
    async def clear(self, ctx, amount):
        if ctx.author.guild_permissions.manage_messages:
            try:
                int(amount)
            except:
                NaN = discord.Embed(title = f"Valor inválido", description = f"『❌』{ctx.author.mention}, `{amount}` não é um valor válido!\n『🔢』Informe um valor entre 1 e 1000!", color = 0xFF0000)
                NaN.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
                return await ctx.reply(embed = NaN)
            else:
                await ctx.channel.purge(limit=int(amount) + 1)
                clearedMsg = discord.Embed(title = f"Mensagens apagadas!", description = f"『🧹』O canal teve {int(amount)} mensagens apagadas!", color = 0x40ffb0)
                clearedMsg.set_thumbnail(url = "https://i.imgur.com/nKHOkqE.gif")
                clearedMsg.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
                del_msg = await ctx.send(embed = clearedMsg)
                await asyncio.sleep(5)
                return await del_msg.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.reply(embed = botPermMsg)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermMsg)
        elif isinstance(error, commands.MissingRequiredArgument):
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            embed = discord.Embed(title = f"『🧹』{command_prefix}clear", color = 0x4070ff)
            embed.set_author(name = f"Central de Ajuda do {self.bot.user.name}", icon_url = self.bot.user.avatar_url)
            embed.add_field(name = f"『ℹ️』Descrição:", value = f"`Apaga uma quantidade de mensagens.`", inline = False)
            embed.add_field(name = f"『🔀』Sinônimos:", value = f"`{command_prefix}delete, {command_prefix}purge`", inline = False)
            embed.add_field(name = f"『⚙️』Uso:", value = f"`{command_prefix}clear <número>`", inline = False)
            embed.add_field(name = f"『💬』Exemplo:", value = f"`{command_prefix}clear 10`", inline = False)
            embed.add_field(name = f"『🛠️』Permissões necessárias:", value = f"`Gerenciar mensagens`", inline = False)
            embed.set_footer(text=f"• Pedido por {ctx.author} em {now}", icon_url= ctx.author.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/FEp8F1G.gif")
            await ctx.reply(embed=embed)

    @commands.command(name="color", aliases=["rgb","rbg","grb","gbr","brg","bgr"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def color(self, ctx, color1 : int = None, color2 : int = None, color3 : int = None):
        if color1 == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe a cor em RBG.")
        if color2 == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe a cor em RBG.")
        if color3 == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe a cor em RBG.")
        
        if color1 > 255 or color1 < 0:
            return await ctx.send(f"❌| {ctx.author.mention}, informe um valor de 0 a 255.")
        if color2 > 255 or color1 < 0:
            return await ctx.send(f"❌| {ctx.author.mention}, informe um valor de 0 a 255.")
        if color3 > 255 or color1 < 0:
            return await ctx.send(f"❌| {ctx.author.mention}, informe um valor de 0 a 255.")
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        #await open_account(ctx.author)
        #users = await get_bank_data()
        #earnings = 1
        #users[str(ctx.author.id)]["wallet"] += earnings
        #with open("mainbank.json","w") as f:
        #    json.dump(users,f)
        hex = discord.Colour.from_rgb(color1, color2, color3)
        embed = discord.Embed(
            title = f"Cor ({color1}, {color2}, {color3})",
            color = hex,
        )
        embed.add_field(name="Hex:", value=f"{hex}")
        embed.add_field(name="RBG:", value=f"{color1}, {color2}, {color3}")
        embed.set_footer(text="Requisitado por " + ctx.author.name + " em " + now, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="createchannel", aliases = ["channelcreate","addchannel","channeladd"])
    @cooldown(1,30, type = commands.BucketType.user)
    async def createchannel(self, ctx, *, channel_name = None):
        if ctx.author.guild_permissions.manage_channels:
            if channel_name == None: 
                return await ctx.send(f"**❌| {ctx.author.mention}**, informe o nome do novo canal.\n**⁉|** Para mais informações sobre o comando, digite `a!help createchannel`")
            #await open_account(ctx.author)
            #users = await get_bank_data()
            #earnings = 2
            #users[str(ctx.author.id)]["wallet"] += earnings
            #with open("mainbank.json","w") as f:
            #    json.dump(users,f)
            new_channel = await ctx.guild.create_text_channel(channel_name)
            await new_channel.send(f"**👶| {ctx.author.mention}**, este canal foi criado com sucesso!\n**<:anicoin:919293624850727022>|**")
            await ctx.send(f"**✅| {ctx.author.mention}**, o canal {new_channel.name} foi criado com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para criar canais! Permissões necessárias: `Gerenciar canais`")

    @commands.command(name='createinvite', aliases = ["invite","convite"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def createinvite(self, ctx, time = None):
        #with open('prefixes.json', 'r') as f:
        #    prefixes = json.load(f)
        #prefix = prefixes[str(ctx.guild.id)]
        if ctx.author.guild_permissions.create_instant_invite:
            if time == None:
                await ctx.send(f"⏰| {ctx.author.mention}, você precisa informar o tempo de convite.\n🔸| Tempos disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{command_prefix}createinvite 1m`\n♾️| OBS: Caso queira que o convite nunca expire, use `{command_prefix}createinvite 0s`")
                return
            try:
                seconds = time[:-1]
                duration = time[-1]
                minutes = int(seconds) * 60
                hours = int(seconds) * 3600
                days = int(seconds) * 86400
                if duration.lower() == "s":
                    seconds = seconds * 1
                elif duration.lower() == "m":
                    seconds = int(minutes)
                elif duration.lower() == "h":
                    seconds = int(hours)
                elif duration.lower() == "d":
                    seconds = int(days)
                else:
                    await ctx.send(f"⏱| {ctx.author.mention}, duração de convite inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{command_prefix}createinvite 1m`")
                    return
            except Exception as e:
                print(e)
                await ctx.send(f"⏱| {ctx.author.mention}, tempo de convite inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{command_prefix}createinvite 1m`")
                return
            invitelink = await ctx.channel.create_invite(max_age=seconds)
            embed = discord.Embed(
                title="✉️| Convite criado com sucesso!",
                description=f"**Link do convite:** {invitelink}",
                color = 0x0055c5
            )
            embed.set_footer(text="Criado por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            print(invitelink)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Criar convites`")

    @commands.command(name='invites', aliases = ["allinvites","invitesall","convites"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def invites(self, ctx):
        if ctx.author.guild_permissions.manage_guild:
            embed = discord.Embed(
                title = f"📧| Todos os convites de {ctx.guild.name}:",
                color = 0x0055c5
            )
            loop = [f"**{invite}**" for invite in await ctx.guild.invites()]
            _list = "\r\n".join([f"『{str(num).zfill(2)}』 {data}" for num, data in enumerate(loop, start=1)])
            convites = f"{_list}"
            embed.add_field(name = f"Convites:", value = f"{convites}", inline = False)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para ver convites! Permissões necessárias: `Gerenciar servidor`")

    @commands.command(name="listban", aliases = ["banlist"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def banlist(self, ctx):
        if ctx.author.guild_permissions.manage_guild:
            embed = discord.Embed(
                title = f"Usuários banidos em {ctx.guild.name}:",
                color = 0x0055c5
            )
            bans = await ctx.guild.bans()
            loop = [f"Tag: **{u[1]}** - ID:`{u[1].id}`" for u in bans]
            _list = "\r\n".join([f"『{str(num).zfill(2)}』 {data}" for num, data in enumerate(loop, start=1)])
            banimentos = f"{_list}"
            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
            embed.add_field(name="Bans:", value=banimentos, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para ver a lista de banimentos! Permissões necessárias: `Gerenciar servidor`")

    @commands.command(name="lock")
    @cooldown(1,5, type = commands.BucketType.user)
    async def lock(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(f"{ctx.channel.mention} **foi bloqueado com sucesso! Para desbloquear, use `a!unlock`!**\n<:anicoin:919293624850727022>|")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para bloquear canais. Permissões necessárias: `Gerenciar canais`")

    @commands.command(name="mute", aliases=['mutar','silenciar'])
    @cooldown(1,5, type = commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member=None, time=None, *, reason=None):
        if ctx.author.guild_permissions.mute_members:
            #with open('prefixes.json', 'r') as f:
            #    prefixes = json.load(f)
            #prefix = prefixes[str(ctx.guild.id)]
            if member == None:
                await ctx.send(f"❌| {ctx.author.mention}, você precisa mencionar um usuário.\n⁉| Para mais informações sobre o comando, digite `{command_prefix}help mute`")
                return
            elif member == ctx.message.author:
                await ctx.send(f"❌| {ctx.author.mention}, você não pode se silenciar.")
                return
            elif time == None:
                await ctx.send(f"⏰| {ctx.author.mention}, você precisa informar o tempo de mute.\n🔸| Tempos disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{command_prefix}mute <usuário> 1m`")
                return
            else:
                if not reason:
                    reason="não informado"
                try:
                    seconds = time[:-1]
                    duration = time[-1]
                    minutes = int(seconds) * 60
                    print(int(minutes))
                    hours = int(seconds) * 3600
                    print(int(hours))
                    if duration.lower() == "s":
                        seconds = seconds * 1
                    elif duration.lower() == "m":
                        seconds = int(minutes)
                    elif duration.lower() == "h":
                        seconds = int(hours)
                    else:
                        await ctx.send(f"⏰| {ctx.author.mention}, duração de mute inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{command_prefix}mute <usuário> 1m`")
                        return
                except Exception as e:
                    print(e)
                    await ctx.send(f"⏰| {ctx.author.mention}, tempo de mute inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{command_prefix}mute <usuário> 1m`")
                    return
                guild = ctx.guild
                Muted = discord.utils.get(guild.roles, name="Muted")
                if not Muted:
                    Muted = await guild.create_role(name="Muted")
                    for channel in guild.channels:
                        await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True)
                await member.add_roles(Muted, reason=reason)
                muted_embed = discord.Embed(
                    title="⏳| Usuário mutado",
                    description=f"**Silenciado por:** {ctx.author.mention}\n**Motivo:** `{reason}`\n**Tempo:** `{time}`",
                    color = 0x0055c5
                )
                await ctx.send(embed=muted_embed)
                print(int(seconds))
                await asyncio.sleep(int(seconds))
                print("Fim do mute")
                await member.remove_roles(Muted)
                await ctx.send(f"⌛| {member.mention}, seu mute acabou.")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para silenciar usuários. Permissões necessárias: `Silenciar membros`")

    @commands.command(name="unmute", aliases = ["desmutar","desilenciar"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member=None):
        if ctx.author.guild_permissions.mute_members:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes[str(ctx.guild.id)]
            if member == None:
                await ctx.send(f"❌| {ctx.author.mention}, você precisa mencionar um usuário.\n⁉| Para mais informações sobre o comando, digite `{prefix}help unmute`")
                return
            if member == ctx.author:
                await ctx.send(f"❌| {ctx.author.mention}, você não pode se desmutar.")
                return
            mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)
            await ctx.send(f"⌛| {member.mention}, seu mute acabou.")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para usar esse comando. Permissões necessárias: `Silenciar membros`")

    @commands.command(name="removeemoji", aliases=["deleteemoji","removeremoji","removemoji"])
    @cooldown(1,5, type = commands.BucketType.user)
    async def removeemoji(self, ctx, emoji: discord.Emoji):
        if ctx.author.guild_permissions.manage_emojis:
                await ctx.send(f'**✅| {ctx.author.mention}**, o emoji foi excluído com sucesso!\n**<:anicoin:919293624850727022>|**')
                await emoji.delete()
        else:
                await ctx.send(f"**❌| {ctx.author.mention}**, você não tem permissão para remover emojis neste servidor! Permissões necessárias: `Gerenciar emojis e stickers`")

    @commands.command(name="removerole", aliases=["deleterole","delrole"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def removerole(self, ctx, *, role_name:discord.Role = None):
        membro = ctx.message.author
        if role_name == None:
            await ctx.send(f"❌| {membro.mention}, informe o nome do cargo.")
            return
        if ctx.author.guild_permissions.manage_roles:
            await role_name.delete()
            await ctx.send(f'✅| {membro.mention}, o cargo foi excluído com sucesso!\n**<:anicoin:919293624850727022>| **')
        else:
            await ctx.send(f"❌| {membro.mention}, você não tem permissão para excluir cargos neste servidor! Permissões necessárias: `Gerenciar cargos`")

    @commands.command(name="renamechannel", aliases = ["changechannelname","channelname","namechannel"])
    @cooldown(1,15, type = commands.BucketType.user)
    async def renamechannel(self, ctx, channel: discord.TextChannel = None, *, channel_name = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if ctx.author.guild_permissions.manage_channels:
            if channel == None: 
                return await ctx.send(f"**❌| {ctx.author.mention}**, informe um canal.\n**⁉|** Para mais informações sobre o comando, digite `{prefix}help renamechannel`")
            if channel_name == None: 
                return await ctx.send(f"**❌| {ctx.author.mention}**, informe o novo nome do canal.\n**⁉|** Para mais informações sobre o comando, digite `{prefix}help renamechannel`")
            await channel.edit(name=channel_name)
            await ctx.send(f"**✅| {ctx.author.mention}**, o canal foi renomeado com sucesso!\n**<:anicoin:919293624850727022>|**")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para criar canais! Permissões necessárias: `Gerenciar canais`")

    @commands.command(name="say")
    @cooldown(1,3, type = commands.BucketType.user)
    async def say(self, ctx, *, mensagem = None):
        if ctx.author.guild_permissions.manage_messages:
            if mensagem == None:
                return await ctx.send(f"❌| {ctx.author.mention}, insira uma mensagem.")
            await ctx.send(mensagem)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")

    @commands.command(name="sayembed", aliases=["embedsay"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def sayembed(self, ctx, *, mensagem = None):
        if ctx.author.guild_permissions.manage_messages:
            if mensagem == None:
                return await ctx.send(f"❌| {ctx.author.mention}, insira uma mensagem.")
            embed = discord.Embed(
                description = f"{mensagem}",
                color = 0x0055c5,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")
    
    @commands.command(name='setguildname',aliases=["changeguildname"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def setguildname(self, ctx, *, name=None):
        if ctx.author.guild_permissions.manage_guild:
            if name == None:
                return await ctx.send(f"❌| {ctx.author.mention}, informe o novo nome do servidor!")
            await ctx.guild.edit(name=name)
            await ctx.send(f"📝| {ctx.author.mention}, o nome do servidor foi alterado com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para alterar o nome do servidor! Permissões necessárias: `Gerenciar servidor`")

    @commands.command(name='setguildicon',aliases=["changeguildicon"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def setguildicon(self, ctx, url: str = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if ctx.author.guild_permissions.manage_guild:
            if url == None:
                return await ctx.send(f"❌| {ctx.author.mention}, informe o link do novo ícone do servidor!")
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200,299):
                            changing = await ctx.send(f"<a:ab_carregando:911073196038582272>| Mudando o ícone...!")
                            await ctx.guild.edit(icon=b_value)
                            await changing.edit(f"📝| {ctx.author.mention}, o ícone do servidor alterado com sucesso!")
                            await ses.close()
                        else:
                            await ctx.send(f'❌| {ctx.author.mention}, houve um erro ao alterar o ícone. Informe o link da imagem.\n💬 Exemplo: {prefix}setguildicon <link>')
                            await ses.close()
                    except discord.HTTPException:
                        await ctx.send(f'❌| O tamanho do arquivo é muito grande.')
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para alterar o nome do servidor! Permissões necessárias: `Gerenciar servidor`")

    @commands.command(name='setnick',aliases=["setusernick","setnickuser","setusername","usernameset","changenick","nickchange"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def setnick(self, ctx, member: discord.Member = None, *, nickname):
        if ctx.author.guild_permissions.manage_nicknames:
            if member == None:
                return await ctx.send(f"❌| {ctx.author.mention}, informe um usuário e o novo apelido dele!")
            changing = await ctx.send(f"<a:ab_carregando:911073196038582272>| Mudando o apelido...!")
            await member.edit(nick=nickname)
            await changing.edit(f"📝| {ctx.author.mention}, o apelido do usuário foi alterado com sucesso!")  
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para alterar apelidos! Permissões necessárias: `Gerenciar nicknames`")

    @commands.command(name="slowmode",aliases=['modolento'])
    @cooldown(1,5, type = commands.BucketType.user)
    async def slowmode(self, ctx, time=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if ctx.author.guild_permissions.manage_channels:
            if time == None:
                return await ctx.send(f"⏰| {ctx.author.mention}, você precisa informar o tempo de slowmode.\n🔸| Tempos disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}slowmode 1m`")
            try:
                seconds = time[:-1]
                duration = time[-1]
                minutes = int(seconds) * 60
                hours = int(seconds) * 3600
                if duration.lower() == "s":
                    seconds = seconds * 1
                elif duration.lower() == "m":
                    seconds = int(minutes)
                elif duration.lower() == "h":
                    seconds = int(hours)
                else:
                    await ctx.send(f"⏱| {ctx.author.mention}, duração de slowmode inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}slowmode 1m`")
                    return
            except Exception as e:
                print(e)
                await ctx.send(f"⏱| {ctx.author.mention}, tempo de slowmode inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}slowmode 1m`")
                return
            muted_embed = discord.Embed(
                title="⏱| Modo lento configurado!",
                description=f"**Modo lento definido por:** {ctx.author.mention}\n**Tempo:** `{time}`",
                color = 0x0055c5
            )
            muted_embed.set_footer(text="Configurado por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=muted_embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para definir o modo lento. Permissões necessárias: `Gerenciar canais`")

    @commands.command(name="unban", aliases = ["deleteban","delban"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def unban(self, ctx, *, member: discord.User = None):
        if member == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe o ID do membro que você deseja desbanir!")
        banned_users = await ctx.guild.bans()
        if ctx.author.guild_permissions.manage_guild:
            for ban_entry in banned_users:
                user = ban_entry.user
                if user == member:
                    creation_time = member.created_at.strftime("%d/%m/%Y às %H:%M:%S")
                    embed = discord.Embed(
                        title = f"{user.name} foi desbanido",
                        color = 0x0055c5,
                    )
                    embed.add_field(name="📕| Tag de Usuário:", value=f"`{user.name}#{user.discriminator}`", inline=True)
                    embed.add_field(name="💻| ID:", value=f"`{user.id}`", inline=True)
                    #embed.add_field(name="🗓️| Data de criação:", value=f"`{creation_time}`", inline=True)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + "| 💰 +1", icon_url=ctx.author.avatar_url)
                    await ctx.guild.unban(user)
                    return await ctx.send(embed=embed)
        else:
            return await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para desbanir usuários!")

    @commands.command(name="unlock")
    @cooldown(1,5, type = commands.BucketType.user)
    async def unlock(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send( ctx.channel.mention + f" **foi desbloqueado com sucesso! Para bloquear, use `a!lock`!**\n<:anicoin:919293624850727022>|")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para desbloquear canais. Permissões necessárias: `Gerenciar canais`")

    @commands.command(name="userpermissions", aliases=["permissions","permissões","perms"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def userpermissions(self, ctx, member: discord.Member = None):
        if ctx.author.guild_permissions.administrator:
            if member == None:
                member = ctx.author
            perms = []
            if member.guild_permissions.create_instant_invite:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.kick_members:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.ban_members:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.administrator:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_channels:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_guild:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.add_reactions:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.view_audit_log:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.priority_speaker:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.stream:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.view_channel:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.send_messages:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.send_tts_messages:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_messages:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.embed_links:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.attach_files:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.read_message_history:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.mention_everyone:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.use_external_emojis:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.view_guild_insights:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.connect:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.speak:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.mute_members:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.deafen_members:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.move_members:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.use_voice_activation:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.change_nickname:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_nicknames:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_roles:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_webhooks:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.manage_emojis:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.use_slash_commands:
                perms.append("✅")
            else:
                perms.append("❌")
            if member.guild_permissions.request_to_speak:
                perms.append("✅")
            else:
                perms.append("❌")
            embed = discord.Embed(
                title = f"🔧| Permissões de @{member}:",
                description = f"""
                『{perms[0]}』Criar convites
                『{perms[1]}』Expulsar membros
                『{perms[2]}』Banir membros
                『{perms[3]}』Administrador
                『{perms[4]}』Gerenciar canais
                『{perms[5]}』Gerenciar servidor
                『{perms[6]}』Adiconar reações
                『{perms[7]}』Ver registro de auditoria
                『{perms[8]}』Orador Prioritário
                『{perms[9]}』Ao vivo, Ver canal
                『{perms[10]}』Enviar mensagens
                『{perms[11]}』Enviar mensagens tts
                『{perms[12]}』Gerenciar mensagens
                『{perms[13]}』Enviar embeds e links
                『{perms[14]}』Anexar arquivos
                『{perms[15]}』Ler histórico de mensagens
                『{perms[16]}』Mencione todos
                『{perms[17]}』Usar emojis externos
                『{perms[18]}』Ver os insights do servidor
                『{perms[19]}』Conectar
                『{perms[20]}』Falar
                『{perms[21]}』Mutar membros
                『{perms[22]}』Ensurdecer membros
                『{perms[23]}』Mover membros
                『{perms[24]}』USE_VAD
                『{perms[25]}』Mudar nickname
                『{perms[26]}』Gerenciar nicknames
                『{perms[27]}』Gerenciar cargos
                『{perms[28]}』Gerenciar webhooks
                『{perms[29]}』Gerenciar emojis e stickers
                『{perms[30]}』Usar comandos /
                『{perms[31]}』Pedido para falar
                """,
                color = 0x0055c5)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
            await ctx.send(embed = embed)

    @removeemoji.error
    async def removeemoji_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            #with open('prefixes.json', 'r') as f:
            #    prefixes = json.load(f)
            #prefix = prefixes[str(ctx.guild.id)]
            await ctx.send(f"**❌|** {ctx.author.mention}, informe o emoji que deseja excluir!\n**💬| Exemplo:** {command_prefix}removeemoji <emoji>\n**⁉|** Para mais informações sobre o comando, digite `{command_prefix}help removeemoji`!")

def setup(bot):
    bot.add_cog(cog_mod(bot))