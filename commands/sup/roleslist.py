import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, BotMissingPermissions, MissingPermissions
import datetime
import json
import aiohttp

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
class cog_roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "roleslist", aliases = ["rolelist"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def button(self, ctx, message1: discord.Message = None, message2: discord.Message = None, message3: discord.Message = None):
        try:
            a_R = "<a:a_ArrowRight:1071105209603993620>"
            if message1 != None:
                roles1Embed = discord.Embed(
                    title = "<a:ab_RedRight:975521519184785428> CARGOS DA ADMINISTRAÇÃO <a:ab_RedLeft:975521412817248306>",
                    color = discord.Color.from_rgb(240, 40, 40),
                    description = 
f"""
Este canal tem o intuito de apresentar os cargos mais importantes do servidor, e as suas respectivas funções.

**<:e_Policia:1070011396294721547> CARGOS DA ADMINISTRAÇÃO:**
{a_R} <@&981694221729816607> ➺ Exclusivo para os bots principais do servidor, o **Any** e o **Janny**!
{a_R} <@&789133849841106994> ➺ Exclusivo para o dono do servidor e criador dos bots **Any** e **Janny**! É a autoridade máxima do servidor, responsável por tomar a maioria das decisões e administrar a comunidade.
{a_R} <@&739210760567390250> ➺ São os administradores do servidor que, assim como o dono, possuem a mesma autoridade e funções, então melhor tomar cuidado com o que faz, os adms estão sempre de olho. <:j_Felizuhul:1058536894805319690>

**<:d_Anotando:1067236947002671124> CARGOS DA STAFF:**
{a_R} <@&793689864469217290> ➺ São os moderadores responsáveis por moderar os membros nos chats de conversa.
{a_R} <@&1054734844434845726> ➺ Movimentam os canais de conversa para manter a atividade no servidor.
{a_R} <@&912505147907788890> ➺ Responsáveis por buscar parcerias em outros servidores.
{a_R} <@&1070416785276420106> ➺ Administram os VIP's do servidor, atendendo e tirando dúvidas sobre os mesmos.
{a_R} <@&1057303437886377984> ➺ Responsáveis por criar eventos para a comunidade.
{a_R} <@&1057303786311405598> ➺ Responsáveis por criar e encerrar os sorteios diários do servidor.
{a_R} <@&1057303954792394794> ➺ Responsáveis por criar e encerras os drops do servidor.
{a_R} <@&1066494361937915914> ➺ Responsáveis por gerenciar os cargos do servidor.
{a_R} <@&1058439007492649010> ➺ Responsáveis por gerenciar os emojis do servidor (criar, editar, excluir).
{a_R} <@&1070416957108650014> ➺ Responsáveis por receber os membros novos e orientá-los dentro do servidor.
"""
                )
                roles1Embed.set_image(url = "https://i.imgur.com/HLHZGBa.png")
                roles1Embed.set_footer(text = "Cargos da administração")
                await message1.edit(content = "", embed = roles1Embed)
            if message2 != None:
                roles2Embed = discord.Embed(
                    title = "<a:ab_RedRight:975521519184785428> CARGOS ESPECIAIS <a:ab_RedLeft:975521412817248306>",
                    color = discord.Color.from_rgb(0, 40, 200),
                    description = 
f"""
**<:c_Style:1067231459066257508> CARGOS ESPECIAIS:**
{a_R} <@&909804122889388072> ➺ Exclusivo para os representantes de servidores parceiros.
{a_R} <@&960291907030896671> ➺ Exclusivo para os membros que impulsionaram o servidor.
{a_R} <@&957296352537219152> ➺ Exclusivo para os aniversariantes do dia. Para ganhar este cargo, informe a sua data de aniversário para um administrador.
{a_R} <@&1071237235044778025> ➺ Entregue para os membros com mais mensagens enviadas na semana (confira o <#1070104992637263922>).
{a_R} <@&966737140635533332> ➺ Entregue para os membros que postam memes frequentemente no <#770662960510140456>.
"""
                )
                roles2Embed.set_image(url = "https://i.imgur.com/e827NQN.png")
                roles2Embed.set_footer(text = "Cargos especiais")
                await message2.edit(content = "", embed = roles2Embed)
            if message3 != None:
                roles3Embed = discord.Embed(
                    title = "<a:ab_RedRight:975521519184785428> CARGOS DE RANKING <a:ab_RedLeft:975521412817248306>",
                    color = discord.Color.from_rgb(255, 210, 0),
                    description = 
f"""
**<:c_Anjinho:1067228675910672425> CARGOS DE RANKING:**
{a_R} <@&723119617488322671> ➢ Cargo padrão que todos os membros recebem ao entrar no servidor.
{a_R} <@&723162586899808346>  ➺ Nível necessário: 10
{a_R} <@&710508609674674246> ➺Nível necessário: 20
{a_R} <@&803677796224073779> ➺ Nível necessário: 35
{a_R} <@&710508893637181452> ➺ Nível necessário: 50
{a_R} <@&797832690396954644> ➺ Nível necessário: 65
{a_R} <@&803678859647123466>️ ➺ Nível necessário: 80
{a_R} <@&803679348363231233> ➺ Nível necessário: 100
{a_R} ??? ➺ Nível necessário: 200

*OBS: Os cargos acima são obtidos no ranking da Loritta!*
"""
                )
                roles3Embed.set_image(url = "https://i.imgur.com/L0O9XHk.png")
                roles3Embed.set_footer(text = "Cargos de ranking")
                await message3.edit(content = "", embed = roles3Embed)
        
        except Exception as e:
            print(e)

    @button.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}roles")
    await bot.add_cog(cog_roles(bot))