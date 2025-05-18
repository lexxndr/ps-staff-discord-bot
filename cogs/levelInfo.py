import disnake, disnake.ui as ui
from disnake.ext import commands

class LevelInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = {"Badges": "<:Badge:1372922191934656612>", "Description": "<:Description:1372561094014537830>", "Tutorial": "<:Objective:1372561114524553226>", "Entities": "<:Skull:1372670255284883476>", "Fun Facts": "<:Tips:1372670198125035571>", "Level Type": "<:Note:1372670234841845973>", "Simulation Cores": "<:Core:1372922221265293395>"}
            # available emojis
            # <:Origin:1372670213702811728>; <:Question:1372670182937460766>; <:Exit:1372670158610632905>; <:Gallery:1372670132249296946>; <:Wrench:1372670271957368893>, <:Overview:1372561106219827341>

    @commands.slash_command(name='level', description='Shows information about a specified level.')
    async def level_info(self, interaction: disnake.CommandInteraction, level: str):

        async def init_components(level: str):
            content = self.bot.jsones["new_level.json"][level]
            sections = content['sections']
            images = content['images']

            container = ui.Container(
                ui.TextDisplay(f'# {level}'),
                ui.Separator(spacing=disnake.SeparatorSpacingSize.small),
                *[
                    item
                    for key, value in sections.items()
                    for item in (
                        ui.TextDisplay(f"## {self.emoji_list.get(key, '')}  {key}\n>>> {value}"),
                        ui.Separator(spacing=disnake.SeparatorSpacingSize.large),
                    )
                ],
                ui.TextDisplay('## <:Gallery:1372670132249296946>  Gallery'),
                ui.MediaGallery(
                    *[
                        item
                        for value in images
                        for item in (
                            disnake.MediaGalleryItem({"media": {"url": value}}),
                        )
                    ],
                ),
                accent_colour=disnake.Colour(0xf0b000),
                spoiler=False,
            )
            return container
        try:
            container = await init_components(level=level)

            await interaction.response.send_message(components=container, flags=disnake.MessageFlags(is_components_v2=True))
            og_message = await interaction.original_message()

            level_names = list(self.bot.jsones["new_level.json"].keys())
            options = [disnake.SelectOption(label=level, value=level) for level in level_names]
            dropdown = disnake.ui.StringSelect(placeholder="Select a level", options=options)

            async def dropdown_callback(interaction: disnake.MessageInteraction):
                # uncomment if ephemeral=False
                #if interaction.author != og_message.interaction_metadata.user:
                    #await interaction.response.send_message("Only the author of the message can use this dropdown.", ephemeral=True) 
                    #return
                container = await init_components(level=interaction.values[0])
                await og_message.edit(components=container)
                await interaction.response.defer()

            dropdown.callback = dropdown_callback

            view = disnake.ui.View()
            view.add_item(dropdown)
            
            await interaction.followup.send(view=view, ephemeral=True)
        except KeyError:
            await interaction.response.send_message(f"*Incorrect option picked!*\nPlease, wait for all the options to appear.\n-# If nothing shows up after some time, report this to the developer.", ephemeral=True)
    
    @level_info.autocomplete("level")
    async def level_autocomplete(self, string: str):
        if not self.bot.jsones["new_level.json"]:
            return []
        
        suggestions = [
            level_name for level_name in self.bot.jsones["new_level.json"].keys()
            if string.lower() in level_name.lower()
        ][:25] # discord limit

        return suggestions

def setup(bot): # setup the cog
    bot.add_cog(LevelInfo(bot))