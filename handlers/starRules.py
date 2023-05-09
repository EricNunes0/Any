import discord
import random
import asyncio

COLORS_STARS = {
    "emoji": {
        "0": "<:ab_RedStar:1061774588796751962>",
        "1": "<:ab_OrangeStar:1061774638536982558>",
        "2": "<:ab_YellowStar:1061774704668577872>",
        "3": "<:ab_GreenStar:1061774738411753572>",
        "4": "<:ab_BlueStar:1061774767268565042>"
    },
    "colors": {
        "0": [255, 20, 20],
        "1": [255, 120, 20],
        "2": [255, 255, 20],
        "3": [20, 255, 20],
        "4": [20, 120, 255]
    },
    "images": {
        "0": "https://i.imgur.com/LFVzcIs.png",
        "1": "https://i.imgur.com/Mtsj64b.png",
        "2": "https://i.imgur.com/eIIO0zx.png",
        "3": "https://i.imgur.com/31D7w6f.png",
        "4": "https://i.imgur.com/QdaROot.png"
    }
}

async def starRulesLoop(bot, channel):
    try:
        print("START")
        starRulesMsg = await channel.fetch_message("1071285219920977940")
        i = random.randint(0, 4)
        starRolesEmbed = discord.Embed(
            title = f"{COLORS_STARS['emoji'][f'{i}']} CAÇA ÀS ESTRELAS {COLORS_STARS['emoji'][f'{i}']}",
            color = discord.Color.from_rgb(COLORS_STARS["colors"][f"{i}"][0], COLORS_STARS["colors"][f"{i}"][1], COLORS_STARS["colors"][f"{i}"][2]),
            description =
"""
*As estrelas da Janny City são itens colecionáveis do <@900346730237820939>. Seu objetivo é coletar o máximo de estrelas que puder para desbloquear benefícios e conseguir aumentar sua posição no ranking.*
"""
        )
        starRolesEmbed.add_field(name = "『🎨』Cores:", inline = False, value =
"""Use suas estrelas para comprar cores para o seu nome. Confira o canal de <#1064641839027724440> para ver todas as cores disponíveis, e seus preços!"""
        )
        starRolesEmbed.add_field(name = "『🌟』Como conseguir?", inline = False, value =
"""De tempos em tempos, uma mensagem escolhida aleatoriamente no chat de conversas pelo Any, terá uma reação de estrela adicionada por ele. Para obter-la, basta clicar na reação rapidamente, e a mesma será adicionada em seu total de estrelas. Mas cuidado, assim que um membro reagir em uma estrela, a mesma irá desaparecer. Portanto, seja rápido para pega-lá antes que outro membro a pegue!"""
        )
        starRolesEmbed.add_field(name = "『✨』Todas as estrelas:", inline = False, value =
f"""
**{COLORS_STARS['emoji'][f'0']} ➺ 3%**
**{COLORS_STARS['emoji'][f'1']} ➺ 2,5%**
**{COLORS_STARS['emoji'][f'2']} ➺ 2%**
**{COLORS_STARS['emoji'][f'3']} ➺ 1,5%**
**{COLORS_STARS['emoji'][f'4']} ➺ 1%**

*As porcentagens acima referencem a probabilidade das estrelas aparecem em alguma mensagem.*
"""
        )
        starRolesEmbed.add_field(name = "『🌠』Total de estrelas:", inline = False, value =
"""
Como ver o seu total de estrelas: `a!stars`
Como ver o ranking de estrelas do servidor: `a!topstars`
"""
        )
        starRolesEmbed.add_field(name = "『💫』Atenção:", inline = False, value =
"""
As estrelas apenas aparecerão em canais de conversas e apostas do Janny! Elas não aparecerão em quaisquer outros canais (inclusos os canais dedicados para flood/spam de mensagens como o <#931019005609779220>). Ademais, não adianta floodar/spamar mensagem para obter estrelas rapidamente! Caso tente, você receberá uma punição!
"""
        )
        starRolesEmbed.set_image(url = COLORS_STARS['images'][f'{i}'])
        starRolesEmbed.set_footer(text = "Caça às estrelas", icon_url = bot.user.display_avatar.url)
        await starRulesMsg.edit(content = "", embed = starRolesEmbed)
        await asyncio.sleep(3)
    except Exception as e:
        print(e)