import discord
import json
import random

class registerGenderRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_gender_{random.randint(0, 1000)}", placeholder = f"Escolha um gênero:", options = [
        discord.SelectOption(
            label = "Masculino",
            emoji = "🚹",
            value = 770251885268434984
        ),
        discord.SelectOption(
            label = "Feminino",
            emoji = "🚺",
            value = 770256373589213205
        ),
        discord.SelectOption(
            label = "Não-binário",
            emoji = "🚻",
            value = 908742556421091328
        ),
        discord.SelectOption(
            label = "Outro",
            emoji = "👤",
            value = 1048619483322916964
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerGenderInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for role in self.json["registerRolesGender"]:
                    if int(role) in rolesIds:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            if int(value) == 0:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Gênero", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todos os gêneros!")
                return
            else:
                registerGenderRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você escolheu o gênero: {registerGenderRole.mention}",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Gênero", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(registerGenderRole)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu o gênero {registerGenderRole}!")
            return
        except Exception as e:
            print(e)

class registerAgeRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_age_{random.randint(0, 1000)}", placeholder = f"Escolha sua idade:", options = [
        discord.SelectOption(
            label = "+18",
            emoji = "🍺",
            value = 908743910027825212
        ),
        discord.SelectOption(
            label = "13 à 17",
            emoji = "🍷",
            value = 908743909688098907
        ),
        discord.SelectOption(
            label = "-13",
            emoji = "🧃",
            value = 1048621342049706044
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerAgeInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for role in self.json["registerRolesAge"]:
                    if int(role) in rolesIds:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            if int(value) == 0:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Idade", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as idades!")
                return
            else:
                registerAgeRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você escolheu a idade: {registerAgeRole.mention}",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Idade", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(registerAgeRole)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu a idade {registerAgeRole}!")
            return
        except Exception as e:
            print(e)

class registerRelationshipRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_relationship_{random.randint(0, 1000)}", placeholder = f"Escolha seu status de relacionamento:", options = [
        discord.SelectOption(
            label = "Solteiro",
            emoji = "👤",
            value = 770717169750114324
        ),
        discord.SelectOption(
            label = "Comprometido",
            emoji = "💞",
            value = 770717226491838474
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerRelationshipInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for role in self.json["registerRolesRelationship"]:
                    if int(role) in rolesIds:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            if int(value) == 0:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Relacionamento", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todos os relacionamentos!")
                return
            else:
                registerRelationshipRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você escolheu o relacionamento: {registerRelationshipRole.mention}",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Relacionamento", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(registerRelationshipRole)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu o relacionamento {registerRelationshipRole}!")
            return
        except Exception as e:
            print(e)

class registerSexualityRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_sexuality_{random.randint(0, 1000)}", placeholder = f"Escolha sua orientação sexual:", options = [
        discord.SelectOption(
            label = "Hétero",
            emoji = "👫",
            value = 770716258215526431
        ),
        discord.SelectOption(
            label = "LGBTQIA+",
            emoji = "🏳️‍🌈",
            value = 770716350976884774
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerSexualityInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for role in self.json["registerRolesSexuality"]:
                    if int(role) in rolesIds:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            if int(value) == 0:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Orientação sexual", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as orientações sexuais!")
                return
            else:
                registerSexualityRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você escolheu a orientação sexual: {registerSexualityRole.mention}",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Orientação sexual", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(registerSexualityRole)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu a orientação sexual {registerSexualityRole}!")
            return
        except Exception as e:
            print(e)

class registerHobbiesRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_hobbies_{random.randint(0, 1000)}", placeholder = f"Escolha seus hobbies:", max_values = 12, options = [
        discord.SelectOption(
            label = "Animes",
            emoji = "🍡",
            value = 908744651362684998
        ),
        discord.SelectOption(
            label = "Mangás",
            emoji = "🗒",
            value = 908744651375251466
        ),
        discord.SelectOption(
            label = "Séries",
            emoji = "📺",
            value = 908744651563991060
        ),
        discord.SelectOption(
            label = "Filmes",
            emoji = "🎞",
            value = 908744652180574288
        ),
        discord.SelectOption(
            label = "Esportes",
            emoji = "⚽",
            value = 908745189806448660
        ),
        discord.SelectOption(
            label = "Jogos",
            emoji = "🕹",
            value = 908745566652088360
        ),
        discord.SelectOption(
            label = "Livros",
            emoji = "📚",
            value = 1048624150245290024
        ),
        discord.SelectOption(
            label = "Programação",
            emoji = "👨‍💻",
            value = 1048624968046477455
        ),
        discord.SelectOption(
            label = "Desenhar",
            emoji = "🎨",
            value = 1048627050988195881
        ),
        discord.SelectOption(
            label = "Música",
            emoji = "🎹",
            value = 1048638519876268122
        ),
        discord.SelectOption(
            label = "Apostas",
            emoji = "🎰",
            value = 1048639876758777916
        ),
        discord.SelectOption(
            label = "Viajar",
            emoji = "🛫",
            value = 1048659796850643004
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerSexualityInteraction(self, interaction: discord.Interaction, select):
        try:
            rolesSelected = []
            userRoles = []
            addedRoles = []
            removedRoles = []
            addedRolesText = []
            removedRolesText = []
            for value in select.values:
                rolesSelected.append(int(value))
            for role in interaction.user.roles:
                userRoles.append(int(role.id))
            if 0 in rolesSelected:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Hobbies", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                for role in self.json["registerRolesHobbies"]:
                    if int(role) in userRoles:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todos os hobbies!")
                return
            registerEmbed = discord.Embed(
                title = f"Hobbies",
                color = discord.Color.from_rgb(210, 30, 30)
            )
            registerEmbed.set_footer(text = "Registro - Hobbies", icon_url = self.bot.user.display_avatar.url)
            for roleSelected in rolesSelected:
                if roleSelected in userRoles:
                    removedRoles.append(str(roleSelected))
                    removedRolesText.append(f"<@&{roleSelected}>")
                else:
                    addedRoles.append(str(roleSelected))
                    addedRolesText.append(f"<@&{roleSelected}>")
            if len(addedRoles) >= 1:
                registerEmbed.add_field(name = "『✅』Hobbies adicionados:", value = "\n".join(addedRolesText), inline = False)
            if len(removedRoles) >= 1:
                registerEmbed.add_field(name = "『❌』Hobbies removidos:", value = "\n".join(removedRolesText), inline = False)
            await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
            for rr in removedRoles:
                registerHobbieRemove = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(rr))
                await interaction.user.remove_roles(registerHobbieRemove)
            for ar in addedRoles:
                registerHobbieAdd = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(ar))
                await interaction.user.add_roles(registerHobbieAdd)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu novos hobbies!")
            return
        except Exception as e:
            print(e)

class registerRegionRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_region_{random.randint(0, 1000)}", placeholder = f"Escolha sua região:", options = [
        discord.SelectOption(
            label = "Norte",
            emoji = "🏕️",
            value = 966131471863660554
        ),
        discord.SelectOption(
            label = "Nordeste",
            emoji = "🏖",
            value = 966131715334619226
        ),
        discord.SelectOption(
            label = "Centro-Oeste",
            emoji = "🏞",
            value = 966131907974823947
        ),
        discord.SelectOption(
            label = "Sudeste",
            emoji = "🏙",
            value = 966132076409655367
        ),
        discord.SelectOption(
            label = "Sul",
            emoji = "🌃",
            value = 966132164129345547
        ),
        discord.SelectOption(
            label = "Portugal",
            emoji = "🇵🇹",
            value = 966133492385738792
        ),
        discord.SelectOption(
            label = "Estrangeiro",
            emoji = "✈",
            value = 966196222291480607
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerSexualityInteraction(self, interaction: discord.Interaction, select):
        try:
            value = select.values[0]
            rolesIds = []
            for role in interaction.user.roles:
                rolesIds.append(int(role.id))
            for role in self.json["registerRolesRegion"]:
                if int(role) in rolesIds:
                    removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                    await interaction.user.remove_roles(removeRegisterRole)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            if int(value) == 0:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Região", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todas as regiões!")
                return
            else:
                registerSexualityRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(value))
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você escolheu a região: {registerSexualityRole.mention}",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Região", icon_url = self.bot.user.display_avatar.url)
                await interaction.user.add_roles(registerSexualityRole)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu a região {registerSexualityRole}!")
            return
        except Exception as e:
            print(e)

class registerPingsRow(discord.ui.View):
    def __init__(self, bot, json):
        super().__init__(timeout = None)
        self.bot = bot
        self.json = json
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    @discord.ui.select(custom_id = f"register_pings_{random.randint(0, 1000)}", placeholder = f"Escolha seus cargos:", max_values = 10, options = [
        discord.SelectOption(
            label = "Reviver chat",
            emoji = "🔑",
            value = 960414419496611860
        ),
        discord.SelectOption(
            label = "Notificações do servidor",
            emoji = "🔔",
            value = 962186652565004409
        ),
        discord.SelectOption(
            label = "Atualizações do Janny",
            emoji = "🔺",
            value = 979920087123394630
        ),
        discord.SelectOption(
            label = "Bump",
            emoji = "📈",
            value = 979800757689778226
        ),
        discord.SelectOption(
            label = "Parcerias",
            emoji = "🛎",
            value = 979920562883268638
        ),
        discord.SelectOption(
            label = "Youtube Ping",
            emoji = "🎥",
            value = 979929259210580019
        ),
        discord.SelectOption(
            label = "Eventos",
            emoji = "🥳",
            value = 1047161356626972703
        ),
        discord.SelectOption(
            label = "Sorteios",
            emoji = "🎉",
            value = 1047164668088688700
        ),
        discord.SelectOption(
            label = "Drops",
            emoji = "🎁",
            value = 1047164421300027505
        ),
        discord.SelectOption(
            label = "Espectador",
            emoji = "🍿",
            value = 1028328814369058877
        ),
        discord.SelectOption(
            label = "Remover todos os cargos",
            emoji = "❌",
            value = 0
        )
    ])
    async def registerPingsInteraction(self, interaction: discord.Interaction, select):
        try:
            rolesSelected = []
            userRoles = []
            addedRoles = []
            removedRoles = []
            addedRolesText = []
            removedRolesText = []
            for value in select.values:
                rolesSelected.append(int(value))
            for role in interaction.user.roles:
                userRoles.append(int(role.id))
            if 0 in rolesSelected:
                registerEmbed = discord.Embed(
                    title = f"꧁📋 Registro 📋꧂",
                    description = f"Você removeu todos os cargos!",
                    color = discord.Color.from_rgb(210, 30, 30)
                )
                registerEmbed.set_footer(text = "Registro - Pings", icon_url = self.bot.user.display_avatar.url)
                await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
                for role in self.json["registerRolesPings"]:
                    if int(role) in userRoles:
                        removeRegisterRole = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(role))
                        await interaction.user.remove_roles(removeRegisterRole)
                await alertChannel.send(f"『❌』{interaction.user.mention} `({interaction.user.id})` removeu todos os pings!")
                return
            registerEmbed = discord.Embed(
                title = f"Pings",
                color = discord.Color.from_rgb(210, 30, 30)
            )
            registerEmbed.set_footer(text = "Registro - Pings", icon_url = self.bot.user.display_avatar.url)
            for roleSelected in rolesSelected:
                if roleSelected in userRoles:
                    removedRoles.append(str(roleSelected))
                    removedRolesText.append(f"<@&{roleSelected}>")
                else:
                    addedRoles.append(str(roleSelected))
                    addedRolesText.append(f"<@&{roleSelected}>")
            if len(addedRoles) >= 1:
                registerEmbed.add_field(name = "『✅』Pings adicionados:", value = "\n".join(addedRolesText), inline = False)
            if len(removedRoles) >= 1:
                registerEmbed.add_field(name = "『❌』Pings removidos:", value = "\n".join(removedRolesText), inline = False)
            await interaction.response.send_message(embed = registerEmbed, ephemeral = True)
            for rr in removedRoles:
                registerPingRemove = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(rr))
                await interaction.user.remove_roles(registerPingRemove)
            for ar in addedRoles:
                registerPingAdd = discord.utils.get(self.bot.get_guild(interaction.guild.id).roles, id = int(ar))
                await interaction.user.add_roles(registerPingAdd)
            alertChannel = self.bot.get_channel(self.json["registerAlert"])
            await alertChannel.send(f"『📋』{interaction.user.mention} `({interaction.user.id})` escolheu novos pings!")
            return
        except Exception as e:
            print(e)

async def getRegisterRow(bot):
    try:
        c = open("../jsons/register.json", encoding = "utf8")
        registerJson = json.load(c)
        channel = bot.get_channel(registerJson["registerChannel"])
        #Pegar IDS das mensagens
        registerMessageGender = await channel.fetch_message(registerJson["registerMessageGender"])
        registerMessageAge = await channel.fetch_message(registerJson["registerMessageAge"])
        registerMessageRelationship = await channel.fetch_message(registerJson["registerMessageRelationship"])
        registerMessageSexuality = await channel.fetch_message(registerJson["registerMessageSexuality"])
        registerMessageHobbies = await channel.fetch_message(registerJson["registerMessageHobbies"])
        registerMessageRegion = await channel.fetch_message(registerJson["registerMessageRegion"])
        registerMessagePings = await channel.fetch_message(registerJson["registerMessagePings"])
        #Criar embeds (GÊNERO)
        registerGenderEmbed = discord.Embed(
            title = f"Gênero",
            description = f"『🚹』<@&770251885268434984>\n『🚺』<@&770256373589213205>\n『🚻』<@&908742556421091328>\n『👤』<@&1048619483322916964>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerGenderEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerGenderEmbed.set_footer(text = "Escolha o seu gênero no menu abaixo:", icon_url = bot.user.display_avatar.url)
        #AGE
        registerAgeEmbed = discord.Embed(
            title = f"Idade",
            description = f"『🍺』<@&908743910027825212>\n『🍷』<@&908743909688098907>\n『🧃』<@&1048621342049706044>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerAgeEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerAgeEmbed.set_footer(text = "Escolha a sua idade no menu abaixo:", icon_url = bot.user.display_avatar.url)
        #RELATIONSHIP
        registerRelationshipEmbed = discord.Embed(
            title = f"Status de relacionamento",
            description = f"『👤』<@&770717169750114324>\n『💞』<@&770717226491838474>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerRelationshipEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerRelationshipEmbed.set_footer(text = "Escolha o seu status de relacionamento no menu abaixo:", icon_url = bot.user.display_avatar.url)
        #SEXUALITY
        registerSexualityEmbed = discord.Embed(
            title = f"Orientação sexual",
            description = f"『👫』<@&770716258215526431>\n『🏳️‍🌈』<@&770716350976884774>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerSexualityEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerSexualityEmbed.set_footer(text = "Escolha a sua orientação sexual:", icon_url = bot.user.display_avatar.url)
        #HOBBIES
        registerHobbiesEmbed = discord.Embed(
            title = f"Hobbies",
            description = f"『🍡』<@&908744651362684998>\n『🗒️』<@&908744651375251466>\n『📺』<@&908744651563991060>\n『🎞️‍』<@&908744652180574288>\n『⚽』<@&908745189806448660>\n『🕹』<@&908745566652088360>\n『📚』<@&1048624150245290024>\n『👨‍💻』<@&1048624968046477455>\n『🎨』<@&1048627050988195881>\n『🎹』<@&1048638519876268122>\n『🎰』<@&1048639876758777916>\n『🛫』<@&1048659796850643004>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerHobbiesEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerHobbiesEmbed.set_footer(text = "Escolha os seus hobbies abaixo:", icon_url = bot.user.display_avatar.url)
        #REGION
        registerRegionEmbed = discord.Embed(
            title = f"Região",
            description = f"『🏕️』<@&966131471863660554>\n『🏖️』<@&966131715334619226>\n『🏞️』<@&966131907974823947>\n『🏙️』<@&966132076409655367>\n『🌃』<@&966132164129345547>\n『🇵🇹』<@&966133492385738792>\n『✈️』<@&966196222291480607>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerRegionEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerRegionEmbed.set_footer(text = "Escolha a sua região:", icon_url = bot.user.display_avatar.url)
        #PINGS
        registerPingsEmbed = discord.Embed(
            title = f"Pings",
            description = f"『🔑』<@&960414419496611860>\n『🔔』<@&962186652565004409>\n『🔺』<@&979920087123394630>\n『📈』<@&979800757689778226>\n『🛎️』<@&979920562883268638>\n『📽️』<@&979929259210580019>\n『🥳』<@&1047161356626972703>\n『🎊』<@&1047164668088688700>\n『🎁』<@&1047164421300027505>\n『🍿』<@&1028328814369058877>",
            color = discord.Color.from_rgb(210, 30, 30)
        )
        registerPingsEmbed.set_image(url = "https://media.discordapp.net/attachments/1004090715267141742/1011058426132050021/linha-imagem-animada-0383.gif")
        registerPingsEmbed.set_footer(text = "Escolha os cargos de pings no menu abaixo:", icon_url = bot.user.display_avatar.url)
        
        await registerMessageGender.edit(content = "", embed = registerGenderEmbed, view = registerGenderRow(bot = bot, json = registerJson))
        await registerMessageAge.edit(content = "", embed = registerAgeEmbed, view = registerAgeRow(bot = bot, json = registerJson))
        await registerMessageRelationship.edit(content = "", embed = registerRelationshipEmbed, view = registerRelationshipRow(bot = bot, json = registerJson))
        await registerMessageSexuality.edit(content = "", embed = registerSexualityEmbed, view = registerSexualityRow(bot = bot, json = registerJson))
        await registerMessageHobbies.edit(content = "", embed = registerHobbiesEmbed, view = registerHobbiesRow(bot = bot, json = registerJson))
        await registerMessageRegion.edit(content = "", embed = registerRegionEmbed, view = registerRegionRow(bot = bot, json = registerJson))
        await registerMessagePings.edit(content = "", embed = registerPingsEmbed, view = registerPingsRow(bot = bot, json = registerJson))
    except Exception as e:
        print(e)