import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommand, SlashContext
import asyncio
import datetime
from io import BytesIO
import json
import aiohttp

now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

intents = discord.Intents.default()
intents.members = True
prefix = "a!"

bot = commands.Bot(command_prefix = prefix, intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

bot.ses = aiohttp.ClientSession()
class cog_s_mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="mod", description="⚙️| Lista de comandos de moderação.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _mod(self, ctx:SlashContext):
        embed = discord.Embed(title = f"『⚙』Moderação [28]『<a:ab_GemBlue:936824926671892530>』",description = f"**`addemoji - addrole - ban - clear - clone - createchannel - createinvite - deletechannel - deleteinvites - embedcreator - invites - kick - listban - lock - mute - nuke - removeemoji - removerole - renamechannel - say - sayembed - setguildicon - setguildname - setnick - slowmode - unban - unlock - unmute`**",color = 0x0055c5)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/Zyaj8U0.gif")
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name ='addemoji', description="😀| Cria um emoji no servidor.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _addemoji(self, ctx: SlashContext, url: str, *, name):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:
                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200,299):
                            emoji = await guild.create_custom_emoji(image=b_value, name = name)
                            await ctx.send(f'**✅| {ctx.author.mention}**, o emoji foi criado com sucesso: <:{name}:{emoji.id}>')
                            await ses.close()
                        else:
                            await ctx.send(f'**❌| {ctx.author.mention}**, houve um erro ao criar o emoji! Informe o link da imagem, e o nome do emoji!\n**💬 Exemplo:** {prefix}addemoji <link> <nome do emoji>')
                            await ses.close()
                    except discord.HTTPException:
                        await ctx.send(f'**❌|** Não foi possível adicionar o emoji pois o tamanho é inválido.')
        else:
            await ctx.send(f"**❌| {ctx.author.mention}**, você não tem permissão para adicionar emojis neste servidor! Permissões necesárias: `Gerenciar emojis e stickers`")

    @cog_ext.cog_slash(name='addrole', description="💼| Cria um cargo no servidor.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _addrole(self, ctx: SlashContext, *, name, r:int = None, g:int = None, b:int = None):
        if name == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe o nome do cargo.")
        if r == None or r < 0:
            r = 0
        if g == None or g < 0:
            g = 0
        if b == None or b < 0:
            b = 0
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
        if ctx.author.guild_permissions.manage_roles:
            hex = discord.Colour.from_rgb(r, g, b)
            await ctx.guild.create_role(name=name, color=hex)
            role = discord.utils.get(ctx.guild.roles, name=name)
            await ctx.send(f'✅| {ctx.author.mention}, o cargo foi criado com sucesso: {role.mention}**')
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para criar cargos neste servidor! Permissões necessárias: `Gerenciar cargos`")

    @cog_ext.cog_slash(name="ban", description="⛔| Bane um usuário.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _ban(self, ctx:SlashContext, member:discord.Member, *,reason=None):
            if member == None:
                await ctx.send(f"❌| {ctx.author.mention}, você precisa mencionar um usuário.")
                return
            if member == ctx.author:
                await ctx.send(f"❌| {ctx.author.mention}, você não pode se banir.")
                return
            if ctx.author.guild_permissions.ban_members:
                await member.ban(reason=reason)
                await ctx.send(f"✅| {member.mention} foi banido do servidor.")
            else:
                await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para banir usuários. Permissões necessárias: `Banir membros`")

    @cog_ext.cog_slash(name='clear', description="❎| Apaga uma quantidade de mensagens.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _clear(self, ctx:SlashContext, amount:int):
        if ctx.author.guild_permissions.manage_messages:
            if amount == None or amount == 0:
                return await ctx.send(f"**❌| {ctx.author.mention}**, informe a quantidade de mensagens para apagar.")
            if amount == None:
                await ctx.channel.purge(limit=1000)
            else:
                try:
                    int(amount)
                except: # Error handler
                    await ctx.send('Digite uma quantidade entre 1 e 1000!')
                else:
                    await ctx.channel.purge(limit=amount + 1)
            del_msg = await ctx.send(f"『<:ab_intAzul:911068022075179098>』O chat teve {amount} mensagens apagadas por {ctx.author.mention}!")
            await asyncio.sleep(5)
            await del_msg.delete()
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para apagar mensagens. Permissões necessárias: `Gerenciar mensagens`")

    @cog_ext.cog_slash(name="kick", description="👞| Expulsa um usuário.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _kick(self, ctx:SlashContext, member:discord.Member, *,reason=None):
        if member == None:
            await ctx.send(f"❌| {ctx.author.mention}, você precisa mencionar um usuário.")
            return
        if member == ctx.author:
            await ctx.send(f"❌| {ctx.author.mention}, você não pode se expulsar.")
            return
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f"✅| {member.mention} foi expulso do servidor.")
        
        
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para expulsar usuários. Permissões necessárias: `Expulsar membros`")

    @cog_ext.cog_slash(name="clone", description="🔃| Clona um canal de texto.")
    @cooldown(1,30, type = commands.BucketType.user)
    async def _clone(self, ctx:SlashContext, channel: discord.TextChannel = None):
        if ctx.author.guild_permissions.manage_channels:
            if channel == None: 
                channel = ctx.channel
            clone_channel = discord.utils.get(ctx.guild.channels, name=channel.name)
            if clone_channel is not None:
                new_channel = await clone_channel.clone(reason="Não informado.")
                await new_channel.send(f"**🤯| {ctx.author.mention}**, o canal foi clonado com sucesso!")
                await ctx.send(f"**🤯| {ctx.author.mention}**, o canal foi clonado com sucesso!")
            else:
                await ctx.send(f"❌| O canal **{channel}** não foi encontrado!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="createchannel", description="👶| Cria um canal de texto.")
    @cooldown(1,30, type = commands.BucketType.user)
    async def _createchannel(self, ctx:SlashContext, *, channel_name):
        if ctx.author.guild_permissions.manage_channels:
            new_channel = await ctx.guild.create_text_channel(channel_name)
            await new_channel.send(f"**👶| {ctx.author.mention}**, este canal foi criado com sucesso!")
            await ctx.send(f"**✅| {ctx.author.mention}**, o canal {new_channel.name} foi criado com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para criar canais! Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name='createinvite', description="✉️| Cria um convite para o servidor.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _createinvite(self, ctx:SlashContext, time = None):
        if ctx.author.guild_permissions.create_instant_invite:
            if time == None:
                await ctx.send(f"⏰| {ctx.author.mention}, você precisa informar o tempo de convite.\n🔸| Tempos disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{prefix}createinvite 1m`\n♾️| OBS: Caso queira que o convite nunca expire, use `{prefix}createinvite 0s`")
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
                    await ctx.send(f"⏱| {ctx.author.mention}, duração de convite inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{prefix}createinvite 1m`")
                    return
            except Exception as e:
                print(e)
                await ctx.send(f"⏱| {ctx.author.mention}, tempo de convite inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas) - d (dias)`\n🔹| Exemplo: `{prefix}createinvite 1m`")
                return
            invitelink = await ctx.channel.create_invite(max_age=seconds)
            embed = discord.Embed(
                title="✉️| Convite criado com sucesso!",
                description=f"**Link do convite:** {invitelink}",
                color = 0x0055c5
            )
            embed.set_footer(text="Criado por " + ctx.author.name + " às " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            print(invitelink)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Criar convites`")

    @cog_ext.cog_slash(name="deletechannel", description="💣| Deleta um canal de texto.")
    @cooldown(1,30, type = commands.BucketType.user)
    async def _deletechannel(self, ctx:SlashContext, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            del_channel = discord.utils.get(ctx.guild.channels, name=channel.name)
            if del_channel is not None:
                await del_channel.delete()
                await ctx.send(f"**💥| {ctx.author.mention}**, o canal {del_channel.name} foi excluído com sucesso!")

            else:
                await ctx.send(f"❌| O canal **{channel.name}** não foi encontrado!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name='deleteinvites', description="📩| Deleta todos os convites do servidor.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _deleeteinvites(self, ctx:SlashContext):
        if ctx.author.guild_permissions.manage_guild:
            delconvites = await ctx.send(f"『<a:ab_carregando:911073196038582272>』| Excluindo convites...")
            for invite in await ctx.guild.invites():
                await invite.delete()
            await delconvites.edit(f"✅| Todos os convites foram excluídos com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para excluir convites! Permissões necessárias: `Gerenciar servidor`")

    @cog_ext.cog_slash(name="embedcreator", description="『💭』Cria uma mensagem embed customizada.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _embedcreator(self, ctx:SlashContext, title = None, description = None, col = None,  autor:discord.Member = None, thumbnail:str = None, image:str = None, footer = None):
#        if ctx.author.guild_permissions.manage_messages:
            if title == None:
                title = ""
            if description == None:
                description = ""
            embed = discord.Embed(title = title, description = description, color = ctx.author.colour)
            if autor != None:
                embed.set_author(name=autor.name, icon_url=autor.avatar_url)
            if thumbnail != None:
                embed.set_thumbnail(url=thumbnail)
            if image != None:
                embed.set_image(url=image)
            if footer != None:
                embed.set_footer(text="\u200b" + now, icon_url=ctx.guild.icon_url)
            if title == None and description == None and autor == None and thumbnail == None and image == None and footer == None:
                noneEmbed = discord.Embed(title = "Embed inexistente", description = "Não é possível criar um embed vazio.", color = 0xff3030)
                noneEmbed.set_thumbnail(url="https://i.imgur.com/uBGwDAM.gif")
                await ctx.channel.send(embed = noneEmbed)
            else:
                await ctx.channel.send("Cadê o embed? 🤔")
#        else:
#            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")

    @cog_ext.cog_slash(name="editembed", description="💭| Edita uma mensagem embed customizada.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _editembed(self, ctx:SlashContext, *, descrição, título, autor:discord.Member = None, thumbnail:str = None, imagem:str = None):
#        if ctx.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title = título,description = descrição,color = ctx.author.colour)
            if autor != None:
                embed.set_author(name=autor.name, icon_url=autor.avatar_url)
            if thumbnail != None:
                embed.set_thumbnail(url=thumbnail)
            if imagem != None:
                embed.set_image(url=imagem)
            embed.set_footer(text="Criado por " + ctx.author.name + " em " + now, icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
#        else:
#            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")


    @cog_ext.cog_slash(name='invites', description="📧| Mostra todos os convites do servidor.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _invites(self, ctx:SlashContext):
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
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para ver convites! Permissões necessárias: `Gerenciar servidor`")

    @cog_ext.cog_slash(name="listban", description="⛔| Mostra todos os usuários banidos do servidor.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _banlist(self, ctx:SlashContext):
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
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Bans:", value=banimentos, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para ver a lista de banimentos! Permissões necessárias: `Gerenciar servidor`")

    @cog_ext.cog_slash(name="lock", description="🔒| Bloqueia um canal de texto.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _lock(self, ctx:SlashContext):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(f"{ctx.channel.mention} **foi bloqueado com sucesso! Para desbloquear, use `a!unlock`!**")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para bloquear canais. Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="mute", description="🤫| Silencia um usuário.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _mute(self, ctx:SlashContext, member: discord.Member, time = None, *, reason=None):
        if ctx.author.guild_permissions.mute_members:
            if member == ctx.author:
                return await ctx.send(f"❌| {ctx.author.mention}, você não pode se silenciar.")
            elif time == None:
                await ctx.send(f"⏰| {ctx.author.mention}, você precisa informar o tempo de mute.\n🔸| Tempos disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}mute <usuário> 1m`")
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
                        await ctx.send(f"⏰| {ctx.author.mention}, duração de mute inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}mute <usuário> 1m`")
                        return
                except Exception as e:
                    print(e)
                    return await ctx.send(f"⏰| {ctx.author.mention}, tempo de mute inválido.\n🔸| Durações disponíveis: `s (segundos) - m (minutos) - h (horas)`\n🔹| Exemplo: `{prefix}mute <usuário> 1m`")
                    
                Muted = discord.utils.get(ctx.guild.roles, name="Muted")
                if not Muted:
                    Muted = await ctx.guild.create_role(name="Muted")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True)
                await member.add_roles(Muted, reason=reason)
                muted_embed = discord.Embed(
                    title="⏳| Usuário mutado",
                    description=f"**Silenciado por:** {ctx.author.mention}\n**Motivo:** `{reason}`\n**Tempo:** `{time}`",
                    color = 0x0055c5
                )
                await ctx.send(embed=muted_embed)
                await asyncio.sleep(int(seconds))
                await member.remove_roles(Muted)
                await ctx.send(f"⌛| {member.mention}, seu mute acabou.")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para silenciar usuários. Permissões necessárias: `Silenciar membros`")

    @cog_ext.cog_slash(name="nuke", description="🧨| Exclui um canal e cria outro com o mesmo nome.")
    @cooldown(1,30, type = commands.BucketType.user)
    async def _nuke(self, ctx:SlashContext, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)
            if nuke_channel is not None:
                new_channel = await nuke_channel.clone(reason="Não informado.")
                await nuke_channel.delete()
                await new_channel.send(f"**🤯| {ctx.author.mention}**, nuke finalizado com sucesso!")
                await ctx.send(f"**🤯| {ctx.author.mention}**, nuke finalizado com sucesso!")
            else:
                await ctx.send(f"❌| O canal **{channel.name}** não foi encontrado!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="removeemoji", description="😕| Exclui um emoji do servidor.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _removeemoji(self, ctx, emoji: discord.Emoji):
        if ctx.author.guild_permissions.manage_emojis:
                await ctx.send(f'**✅| {ctx.author.mention}**, o emoji foi excluído com sucesso!')
                await emoji.delete()
        else:
                await ctx.send(f"**❌| {ctx.author.mention}**, você não tem permissão para remover emojis neste servidor! Permissões necessárias: `Gerenciar emojis e stickers`")

    @cog_ext.cog_slash(name="removerole", description="🛅| Exclui um cargo do servidor.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _removerole(self, ctx, *, role_name:discord.Role = None):
        if ctx.author.guild_permissions.manage_roles:
            if role_name == None:
                return await ctx.send(f"❌| {ctx.author.mention}, informe o nome do cargo.")
            await role_name.delete()
            await ctx.send(f'✅| {ctx.author.mention}, o cargo foi excluído com sucesso!')
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para excluir cargos neste servidor! Permissões necessárias: `Gerenciar cargos`")

    @cog_ext.cog_slash(name="renamechannel", description="✍️| Renomeia um canal do servidor.")
    @cooldown(1,15, type = commands.BucketType.user)
    async def _renamechannel(self, ctx:SlashContext, channel: discord.TextChannel, *, channel_name):
        if ctx.author.guild_permissions.manage_channels:
            await channel.edit(name=channel_name)
            await ctx.send(f"**✅| {ctx.author.mention}**, o canal foi renomeado com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para criar canais! Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="say", description="💬| Faz o bot dizer uma mensagem.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _say(self, ctx:SlashContext, *, mensagem):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send(mensagem)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")

    @cog_ext.cog_slash(name="sayembed", description="🗨️| Faz o bot dizer uma mensagem em Embed.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _sayembed(self, ctx:SlashContext, *, mensagem):
        if ctx.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                description = f"{mensagem}",
                color = 0x0055c5,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now, icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem a permissão para usar este comando! Permissões necessárias: `Gerenciar mensagens`")

    @cog_ext.cog_slash(name='setguildname', description="📝| Muda o nome do servidor.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _setguildname(self, ctx:SlashContext, *, name):
        if ctx.author.guild_permissions.manage_guild:
            if name == None:
                return await ctx.send(f"❌| {ctx.author.mention}, informe o novo nome do servidor!")
            await ctx.guild.edit(name=name)
            await ctx.send(f"📝| {ctx.author.mention}, o nome do servidor foi alterado com sucesso!")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para alterar o nome do servidor! Permissões necessárias: `Gerenciar servidor`")

    @cog_ext.cog_slash(name='setguildicon', description="🌆| Muda o ícone do servidor.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _setguildicon(self, ctx:SlashContext, url: str):
        if ctx.author.guild_permissions.manage_guild:
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

    @cog_ext.cog_slash(name='setnick', description="✏️| Muda o apelido de um usuário.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _setnick(self, ctx:SlashContext, member: discord.Member, *, nickname):
        if ctx.author.guild_permissions.manage_nicknames:
            changing = await ctx.send(f"<a:ab_carregando:911073196038582272>| Mudando o apelido...!")
            await member.edit(nick=nickname)
            await changing.edit(f"📝| {ctx.author.mention}, o apelido do usuário foi alterado com sucesso!")  
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para alterar apelidos! Permissões necessárias: `Gerenciar nicknames`")

    @cog_ext.cog_slash(name="slowmode", description="⏳| Altera o modo lento de um canal de texto.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _slowmode(self, ctx:SlashContext, time=None):
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
            muted_embed.set_footer(text="Configurado por " + ctx.author.name + " às " + now, icon_url=ctx.author.avatar_url)
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=muted_embed)
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para definir o modo lento. Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="unban", description="🚶| Tira o banimento de um usuário.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def unban(self, ctx:SlashContext, *, member_id: discord.User = None):
        if member_id == None:
            return await ctx.send(f"❌| {ctx.author.mention}, informe o ID do membro que você deseja desbanir!")
        banned_users = await ctx.guild.bans()
        if ctx.author.guild_permissions.manage_guild:
            for ban_entry in banned_users:
                user = ban_entry.user
                if user == member_id:
                    creation_time = member_id.created_at.strftime("%d/%m/%Y às %H:%M:%S")
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

    @cog_ext.cog_slash(name="unlock", description="🔓| Desloqueia um canal de texto.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _unlock(self, ctx:SlashContext):
        if ctx.author.guild_permissions.manage_channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send( ctx.channel.mention + f" **foi desbloqueado com sucesso! Para bloquear, use `a!lock`!**")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para desbloquear canais. Permissões necessárias: `Gerenciar canais`")

    @cog_ext.cog_slash(name="unmute", description = "🗣️| Desilencia um usuário.")
    @cooldown(1,5, type = commands.BucketType.user)
    async def _unmute(self, ctx:SlashContext, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if member == ctx.author:
                return await ctx.send(f"❌| {ctx.author.mention}, você não pode se desmutar.")
            mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)
            await ctx.send(f"⌛| {member.mention}, seu mute acabou.")
        else:
            await ctx.send(f"❌| {ctx.author.mention}, você não tem permissão para usar esse comando. Permissões necessárias: `Silenciar membros`")

    @cog_ext.cog_slash(name="votar", description = "🗳️| Inicia uma votação.")
    @cooldown(1,3, type = commands.BucketType.user)
    async def _votar(self, ctx:SlashContext, *, description, minutos:int, emoji:discord.Emoji, channel:discord.TextChannel):
        if ctx.author.guild_permissions.administrator:
            minutos = minutos * 60
            now = datetime.datetime.now()
            now = now.strftime("%d/%m/%Y - %H:%M:%S")
            emj = f'{emoji}'
            valid_reactions = [f'{emoji}']

            embed = discord.Embed(title = f"Votação de {ctx.author.name}:", description = f"{description}", color = ctx.author.colour)
            vote = await channel.send(embed=embed)
            await vote.add_reaction(emj)
            await asyncio.sleep(minutos)
            msg = await vote.channel.fetch_message(vote.id)
            await ctx.send(msg.reactions)
            print("Fim da votação")
        else:
            await ctx.send(f"**❌| {ctx.author.mention}**, você não tem permissão para iniciar votações. Permissões necessárias: `Administrador`")

def setup(bot):
    bot.add_cog(cog_s_mod(bot))