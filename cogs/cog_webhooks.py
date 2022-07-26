import discord
from discord.ext import commands
import animec
import datetime
import random
import json
now = datetime.datetime.now()
now = now.strftime("%d/%m/%Y às %H:%M:%S")

class cog_webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ednaldopereira"])
    #@cooldown(1,2, type = commands.BucketType.user)
    async def ednaldo(self, ctx):
        frases = ["Não importa o que os outros pensam de negatividade de mim... o que importa é o que eu penso de positividade de mim",
        "Se a vida te derrubar, aproveite e olhe baixo da saia dela",
        "Caiu? Levante-se e não derrube quem te derrubou, ele vai cair sozinho",
        "\"Ain, eu queria ser o Ednaldo Pereira\"\nClaro que queria, até eu queria ser ele",
        "Dizem que eu pego todas as mulheres, e eu pego\nSeu nome é \'mulher\' 😉",
        "Duas mulheres brigavam sobre quem é mais bonita\nQuando eu cheguei, as duas disseram: \"É o Ednaldo Pereira\"",
        "Você não vale nada, você vale tudo\nVocê topa qualquer parada, pois você quer se tudo, e não é nada",
        "Não importa o que eu ganhei\nNão importa o que eu gastei\nE sim importa é o que de bom eu vivenciei",
        "Como conseguir uma namorada:\nChega perto dela e fala bem baixinho no ouvido dela: \'Ednaldo Pereira\'",
        "Quem é Ednaldo Pereira?.\n\nPara o cego, Ednaldo é a luz.\nPara o faminto, Ednaldo é o pão.\nPara o sedento, Ednaldo é a fonte.\nPara o enfermo, Ednaldo é a cura.\nPara o prisioneiro, Ednaldo é a liberdade.\nPara o mentiroso, Ednaldo é a verdade.\nPara o viajante, Ednaldo é o caminho.",
        ]
        frase = random.choice(frases)
        webhook = await ctx.channel.create_webhook(name="Ednaldo Pereira")
        await webhook.send(
            str(frase), username="Ednaldo Pereira", avatar_url="https://i.imgur.com/jt74KLL.jpg")

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    @commands.command(aliases=["senseiraylamm","mestreraylamm","railam","senseirailam","mestrerailam","raylam","senseiraylam","mestreraylam"])
    #@cooldown(1,2, type = commands.BucketType.user)
    async def raylamm(self, ctx):
        frases = ["Jiu-jitsu🥋, evolução⬆️\nTerra🌎 de cachorro🐶 louco🤪\nDeu mole😥, não❌ defendeu🛡️\nPego🤚 o braço💪 e o pescoço🙅‍♂️",
        "Jiu-jitsu🥋, evolução⬆️\nArte🎨 milenar🗿\nEncaixou🫂, não❌ bateu...👊\nSe prepara😮 vai apagar😵"
        ]
        frase = random.choice(frases)
        webhook = await ctx.channel.create_webhook(name="Grão Mestre Raylamm")
        await webhook.send(
            str(frase), username="Grão Mestre Raylamm", avatar_url="https://pbs.twimg.com/profile_images/642243374989250560/zYQGxVDo_400x400.jpg")

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    @commands.command(aliases=["ericachan","erica-chan"])
    #@cooldown(1,2, type = commands.BucketType.user)
    async def erica(self, ctx , *, mensagem):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name="Erica-Chan")
        await webhook.send(
            str(mensagem), username="Erica-Chan", avatar_url="https://media.discordapp.net/attachments/740760158098948097/927742750345035826/unknown.png?width=535&height=468")

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

def setup(bot):
    bot.add_cog(cog_webhooks(bot))