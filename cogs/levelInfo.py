import disnake, aiohttp, aiofiles, dotenv, json, os, disnake.ui as ui
from disnake.ext import commands
from typing import Sequence

env = dotenv.dotenv_values('.env') or os.environ

class levelInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojiList = {"Badges": "<:Badge:1372922191934656612>", "Description": "<:Description:1372561094014537830>", "Tutorial": "<:Objective:1372561114524553226>", "Entities": "<:Skull:1372670255284883476>", "Fun Facts": "<:Tips:1372670198125035571>", "Level Type": "<:Note:1372670234841845973>", "Simulation Cores": "<:Core:1372922221265293395>"}
            # available emojis
            # <:Origin:1372670213702811728>; <:Question:1372670182937460766>; <:Exit:1372670158610632905>; <:Gallery:1372670132249296946>; <:Wrench:1372670271957368893>, <:Overview:1372561106219827341>

    @commands.slash_command(name='level', description='Shows information about a specified level.') # init the slash command
    async def levelinfo(self, interaction: disnake.CommandInteraction, level: str): # I understand it now.
        try:
            content = self.bot.jsones["newlevel.json"][level]
            sections = content['sections']
            images = content['images']

            components: Sequence[ui.UIComponent] = [ # init components v2
                ui.Container(
                    ui.TextDisplay(f'# {level}'),
                    ui.Separator(spacing=disnake.SeparatorSpacingSize.small),
                    *[ # i have no idea how this works but its perfect and i dont want to touch this EVER
                        item
                        for key, value in sections.items()
                        for item in (
                            ui.TextDisplay(f"## {self.emojiList.get(key, '')}  {key}\n**    {value}**"),
                            ui.Separator(spacing=disnake.SeparatorSpacingSize.small),
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
                ),
            ]

            await interaction.response.send_message(components=components, flags=disnake.MessageFlags(is_components_v2=True))
        except KeyError:
            await interaction.response.send_message(f"*Incorrect option picked!*\nPlease, wait for all the options to appear.\n-# If nothing shows up after some time, report this to the developer.", ephemeral=True)
    
    @levelinfo.autocomplete("level")
    async def level_autocomplete(self, inter: disnake.ApplicationCommandInteraction, string: str):
        if not self.levelList:
            return []

        suggestions = [
            level_name for level_name in self.levelList.keys()
            if string.lower() in level_name.lower()
        ][:25]  # Discord limit for autocomplete options

        return suggestions

def setup(bot): # setup the cog
    bot.add_cog(levelInfo(bot))