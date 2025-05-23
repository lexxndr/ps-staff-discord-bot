import disnake, disnake.ui as ui
from disnake.ext import commands

class Entities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_list = {"Badge Type": "<:Badge:1372922191934656612>", "Description": "<:Description:1372561094014537830>", "Tutorial": "<:Objective:1372561114524553226>", "Fun Facts": "<:Tips:1372670198125035571>"}
            # available emojis
            # <:Origin:1372670213702811728>; <:Question:1372670182937460766>; <:Exit:1372670158610632905>; <:Gallery:1372670132249296946>; <:Wrench:1372670271957368893>, <:Overview:1372561106219827341>

    @commands.slash_command(name='entity', description='Shows information about a specified entity.')
    async def entities(self, interaction: disnake.CommandInteraction, entity: str):

        async def init_components(entity: str):
            content = self.bot.jsones["entities.json"][entity]
            sections = content['sections']
            images = content['images']

            container = ui.Container(
                ui.Section(
                    ui.TextDisplay(f'# {entity}'), accessory=ui.Thumbnail(media={"url": images[0]})
                    ),
                ui.Separator(spacing=disnake.SeparatorSpacingSize.small),
                *[
                    item
                    for key, value in sections.items()
                    for item in (
                        ui.TextDisplay(f"## {self.emoji_list.get(key, '')}  {key}\n>>> {value}"),
                        ui.Separator(spacing=disnake.SeparatorSpacingSize.small), 
                    )
                ],
                ui.TextDisplay('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀'), # probably the only way to make the size of the embed be constant
                accent_colour=disnake.Colour(0xf0b000),
                spoiler=False
            )
            return container
        try:
            container = await init_components(entity)
            await interaction.response.send_message(components=container, flags=disnake.MessageFlags(is_components_v2=True))
            og_message = await interaction.original_message()

            entity_names = list(self.bot.jsones["entities.json"].keys())
            options = [disnake.SelectOption(label=entity, value=entity) for entity in entity_names]
            dropdown = disnake.ui.StringSelect(placeholder="Select an entity", options=options)

            async def dropdown_callback(interaction: disnake.MessageInteraction):
                # uncomment if ephemeral=False
                #if interaction.author != og_message.interaction_metadata.user:
                    #await interaction.response.send_message("Only the author of the message can use this dropdown.", ephemeral=True) 
                    #return
                container = await init_components(entity=interaction.values[0])
                await og_message.edit(components=container)
                await interaction.response.defer()

            dropdown.callback = dropdown_callback

            view = disnake.ui.View()
            view.add_item(dropdown)
            
            await interaction.followup.send(view=view, ephemeral=True)
        except KeyError:
            await interaction.response.send_message(f"*Incorrect option picked!*\nPlease, wait for all the options to appear.\n-# If nothing shows up after some time, report this to the developer.", ephemeral=True)
    
    @entities.autocomplete("entity")
    async def entity_autocomplete(self, string: str):
        if not self.bot.jsones["entities.json"]:
            return []
        
        suggestions = [
            entity_name for entity_name in self.bot.jsones["entities.json"].keys()
            if string.lower() in entity_name.lower()
        ][:25] # discord limit

        return suggestions

def setup(bot): # setup the cog
    bot.add_cog(Entities(bot))