import discord
import random
import json

class onMemberJoinRow(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

async def editVoiceChannel(channel, count):
    await channel.edit(name = f"『🌟』Membros: {count}")
    print("Contador de membros editado")
    try:
        await channel.connect()
    except Exception as e:
        print(e)

async def onMemberJoin(bot, member):
    try:
        linkJson = open("../link.json", encoding = "utf8")
        link = json.load(linkJson)
        if member.guild.id == 710506024489976028:
            print(f"『📤』Um usuário entrou no servidor! {member}")
            welcomeChannel = bot.get_channel(723155037332832296)
            print(welcomeChannel)
            welEmjs = ["<a:ab_8bitLaserDance:908674226288988230>", "<a:ab_AnimeDance:908671238451396618>", "<a:ab_BarriguinhaMole:908669226758340659>", "<a:ab_BobDance:908669712664256562>", "<a:ab_CyanDance:908673970503553047>", "<a:ab_Caverinha:960384154900500490>"]
            e = random.choice(welEmjs)
            guildMemberAdd = discord.Embed(title = f"{e} Seja bem-vindo(a)! {e}", color = discord.Color.from_rgb(240, 210, 0))
            guildMemberAdd.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.display_avatar.url)
            guildMemberAdd.add_field(name = f"〔<a:ab_LevelDown:1051238512319537283>〕Confira:", value = f"**『{link['grayDiamond']}』Regras:** <#1064003850228473876>\n**『{link['greenDiamond']}』Registre-se:** <#1068578017292599356>\n**『{link['redDiamond']}』Use o Janny:** <#970038786908127273>\n**『{link['purpleDiamond']}』Participe dos nossos sorteios:** <#1047160583302164550>")
            guildMemberAdd.set_thumbnail(url = member.display_avatar.url)
            guildMemberAdd.set_footer(text = f"ID: {member.id}", icon_url = member.display_avatar.url)
            print("Embed criado")
            view = onMemberJoinRow()
            view.add_item(discord.ui.Button(label = "Regras", style = discord.ButtonStyle.link, emoji = "📃", url = "https://discord.com/channels/710506024489976028/1064003850228473876"))
            view.add_item(discord.ui.Button(label = "Registre-se", style = discord.ButtonStyle.link, emoji = "📋", url = "https://discord.com/channels/710506024489976028/1068578017292599356"))
            view.add_item(discord.ui.Button(label = "Janny", style = discord.ButtonStyle.link, emoji = "🎰", url = "https://discord.com/channels/710506024489976028/970038786908127273"))
            view.add_item(discord.ui.Button(label = "Sorteios", style = discord.ButtonStyle.link, emoji = "🎉", url = "https://discord.com/channels/710506024489976028/1047160583302164550"))
            print("Row criado")
            await welcomeChannel.send(content = member.mention, embed = guildMemberAdd, view = view)
            print("Mensagem de boas vindas enviada")
            return
    except Exception as e:
        print(e)