import discord
from discord.ext import commands
import datetime
import json

intents = discord.Intents.default()
intents.members = True
now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y - %H:%M:%S")

command_prefix = "a!"
bot = commands.Bot(command_prefix = "a!", intents=intents,  case_insensitive = True)

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

current_language = "pt"

class cog_util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="util", aliases = ["🔑"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def util(self, ctx):
        embed = discord.Embed(title = f"『🔑』Utilidades [22]",description =  "**`anime - avatar - banner - calc - channelinfo - color - data - emoji - emojiinfo - firstmessage - font - guildicon - languages - membros - roleinfo - roleuser - serverinfo - timer - translate - userinfo - userroles - weather`**",color = 0x308020)
        embed.set_footer(text=f"• Para obter informações de cada comando, digite {command_prefix}help <comando>", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/heRA5YW.gif")
        await ctx.reply(embed=embed)

    @commands.command(name='avatar')
    @cooldown(1,3, type = commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar_url
        embed = discord.Embed(
            title = "🖼 " + ctx.author.name,
            description = f"Clique [aqui]({userAvatar}) para baixar",
            color = 0x308020
        )
        embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        embed.set_image(url=userAvatar)
        await ctx.send(embed=embed)

    @commands.command(name="calc", aliases = ["calcular","calcule"])
    @cooldown(1,2, type = commands.BucketType.user)
    async def calc(self, ctx, *, expression=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        if expression == None:
            await ctx.send(f"❌| Por favor {ctx.author.mention}, informe um cálculo.\n⁉| Para mais informações sobre o comando, digite `{prefix}help calc`")
            return
        expression = "".join(expression)
        response = eval(expression)
        await ctx.send("A resposta é: " + str(response))

    @commands.command(name="channelinfo", aliases = ["infochannel","chatinfo"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def channelinfo(self, ctx):
        member = ctx.message.author
        nsfw = "Sim" if ctx.channel.is_nsfw() else "Não"
        embed = discord.Embed(
            title = f"Informações do canal:",
            color = 0x308020
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        fields = [("✍| Nome:", f"`{ctx.channel.name}`", True),
        ("💻| ID", f"`{ctx.channel.id}`", True),
        #("📍| Descrição", f"`{ctx.channel.description}`", True),
        ("🕰| Criado em:", ctx.channel.created_at.strftime("`%d/%m/%Y às %H:%M`"), True),
        ("🔞| NSFW:", f"`{nsfw}`", True),
        #("\u200b", "\u200b", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " às " + now + f"| 💰", icon_url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name= "data")
    @cooldown(1,2, type = commands.BucketType.user)
    async def data(self, ctx):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        await ctx.reply(f"⌚| Data e hora atual: **{now}**\n<:anicoin:919293624850727022>|")

    @commands.command(name="emoji", aliases=["emj"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def emoji(self, ctx, emoji: discord.PartialEmoji = None):
        if not emoji:
            await ctx.send(f"❌| {ctx.author.mention}, informe o emoji.")
        else:
            await ctx.send(emoji.url)

    @commands.command(name="emojiinfo", aliases = ["emojinfo","infoemoji"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def emojiinfo(self, ctx, emoji: discord.Emoji = None):
        if emoji == None:
            await ctx.send(f"❌| {ctx.author.mention}, informe o emoji.")
            return

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except:
            return await ctx.send("Não foi possível encontrar o emoji.")

        emjManaged = "Sim" if emoji.managed else "Não"
        emjAnimated = "Sim" if emoji.animated else "Não"
        emjCreation = emoji.created_at.strftime("%d/%m/%Y às %H:%M:%S")
        emojiUse = "@everyone" if not emoji.roles else " ".join(role.name for role in emoji.roles)

        embed = discord.Embed(
            title = f"Informações do emoji: <:{emoji.name}:{emoji.id}>",
            description = f"**✏| Nome:** `{emoji.name}`\n**ℹ| ID:** `{emoji.id}`\n**@| Código:** `{emoji}`\n**⏬| Download:** [Link para baixar]({emoji.url})\n**👑| Criador:** {emoji.user.mention}\n**📆| Criado em:** `{emjCreation}`\n**👥| Quem pode usar:** {emojiUse}\n**🌠| Animado:** `{emjAnimated}`\n**⚙| Restrito à moderação:** `{emjManaged}`\n**🌆| Servidor do emoji:** `{emoji.guild.name}`",
            color = 0x308020
        )
        embed.set_thumbnail(url=emoji.url)
        embed.set_footer(text=f"Pedido por {ctx.author.name} em {now} | 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", aliases = ["ui","infouser","memberinfo","perfil"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")    
        if member == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, mencione um usuário!")
            return
        userAvatar = member.avatar_url
        creation_time = member.created_at.strftime("%d/%m/%Y às %H:%M:%S")
        joined_time = member.joined_at.strftime("%d/%m/%Y às %H:%M:%S")
        embed = discord.Embed(
            title = f"{member.name}",
            color = member.colour
        )
        if member.bot == True:
            embed.set_author(name=f"{member.name} 「🤖」", icon_url=userAvatar)   
        else:
            embed.set_author(name=f"{member.name}", icon_url=userAvatar)
        
        embed.add_field(name="📕| Tag de Usuário:", value=f"`{member.name}#{member.discriminator}`", inline=True)
        embed.add_field(name="💻| ID:", value=f"`{member.id}`", inline=True)
        embed.add_field(name="🗓| Conta criada em:", value=f"`{creation_time}`", inline=True)
        embed.add_field(name="📆| Entrou em:", value=f"`{joined_time}`", inline=True)
        embed.set_thumbnail(url=userAvatar)
        embed.set_footer(text="Pedido por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="roleinfo", aliases = ["ri","inforole"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role = None):
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")    
        if role == None:
            await ctx.send(f"**❌| {ctx.author.mention}**, mencione um cargo!")
            return
        creation_time = role.created_at.strftime("%d/%m/%Y às %H:%M:%S")
        integration = "Sim" if role.is_integration() else "Não"
        bot_managed = "Sim" if role.is_bot_managed() else "Não"
        membros = []
        for user in ctx.guild.members:
            if role in user.roles:
                membros.append(f"『{user.mention}』")
        number_users = len(membros)
        embed = discord.Embed(
            title = f"{role.name}",
            color = role.colour
        )
        embed.set_author(name=f"{ctx.guild.name} 「🤖」", icon_url=ctx.guild.icon_url)
        
        embed.add_field(name="@| Menção:", value=f"`<@&{role.id}>`", inline=True)
        embed.add_field(name="💻| ID:", value=f"`{role.id}`", inline=True)
        embed.add_field(name="🗓| Criado em:", value=f"`{creation_time}`", inline=True)
        embed.add_field(name="🎨| Cor:", value=f"`{role.color}`", inline=True)
        embed.add_field(name="👤| Membros:", value=f"`{number_users}`", inline=True)
        embed.add_field(name="🤖| Integração:", value=f"`{bot_managed}`", inline=True)
        #embed.add_field(name="🔧| Gerenciado por bot:", value=f"`{bot_managed}`", inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="roleuser", aliases=["userrole","userole"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def roleuser(self, ctx, role: discord.Role = None):
        membros = []
        role = discord.utils.find(
            lambda r: r.id == role.id, ctx.guild.roles)
        for user in ctx.guild.members:
            if role in user.roles:
                membros.append(f"『{user.mention}』")
        number_users = len(membros)
        embed = discord.Embed(title = f"🧳| Usuários com a role {role.name} 『{number_users}』", description = "".join(reversed(membros)), color = 0x308020)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name="serverinfo", aliases = ["infoserver","guildinfo","si"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def serverinfo(self, ctx):
        member = ctx.message.author
        owner = ctx.message.guild.owner
        usuarios = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        ban = len(await ctx.guild.bans())
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        roles = len(ctx.guild.roles)
        invites = len(await ctx.guild.invites())
        emojis = len(ctx.guild.emojis)
        embed = discord.Embed(
            title = f"Informações do Servidor:",
            color = 0x308020
        )
        online = len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
        idle = len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
        dnd = len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
        offline = len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        fields = [("✍| Nome:", f"`{ctx.guild.name}`", True),
        ("💻| ID", f"`{ctx.guild.id}`", True),
        ("👑| Dono:", owner.mention, True),
        ("🌎| Região:", f"`{ctx.guild.region}`", True),
        ("🕰| Criado em:", ctx.guild.created_at.strftime("`%d/%m/%Y às %H:%M`"), True),
        ("👥| Membros:", f"`{ctx.guild.member_count}`", True),
        ("👤| Usuários:", f"`{usuarios}`", True),
        ("🤖| Bots:", f"`{bots}`", True),
        ("⛔| Usuários banidos:", f"`{ban}`", True),
        ("ℹ| Status dos Membros:", f"🟢 `{online}` 🟡 `{idle}` 🔴 `{dnd}` ⚫ `{offline}`", True),
        ("📚| Canais de Texto:", f"`{text_channels}`", True),
        ("🔊| Canais de Voz:", f"`{voice_channels}`", True),
        ("🗂| Categorias:", f"`{categories}`", True),
        ("🗃| Cargos:", f"`{roles}`", True),
        ("✉| Convites:", f"`{invites}`", True),
        ("😀| Emojis:", f"`{emojis}`", True),
        #("\u200b", "\u200b", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " às " + now + "| 💰 +1", icon_url=member.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="servers", aliases=["grupos","servidores","guilds"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def servers(self, ctx):
        servidores = []
        for guild in bot.guilds:
            servidores.append(f"『{guild.name}』")
            print(guild.name)
        number_guilds = len(servidores)
        embed = discord.Embed(title = f"🌎| Servidores onde eu estou: 『{number_guilds}』", description = "".join(servidores), color = 0x308020)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " em " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name="userroles", aliases=["roles","useroles"])
    @cooldown(1,3, type = commands.BucketType.user)
    async def userroles(self, ctx, member: discord.Member):
        roles = []
        for role in member.roles:
            if role.name != "@everyone":
                roles.append(f"『<@&{role.id}>』")
        number_roles = len(roles)
        embed = discord.Embed(title = f"💼| Cargos do @{member} 『{number_roles}』", description = "".join(reversed(roles)), color = 0x308020)
        embed.set_footer(text="Requisitado por " + ctx.author.name + " às " + now + f"| 💰", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

async def setup(bot):
    print("cog_util.py loaded")
    await bot.add_cog(cog_util(bot))