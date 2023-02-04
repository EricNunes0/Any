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
class cog_sorteioRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "sorteiorules", aliases = ["sorteiorule", "rulessorteios", "rulesorteios", "regrassorteios", "regrassorteio", "regrasorteio"], pass_context = True)
    @has_permissions(administrator = True)
    @cooldown(1, 3, type = commands.BucketType.user)
    async def button(self, ctx, message: discord.Message = None):
        try:
            jc = "<:JannyCoin:969659132913274910>"
            roles1Embed = discord.Embed(
                title = "<a:g_CoolCat:908670092362014770> REGRAS DOS SORTEIOS <a:g_CoolCat:908670092362014770>",
                color = discord.Color.from_rgb(153, 16, 238)
            )
            roles1Embed.add_field(name = "Como participar?", inline = False, value = 
"""
Para participar dos sorteios, é necessário que você pegue o cargo <@&1047164668088688700> no <#1068578017292599356> e acesse o canal <#1047160583302164550> nos horários que houver sorteios disponíveis! Todos os sorteios possuem seus próprios requisitos, que são tarefas das quais você deverá cumprir para poder participar. Ao final do sorteio, caso você tenha sido sorteado e tiver cumprido os requisitos, o prêmio será seu! <a:d_8bitLaserDance:908674226288988230>
"""
            )
            roles1Embed.add_field(name = "Horários:", inline = False, value = 
"""
Todos os dias temos sorteios disponíveis das 12h até 20h.
"""
            )
            roles1Embed.add_field(name = "Requisitos:", inline = False, value = 
"""
Os requisitos sempre serão diferentes em cada um dos sorteios, e apenas serão considerados vencedores aqueles que cumprirem eles e e forem sorteados! Os sorteios são divididos em 5 níveis de dificuldade, de acordo com o nível de dificuldade dos requisitos estabelecidos. Vale lembrar que quanto maior o nível de dificuldade, maior será a recompensa para o vencedor!
"""
            )
            roles1Embed.add_field(name = "Níveis de dificuldade:", inline = False, value = 
f"""
<:ab_RedStar:1061774588796751962> ➺ Muito fáceis (250K {jc} - 500K {jc})
<:ab_OrangeStar:1061774638536982558> ➺ Fáceis (1M {jc} - 2M {jc})
<:ab_YellowStar:1061774704668577872> ➺ Médios (2M {jc} - 4M {jc})
<:ab_GreenStar:1061774738411753572> ➺ Difíceis (4M {jc} - 6M {jc})
<:ab_BlueStar:1061774767268565042> ➺ Muito difíceis (+6M {jc})
"""
            )
            roles1Embed.add_field(name = "Atenção:", inline = False, value = 
f"""
Ao final dos sorteios, vamos verificar se todos os vencedores cumpriram totalmente os requisitos. Em caso de não terem sido cumpridos, o vencedor não vai receber sua recompensa, e daremos reroll (sortearemos novamente)!
"""
            )
            roles1Embed.set_image(url = "https://i.imgur.com/VPvEKP0.png")
            roles1Embed.set_footer(text = "Sorteios da Janny City!")
            await message.edit(content = "", embed = roles1Embed)
            return
        except Exception as e:
            print(e)

    @button.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = userPermAdmin)
    
async def setup(bot):
    print(f"{prefix}roles")
    await bot.add_cog(cog_sorteioRules(bot))